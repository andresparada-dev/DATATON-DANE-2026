#!/usr/bin/env python3
"""Ruta 2 · Controles de calidad y referencia nacional a partir de la respuesta cruda de la API CENU.

Entrada: Excel exportado de POST /structural/general con granularity="country" y variables
         ciiu_division, total_income_2023, total_employed_personnel (columna `pais` con el JSON).
Uso:     python ruta2/control_calidad.py ruta2_resultados_api.xlsx [--bogota ruta2_resultados.xlsx]
Salida:  ruta2_control_calidad.xlsx, ruta2_nacional_rangos.png
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ruta2_bogota import DIVISIONES, clasificar_rango, gran_sector  # noqa: E402

UNIVERSO_MODULO = 1_058_881          # GET /structural/modules-universes → sectoral_reference_2023
UNIVERSO_GENERAL = 2_005_248         # general_distribution
INGRESOS_PUBLICADOS_BILLONES = 2421  # cifra difundida por el DANE (ingresos 2023 ≈ $2.421 billones)

# Resultado de ruta2_bogota.py (consola del equipo, 24-oct-2026). Se sobrescribe con --bogota si se pasa el Excel.
BOGOTA_TOP = {47: 92335, 56: 23357, 45: 11089, 96: 9125, 46: 8592, 95: 5258, 86: 4023, 85: 2361,
              14: 1994, 25: 1801, 10: 1658, 52: 1621}
BOGOTA_TOTAL = 195_745
# Los % bajo/alto de Bogotá se leen de la salida corregida de ruta2_bogota.py (--bogota ruta2_resultados.xlsx).
BOGOTA_IND: dict[int, tuple[float, float]] = {}


def _buscar_variables(x):
    """Devuelve el primer dict de la respuesta que contenga la variable ciiu_division con sus values."""
    if isinstance(x, dict):
        if isinstance(x.get("ciiu_division"), dict) and "values" in x["ciiu_division"]:
            return x
        for v in x.values():
            r = _buscar_variables(v)
            if r:
                return r
    elif isinstance(x, list):
        for v in x:
            r = _buscar_variables(v)
            if r:
                return r
    return None


def descargar_pais() -> dict:
    """Consulta nacional de las 3 variables de la Ruta 2 directamente a la API."""
    import requests
    from ruta2_bogota import BASE, MODULO
    variables = ["ciiu_division", "total_income_2023", "total_employed_personnel"]
    intentos = []
    for body in ({"module": MODULO, "variables": variables, "granularity": "country"},
                 {"module": MODULO, "variables": variables, "variable_filters": {"granularity": "country"}},
                 {"module": MODULO, "variables": variables, "granularity": "country", "variable_filters": {}}):
        r = requests.post(f"{BASE}/structural/general", json=body, timeout=180)
        intentos.append((r.status_code, json.dumps(body), r.text[:200]))
        if r.ok:
            pais = _buscar_variables(r.json())
            if pais:
                print("Datos nacionales descargados de la API con body:", body)
                return pais
    for t in intentos:
        print("intento:", *t)
    raise RuntimeError("No se pudo descargar el nivel nacional. Sube el Excel de la API y pasa su nombre.")


def leer_pais(ruta: str | None) -> dict:
    if not ruta or not Path(ruta).exists():
        if ruta:
            print(f"No existe {ruta}; se descargan los datos nacionales desde la API.")
        return descargar_pais()
    df = pd.read_excel(ruta)
    celda = df["pais"].dropna().iloc[0]
    celda = celda if isinstance(celda, dict) else ast.literal_eval(celda)
    return _buscar_variables(celda) or celda


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("excel_api", nargs="?", default=None, help="Excel con la respuesta nacional (opcional)")
    ap.add_argument("--salida", default=".")
    ap.add_argument("--bogota", default=None, help="ruta2_resultados.xlsx (salida corregida de ruta2_bogota.py)")
    a = ap.parse_args()
    if a.bogota:
        ct = pd.read_excel(a.bogota, sheet_name="cuadro_top")
        BOGOTA_IND.update({int(r.division): (r.pct_bajo_ingreso, r.pct_alto_ingreso) for r in ct.itertuples()})
    out = Path(a.salida)
    d = leer_pais(a.excel_api)

    div = pd.DataFrame(d["ciiu_division"]["values"])
    ing = pd.DataFrame(d["total_income_2023"]["values"])
    per = pd.DataFrame(d["total_employed_personnel"]["values"])
    tc_div = d["ciiu_division"]["total_count"]
    tc_ing = d["total_income_2023"]["total_count"]
    tc_per = d["total_employed_personnel"]["total_count"]
    tv_ing = d["total_income_2023"]["total_value"]

    validos = div["codigo"].str.fullmatch(r"\d{2}")
    div["division"] = pd.to_numeric(div["codigo"].where(validos), errors="coerce")

    # ---------------- controles
    ctl = [
        ("Universo módulo sectoral_reference_2023", UNIVERSO_MODULO, "GET /structural/modules-universes"),
        ("Universo distribución general", UNIVERSO_GENERAL, "El módulo cubre el {:.1f}% del universo general".format(100 * UNIVERSO_MODULO / UNIVERSO_GENERAL)),
        ("ciiu_division: total_count", tc_div, ""),
        ("ciiu_division: Σ conteo", int(div["conteo"].sum()), "OK" if div["conteo"].sum() == tc_div else "NO CUADRA"),
        ("ciiu_division: Σ porcentaje", round(div["porcentaje"].sum(), 2), "≈100 por redondeo"),
        ("ciiu_division: unidades sin división (universo − total_count)", UNIVERSO_MODULO - tc_div,
         f"{100 * (UNIVERSO_MODULO - tc_div) / UNIVERSO_MODULO:.4f}% del universo"),
        ("ciiu_division: códigos inválidos", int(div.loc[~validos, "conteo"].sum()), ", ".join(div.loc[~validos, "codigo"])),
        ("ciiu_division: n.º de divisiones válidas", int(validos.sum()), ""),
        ("Ingreso 2023: total_count (respondieron)", tc_ing, ""),
        ("Ingreso 2023: Σ rangos", int(ing["value"].sum()), "OK" if ing["value"].sum() == tc_ing else "NO CUADRA"),
        ("Ingreso 2023: % respuesta sobre universo", round(100 * tc_ing / UNIVERSO_MODULO, 2), f"sin dato: {UNIVERSO_MODULO - tc_ing:,}"),
        ("Ingreso 2023: total_value (billones COP)", round(tv_ing / 1e12, 1),
         f"Cifra publicada ≈ {INGRESOS_PUBLICADOS_BILLONES} billones → {'CUADRA' if abs(tv_ing / 1e12 - INGRESOS_PUBLICADOS_BILLONES) < 1 else 'revisar'}"),
        ("Ingreso 2023: promedio por unidad (millones COP)", round(d["total_income_2023"]["average"] / 1e6, 1),
         "Media muy superior a la mediana (11–50 M): alta concentración"),
        ("Personal: total_count (respondieron)", tc_per, ""),
        ("Personal: Σ rangos", int(per["value"].sum()), "OK" if per["value"].sum() == tc_per else "NO CUADRA"),
        ("Personal: % respuesta sobre universo", round(100 * tc_per / UNIVERSO_MODULO, 2), f"sin dato: {UNIVERSO_MODULO - tc_per:,}"),
        ("Bogotá: unidades con división CIIU", BOGOTA_TOTAL, f"{100 * BOGOTA_TOTAL / tc_div:.1f}% del total nacional del módulo"),
    ]
    control = pd.DataFrame(ctl, columns=["control", "valor", "nota"])

    # ---------------- rangos nacionales
    def resumen_rangos(df, etq, total):
        r = df.rename(columns={"value": "unidades"}).assign(
            variable=etq, pct_respondientes=lambda x: 100 * x["unidades"] / total,
            clase=lambda x: x["description"].map(lambda s: clasificar_rango(s, etq)))
        r["pct_acumulado"] = r["pct_respondientes"].cumsum()
        return r[["variable", "code", "unidades", "pct_respondientes", "pct_acumulado", "clase"]]

    rangos = pd.concat([resumen_rangos(ing, "ingreso", tc_ing), resumen_rangos(per, "personal", tc_per)], ignore_index=True)
    ind_nac = rangos.groupby(["variable", "clase"])["pct_respondientes"].sum().unstack().round(2)

    # ---------------- top 10 nacional y comparación con Bogotá
    dv = div.dropna(subset=["division"]).astype({"division": int})
    dv["nombre"] = dv["division"].map(DIVISIONES)
    dv["gran_sector"] = dv["division"].map(gran_sector)
    dv = dv.sort_values("conteo", ascending=False, ignore_index=True)
    dv["rank_nacional"] = dv.index + 1
    sector_nac = dv.groupby("gran_sector")["conteo"].sum().sort_values(ascending=False)
    sector_nac = pd.DataFrame({"unidades": sector_nac, "pct": (100 * sector_nac / sector_nac.sum()).round(2)})

    bog = pd.DataFrame({"division": list(BOGOTA_TOP), "unidades_bogota": list(BOGOTA_TOP.values())})
    bog["rank_bogota"] = range(1, len(bog) + 1)
    comp = bog.merge(dv[["division", "nombre", "gran_sector", "conteo", "porcentaje", "rank_nacional"]], on="division", how="left")
    comp = comp.rename(columns={"conteo": "unidades_nacional", "porcentaje": "pct_nacional"})
    comp["pct_bogota"] = 100 * comp["unidades_bogota"] / BOGOTA_TOTAL
    comp["participacion_bogota_en_nacional"] = 100 * comp["unidades_bogota"] / comp["unidades_nacional"]
    comp["LQ_bogota"] = (comp["unidades_bogota"] / BOGOTA_TOTAL) / (comp["unidades_nacional"] / tc_div)
    comp["pct_bajo_ingreso_bog"] = comp["division"].map(lambda x: BOGOTA_IND.get(x, (float("nan"),) * 2)[0])
    comp["pct_alto_ingreso_bog"] = comp["division"].map(lambda x: BOGOTA_IND.get(x, (float("nan"),) * 2)[1])
    comp["dif_bajo_vs_nacional_pp"] = comp["pct_bajo_ingreso_bog"] - ind_nac.loc["ingreso", "bajo"]
    comp["dif_alto_vs_nacional_pp"] = comp["pct_alto_ingreso_bog"] - ind_nac.loc["ingreso", "alto"]

    top_nac = dv.head(15)[["rank_nacional", "division", "nombre", "gran_sector", "conteo", "porcentaje"]].copy()
    top_nac["pct_acumulado"] = top_nac["porcentaje"].cumsum()
    top_nac["en_top10_bogota"] = top_nac["division"].isin(list(BOGOTA_TOP)[:10])

    xlsx = out / "ruta2_control_calidad.xlsx"
    with pd.ExcelWriter(xlsx) as w:
        control.to_excel(w, sheet_name="controles", index=False)
        top_nac.round(2).to_excel(w, sheet_name="top15_nacional", index=False)
        comp.round(3).to_excel(w, sheet_name="bogota_vs_nacional", index=False)
        rangos.round(2).to_excel(w, sheet_name="rangos_nacionales", index=False)
        ind_nac.to_excel(w, sheet_name="indicadores_nacionales")
        sector_nac.to_excel(w, sheet_name="gran_sector_nacional")
        dv.to_excel(w, sheet_name="divisiones_nacional", index=False)

    pd.set_option("display.width", 220)
    print(control.to_string(index=False))
    print("\nIndicadores nacionales (% sobre respondientes):\n", ind_nac)
    print("\nGran sector nacional:\n", sector_nac)
    print("\nTop 15 nacional:\n", top_nac.round(2).to_string(index=False))
    print("\nBogotá vs nacional:\n", comp.round(2).to_string(index=False))
    graficar(rangos, out / "ruta2_nacional_rangos.png")
    print("\n->", xlsx)


def graficar(rangos, ruta):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"bajo": "#e34948", "medio": "#b4b2a9", "alto": "#2a78d6"}
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
    for ax, (etq, tit) in zip(axs, (("ingreso", "Ingresos 2023 (millones COP)"), ("personal", "Personal ocupado"))):
        r = rangos[rangos["variable"] == etq]
        ax.barh(r["code"][::-1], r["pct_respondientes"][::-1], color=[col[c] for c in r["clase"][::-1]],
                height=0.65, edgecolor="white", linewidth=1.5)
        for y, v in enumerate(r["pct_respondientes"][::-1]):
            ax.text(v + 0.5, y, f"{v:.1f}%", va="center", fontsize=8, color="#52514e")
        ax.set_title(tit, loc="left", fontweight="bold")
        ax.set_xlabel("% de unidades que respondieron")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.suptitle("Colombia urbana · módulo sectoral_reference_2023 (CENU preliminar) · rojo = rango bajo, azul = rango alto",
                 x=0.01, ha="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
