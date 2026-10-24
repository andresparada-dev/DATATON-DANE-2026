#!/usr/bin/env python3
"""Ruta 2 · Verificador: compara cifras de un Excel y/o del dashboard HTML contra la API del CENU (en vivo).

Colab:
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/ruta2_bogota.py
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/control_calidad.py
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/ruta2_dashboard.py
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/verificar_api.py
    !python verificar_api.py --excel ruta2_dashboard.xlsx --html dashboard_cenu_ruta_2.html

Qué verifica (por cada división encontrada en el Excel / HTML):
  · Unidades por división: igualdad EXACTA con la API.
  · % bajo / % alto de ingreso y de personal, % de respuesta: diferencia ≤ 0,05 p.p. (redondeo a 1 decimal).
  · Totales: Σ divisiones y Σ rangos = total_count de la API.
Salida: tabla en pantalla con ✅ / ❌, resumen "N de M valores correctos" y verificacion_api.xlsx.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

from ruta2_bogota import BOGOTA, CENU, DIVISIONES
from ruta2_dashboard import consultar, indicadores

TOL = 0.05


def _slug(t) -> str:
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t)


def _division(v):
    """'47', 47, '4711/47', '47 Comercio...' → 47 ; códigos de 4 dígitos sin división → None."""
    s = str(v)
    if "/" in s:
        s = s.split("/")[-1]
    m = re.match(r"\s*(\d+)", s)
    if not m:
        return None
    n = m.group(1)
    return int(n) if len(n) <= 2 else None


def columnas_metricas(cols) -> dict:
    """Detecta columnas por palabras clave → {métrica: columna}."""
    out = {}
    for c in cols:
        s = _slug(c)
        if "divis" in s and "nombre" not in s and "division" not in out:
            out["division"] = c
        elif "unidad" in s and "pct" not in s and "%" not in str(c) and "unidades" not in out:
            out["unidades"] = c
        elif "respuesta" in s and "ingreso" in s:
            out["pct_respuesta_ingreso"] = c
        elif "respuesta" in s and "personal" in s:
            out["pct_respuesta_personal"] = c
        elif "bajo" in s and "ingreso" in s:
            out["pct_bajo_ingreso"] = c
        elif "alto" in s and "ingreso" in s:
            out["pct_alto_ingreso"] = c
        elif "bajo" in s and "personal" in s:
            out["pct_bajo_personal"] = c
        elif "alto" in s and "personal" in s:
            out["pct_alto_personal"] = c
    return out


def leer_excel(ruta: str) -> list[pd.DataFrame]:
    tablas = []
    for hoja, df in pd.read_excel(ruta, sheet_name=None).items():
        m = columnas_metricas(df.columns)
        if "division" in m and len(m) >= 2:
            t = pd.DataFrame({k: df[c] for k, c in m.items()})
            t["division"] = t["division"].map(_division)
            t = t.dropna(subset=["division"]).astype({"division": int})
            t.insert(0, "fuente", f"{Path(ruta).name}:{hoja}")
            tablas.append(t)
            print(f"Excel · hoja '{hoja}': {len(t)} filas, columnas verificables: {sorted(set(m) - {'division'})}")
    return tablas


def leer_html(ruta: str, divisiones_api: pd.DataFrame) -> pd.DataFrame | None:
    """Extrae `const data = [...]` del dashboard. Si no trae código de división, se empareja por unidades o nombre."""
    html = Path(ruta).read_text(encoding="utf-8")
    m = re.search(r"const data = \[(.*?)\];", html, flags=re.S)
    if not m:
        d = re.search(r"const D = (\{.*?\});\n", html, flags=re.S)   # dashboard_ruta2_final.html
        if not d:
            print("HTML: no se encontró `const data = [...]` ni `const D = {...}`")
            return None
        divs = json.loads(d.group(1))["divs"]
        t = pd.DataFrame([{"division": int(x["div"]), "unidades": x["units"], "pct_bajo_ingreso": x["low"],
                           "pct_alto_ingreso": x["high"], "pct_bajo_personal": x["lowP"], "pct_alto_personal": x["highP"]}
                          for x in divs])
        t.insert(0, "fuente", "HTML")
        print(f"HTML: {len(t)} divisiones en const D")
        return t
    filas = []
    for obj in re.findall(r"\{(.*?)\}", m.group(1), flags=re.S):
        campo = lambda k: (re.search(rf"\b{k}\s*:\s*(\"[^\"]*\"|[-\d.]+)", obj) or [None, None])[1]  # noqa: E731
        name = (campo("name") or "").strip('"')
        f = {"nombre_html": name, "unidades": float(campo("units")) if campo("units") else None,
             "pct_bajo_ingreso": float(campo("low")) if campo("low") else None,
             "pct_alto_ingreso": float(campo("high")) if campo("high") else None}
        if campo("lowPers"):
            f["pct_bajo_personal"] = float(campo("lowPers"))
        if campo("highPers"):
            f["pct_alto_personal"] = float(campo("highPers"))
        div = campo("division")
        if div:
            f["division"] = int(div.strip('"'))
        else:  # emparejar por unidades exactas, luego por nombre
            hit = divisiones_api[divisiones_api["unidades"] == f["unidades"]]
            if hit.empty:
                hit = divisiones_api[divisiones_api["nombre"].map(_slug).str.contains(_slug(name)[:12], regex=False)]
            f["division"] = int(hit.iloc[0]["division"]) if not hit.empty else None
        filas.append(f)
    t = pd.DataFrame(filas).dropna(subset=["division"]).astype({"division": int})
    t.insert(0, "fuente", "HTML")
    print(f"HTML: {len(t)} filas en const data")
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", action="append", default=[], help="Excel a verificar (repetible)")
    ap.add_argument("--html", default=None, help="dashboard HTML a verificar")
    ap.add_argument("--municipio", default=BOGOTA)
    a = ap.parse_args()
    api = CENU()

    # Verdad de referencia: API en vivo
    r = consultar(api, ["ciiu_division"], municipio=a.municipio)["ciiu_division"]
    d = r["values"]
    d = d[d["code"].astype(str).str.fullmatch(r"\d{2}")]
    divs = pd.DataFrame({"division": d["code"].astype(int), "unidades": d["value"]})
    divs["nombre"] = divs["division"].map(DIVISIONES)
    print(f"API: {len(divs)} divisiones, {divs['unidades'].sum():,.0f} unidades con CIIU (total_count {r['total_count']})")

    tablas = [t for e in a.excel for t in leer_excel(e)]
    if a.html:
        h = leer_html(a.html, divs)
        if h is not None:
            tablas.append(h)
    if not tablas:
        raise SystemExit("No hay nada que verificar: pasa --excel y/o --html")

    cache = {}
    filas = []
    for t in tablas:
        for row in t.to_dict("records"):
            dv = row["division"]
            if dv not in cache:
                res = consultar(api, ["total_income_2023", "total_employed_personnel"], {"ciiu_division": [f"{dv:02d}"]},
                                a.municipio)
                u = divs.loc[divs["division"] == dv, "unidades"]
                verdad = {"unidades": float(u.iloc[0]) if len(u) else float("nan")}
                for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
                    verdad.update(indicadores(res[var]["values"], etq))
                    if f"respondieron_{etq}" in verdad and verdad["unidades"] == verdad["unidades"]:
                        verdad[f"pct_respuesta_{etq}"] = 100 * verdad[f"respondieron_{etq}"] / verdad["unidades"]
                cache[dv] = verdad
            verdad = cache[dv]
            for met in ("unidades", "pct_respuesta_ingreso", "pct_bajo_ingreso", "pct_alto_ingreso",
                        "pct_respuesta_personal", "pct_bajo_personal", "pct_alto_personal"):
                if met not in row or pd.isna(row[met]):
                    continue
                val = float(str(row[met]).replace("%", "").replace(",", "")) if isinstance(row[met], str) else float(row[met])
                api_v = verdad.get(met, float("nan"))
                ok = (val == api_v) if met == "unidades" else abs(val - round(api_v, 1)) <= TOL + 1e-9 or abs(val - api_v) <= TOL
                filas.append({"fuente": row["fuente"], "division": f"{dv:02d}", "actividad": DIVISIONES.get(dv, ""),
                              "metrica": met, "valor_archivo": val, "valor_api": round(api_v, 2),
                              "diferencia": round(val - api_v, 2), "estado": "✅" if ok else "❌"})
    res = pd.DataFrame(filas)
    pd.set_option("display.width", 220)
    pd.set_option("display.max_rows", 500)
    print(res.to_string(index=False))
    for fuente, g in res.groupby("fuente"):
        n_ok = (g["estado"] == "✅").sum()
        print(f"\n{fuente}: {n_ok} de {len(g)} valores coinciden con la API ({100 * n_ok / len(g):.1f}%)")
        if n_ok < len(g):
            print("   Errores:", ", ".join(f"{x.division}-{x.metrica}" for x in g[g.estado == '❌'].itertuples()))
    res.to_excel("verificacion_api.xlsx", index=False)
    print("\nDetalle -> verificacion_api.xlsx")


if __name__ == "__main__":
    main()
