#!/usr/bin/env python3
"""Ruta 2 · Bogotá — genera desde la API del CENU el Excel del dashboard y los datos para el HTML.

Colab:
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/ruta2_bogota.py
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/control_calidad.py
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/ruta2_dashboard.py
    !python ruta2_dashboard.py --top 12 --html dashboard_cenu_ruta_2.html     # --html es opcional

Salida:
    ruta2_dashboard.xlsx  hojas: kpis, top_divisiones, rangos_por_division, bogota_rangos_total,
                          divisiones, por_sector, nacional_rangos, controles, fuentes
    dashboard_data.js     bloque `const data = [...]` listo para pegar en el HTML
    <html>_actualizado.html  si se pasa --html: el mismo dashboard con las cifras de la API

Reglas (iguales a la guía de la Ruta 2):
  · % sobre las unidades que RESPONDIERON; "Sin información" (en personal, el rango "0") no entra al denominador.
  · Bajo: ingreso 0-10 M · personal 1-5.   Alto: ingreso > 1.000 M · personal > 50.
  · Tipología frente a la referencia nacional (bajo 23,8 % / alto 6,1 % de ingreso, o la que devuelva la API).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from ruta2_bogota import BOGOTA, CENU, DIVISIONES, MODULO, clasificar_rango

REF_NACIONAL_DEFECTO = (23.76, 6.12)   # % bajo / % alto de ingreso, nivel nacional (API, granularity=country)
ICONOS = {47: "fa-shop", 56: "fa-utensils", 45: "fa-car", 96: "fa-scissors", 46: "fa-boxes-stacked",
          95: "fa-laptop-medical", 86: "fa-stethoscope", 85: "fa-graduation-cap", 14: "fa-shirt",
          25: "fa-hammer", 10: "fa-bread-slice", 52: "fa-warehouse", 55: "fa-bed", 49: "fa-truck",
          69: "fa-scale-balanced", 62: "fa-laptop-code", 68: "fa-building", 33: "fa-screwdriver-wrench"}


def sector_cenu(d: int) -> str:
    return ("Agro y minería" if d <= 9 else "Industria" if d <= 39 else "Construcción" if d <= 43
            else "Comercio" if d <= 47 else "Transporte" if d <= 53 else "Servicios")


def buscar_variable(x, var):
    """Primer dict {total_count, values} asociado a `var` dentro de la respuesta (cualquier anidamiento)."""
    if isinstance(x, dict):
        if isinstance(x.get(var), dict) and "values" in x[var]:
            return x[var]
        for v in x.values():
            r = buscar_variable(v, var)
            if r is not None:
                return r
    elif isinstance(x, list):
        for v in x:
            r = buscar_variable(v, var)
            if r is not None:
                return r
    return None


def consultar(api: CENU, variables: list[str], filtros: dict | None = None, municipio: str = BOGOTA) -> dict:
    """POST structural/general → {variable: {"total_count": n, "values": DataFrame(code, description, value)}}."""
    body = {"module": MODULO, "variables": variables,
            "variable_filters": {"municipality_ids": [municipio], **(filtros or {})}}
    r = api.post("structural/general", body)
    if not r.ok:
        raise RuntimeError(f"{r.status_code} {r.text[:300]} · body={json.dumps(body, ensure_ascii=False)}")
    j = r.json()
    api.log.append({"body": body, "respuesta": j})
    out = {}
    for var in variables:
        res = buscar_variable(j, var) or {"values": []}
        vals = pd.DataFrame([{
            "code": v.get("codigo", v.get("code")),
            "description": v.get("descripcion") or v.get("description") or v.get("codigo", v.get("code")),
            "value": float(v.get("conteo", v.get("value")) or 0)} for v in res.get("values", [])])
        out[var] = {"total_count": res.get("total_count"), "values": vals}
    return out


def indicadores(vals: pd.DataFrame, etq: str) -> dict:
    """% bajo / medio / alto sobre respondientes + respondientes + sin dato."""
    if vals.empty:
        return {}
    v = vals.assign(clase=vals["description"].map(lambda d: clasificar_rango(d, etq)))
    resp = v.loc[v["clase"] != "sin_dato", "value"].sum()
    sin = v.loc[v["clase"] == "sin_dato", "value"].sum()
    pct = lambda c: 100 * v.loc[v["clase"] == c, "value"].sum() / resp if resp else float("nan")  # noqa: E731
    return {f"respondieron_{etq}": resp, f"sin_info_{etq}": sin, f"pct_bajo_{etq}": pct("bajo"),
            f"pct_medio_{etq}": pct("medio"), f"pct_alto_{etq}": pct("alto")}


def tipologia(bajo, alto, ref) -> str:
    nb, na = ref
    if pd.isna(bajo) or pd.isna(alto):
        return "Sin datos"
    if alto > na:
        return "Polarizado" if bajo >= 20 else "Base para escalar"
    return "Señal de subsistencia" if bajo >= 20 else "Intermedio"


def nacional(api: CENU):
    """Rangos nacionales (granularity=country). Devuelve (ref_bajo, ref_alto, DataFrame) o None si la API no responde."""
    try:
        from control_calidad import descargar_pais
        pais = descargar_pais()
    except Exception as e:  # noqa: BLE001
        print("Aviso: no se pudo consultar el nivel nacional:", e)
        return None
    filas = []
    for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
        vals = pd.DataFrame(pais[var]["values"]).rename(columns={"value": "unidades"})
        vals["clase"] = vals["description"].map(lambda d: clasificar_rango(d, etq))
        resp = vals.loc[vals["clase"] != "sin_dato", "unidades"].sum()
        vals["pct_respondientes"] = (100 * vals["unidades"] / resp).where(vals["clase"] != "sin_dato")
        vals.insert(0, "variable", etq)
        filas.append(vals[["variable", "code", "unidades", "pct_respondientes", "clase"]])
    df = pd.concat(filas, ignore_index=True)
    ing = df[df["variable"] == "ingreso"]
    ref = (ing.loc[ing["clase"] == "bajo", "pct_respondientes"].sum(), ing.loc[ing["clase"] == "alto", "pct_respondientes"].sum())
    return ref, df, pais


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--municipio", default=BOGOTA)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--html", default=None, help="dashboard HTML a actualizar (opcional)")
    ap.add_argument("--salida", default=".")
    a = ap.parse_args()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    api = CENU()

    try:
        universos = api.get("structural/modules-universes")
    except Exception:  # noqa: BLE001
        universos = {}
    # 1) Divisiones CIIU del municipio
    r = consultar(api, ["ciiu_division"], municipio=a.municipio)["ciiu_division"]
    div = r["values"].copy()
    div["division"] = pd.to_numeric(div["code"].astype(str).where(div["code"].astype(str).str.fullmatch(r"\d{2}")),
                                     errors="coerce")
    invalidas = int(div.loc[div["division"].isna(), "value"].sum())
    div = div.dropna(subset=["division"]).astype({"division": int})
    div = div.groupby("division", as_index=False)["value"].sum().rename(columns={"value": "unidades"})
    div["nombre"] = div["division"].map(DIVISIONES)
    div["sector_cenu"] = div["division"].map(sector_cenu)
    con_ciiu = int(div["unidades"].sum())
    div["pct_unidades"] = 100 * div["unidades"] / con_ciiu
    div = div.sort_values("unidades", ascending=False, ignore_index=True)
    div["rank"] = div.index + 1

    # 2) Agregado del municipio (sin filtro de división) e indicadores por división
    agg = consultar(api, ["total_income_2023", "total_employed_personnel"], municipio=a.municipio)
    nac = nacional(api)
    ref = nac[0] if nac else REF_NACIONAL_DEFECTO
    filas, detalle = [], []
    for d in div.head(a.top).itertuples():
        fila = {"rank": d.rank, "division": d.division, "nombre": d.nombre, "sector_cenu": d.sector_cenu,
                "unidades": d.unidades, "pct_unidades": d.pct_unidades}
        res = consultar(api, ["total_income_2023", "total_employed_personnel"], {"ciiu_division": [f"{d.division:02d}"]},
                        a.municipio)
        for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
            vals = res[var]["values"]
            fila.update(indicadores(vals, etq))
            if f"respondieron_{etq}" in fila:
                fila[f"pct_respuesta_{etq}"] = 100 * fila[f"respondieron_{etq}"] / d.unidades
            if not vals.empty:
                detalle.append(vals.assign(division=d.division, variable=etq,
                                           clase=vals["description"].map(lambda s, e=etq: clasificar_rango(s, e))))
        fila["tipologia"] = tipologia(fila.get("pct_bajo_ingreso"), fila.get("pct_alto_ingreso"), ref)
        filas.append(fila)
        print(f"  {d.division:02d} {d.nombre[:40]:40s} {d.unidades:>8,.0f}  bajo {fila.get('pct_bajo_ingreso', float('nan')):5.1f}%"
              f"  alto {fila.get('pct_alto_ingreso', float('nan')):5.1f}%  {fila['tipologia']}")
    top = pd.DataFrame(filas)
    rangos = pd.concat(detalle, ignore_index=True) if detalle else pd.DataFrame()

    bog_rangos = []
    for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
        v = agg[var]["values"].assign(variable=etq)
        v["clase"] = v["description"].map(lambda s, e=etq: clasificar_rango(s, e))
        resp = v.loc[v["clase"] != "sin_dato", "value"].sum()
        v["pct_respondientes"] = (100 * v["value"] / resp).where(v["clase"] != "sin_dato")
        v["pct_total"] = 100 * v["value"] / v["value"].sum()
        bog_rangos.append(v)
    bog_rangos = pd.concat(bog_rangos, ignore_index=True)
    ind_bog = {etq: indicadores(agg[var]["values"], etq) for var, etq in
               (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal"))}

    por_sector = div.groupby("sector_cenu", as_index=False)["unidades"].sum().sort_values("unidades", ascending=False)
    por_sector["pct"] = 100 * por_sector["unidades"] / con_ciiu

    universo_mod = (universos.get(MODULO) or {}).get("universe")
    kpis = pd.DataFrame([
        ("Municipio (DIVIPOLA)", a.municipio),
        ("Unidades con división CIIU visible", con_ciiu),
        ("total_count de ciiu_division (API)", r["total_count"]),
        ("Divisiones CIIU con unidades", len(div)),
        ("Códigos de división no válidos", invalidas),
        ("% bajo ingreso (municipio)", round(ind_bog["ingreso"].get("pct_bajo_ingreso", float("nan")), 2)),
        ("% alto ingreso (municipio)", round(ind_bog["ingreso"].get("pct_alto_ingreso", float("nan")), 2)),
        ("% bajo personal 1-5 (municipio)", round(ind_bog["personal"].get("pct_bajo_personal", float("nan")), 2)),
        ("% alto personal >50 (municipio)", round(ind_bog["personal"].get("pct_alto_personal", float("nan")), 2)),
        ("Referencia nacional % bajo ingreso", round(ref[0], 2)),
        ("Referencia nacional % alto ingreso", round(ref[1], 2)),
        ("Universo nacional del módulo", universo_mod),
        ("Mayor % alto ingreso (top)", f"{int(top.loc[top.pct_alto_ingreso.idxmax(), 'division']):02d} {top.loc[top.pct_alto_ingreso.idxmax(), 'nombre']} ({top.pct_alto_ingreso.max():.1f}%)"),
        ("Mayor % bajo ingreso (top)", f"{int(top.loc[top.pct_bajo_ingreso.idxmax(), 'division']):02d} {top.loc[top.pct_bajo_ingreso.idxmax(), 'nombre']} ({top.pct_bajo_ingreso.max():.1f}%)"),
    ], columns=["indicador", "valor"])
    controles = pd.DataFrame([
        ("Σ unidades de divisiones = total_count", con_ciiu + invalidas, r["total_count"],
         "OK" if r["total_count"] in (None, con_ciiu + invalidas) else "REVISAR"),
        ("Σ rangos ingreso (municipio) = total_count", agg["total_income_2023"]["values"]["value"].sum(),
         agg["total_income_2023"]["total_count"], "OK" if agg["total_income_2023"]["total_count"] in
         (None, agg["total_income_2023"]["values"]["value"].sum()) else "REVISAR"),
        ("Σ rangos personal (municipio) = total_count", agg["total_employed_personnel"]["values"]["value"].sum(),
         agg["total_employed_personnel"]["total_count"], "OK" if agg["total_employed_personnel"]["total_count"] in
         (None, agg["total_employed_personnel"]["values"]["value"].sum()) else "REVISAR"),
    ], columns=["control", "calculado", "api", "resultado"])
    fuentes = pd.DataFrame([
        ("API Visor Interactivo CENU", "https://censoeconomiconacionalurbano.dane.gov.co/backend/api/v1/structural/general"),
        ("Módulo", MODULO), ("Resultados", "Preliminares (DANE, CENU 2024; año de referencia 2023)"),
        ("Regla de supresión", "No se publican municipios con menos de 30 unidades; algunos CIIU no visibles por reserva"),
    ], columns=["campo", "valor"])

    xlsx = out / "ruta2_dashboard.xlsx"
    with pd.ExcelWriter(xlsx) as w:
        kpis.to_excel(w, sheet_name="kpis", index=False)
        top.round(2).to_excel(w, sheet_name="top_divisiones", index=False)
        rangos.round(2).to_excel(w, sheet_name="rangos_por_division", index=False)
        bog_rangos.round(2).to_excel(w, sheet_name="bogota_rangos_total", index=False)
        div.round(3).to_excel(w, sheet_name="divisiones", index=False)
        por_sector.round(2).to_excel(w, sheet_name="por_sector", index=False)
        if nac:
            nac[1].round(2).to_excel(w, sheet_name="nacional_rangos", index=False)
        controles.to_excel(w, sheet_name="controles", index=False)
        fuentes.to_excel(w, sheet_name="fuentes", index=False)
    (out / "ruta2_respuestas_api.json").write_text(json.dumps(api.log, ensure_ascii=False))

    js = "const data = [\n" + ",\n".join(
        f'            {{ name: {json.dumps(t.nombre, ensure_ascii=False)}, division: "{t.division:02d}", units: {int(t.unidades)}, '
        f'low: {t.pct_bajo_ingreso:.1f}, high: {t.pct_alto_ingreso:.1f}, '
        f'lowPers: {t.pct_bajo_personal:.1f}, highPers: {t.pct_alto_personal:.1f}, '
        f'tipologia: {json.dumps(t.tipologia, ensure_ascii=False)}, icon: "{ICONOS.get(t.division, "fa-briefcase")}" }}'
        for t in top.itertuples()) + "\n        ];"
    (out / "dashboard_data.js").write_text(js, encoding="utf-8")
    if a.html:
        html = Path(a.html).read_text(encoding="utf-8")
        nuevo, n = re.subn(r"const data = \[.*?\];", js, html, count=1, flags=re.S)
        if n:
            dest = out / (Path(a.html).stem + "_actualizado.html")
            dest.write_text(nuevo, encoding="utf-8")
            print("HTML actualizado (bloque de datos):", dest, "· revisar también los textos fijos (KPIs y conclusiones)")
    print(f"\nListo: {xlsx}\n       {out / 'dashboard_data.js'}")


if __name__ == "__main__":
    main()
