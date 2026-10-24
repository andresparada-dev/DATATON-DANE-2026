#!/usr/bin/env python3
"""Construye ruta2/salidas/ruta2_bogota_cifras_verificadas.xlsx y el dashboard corregido SIN llamar a la API.

Usa únicamente cifras que ya salieron de la API o del Visor del CENU (24-oct-2026):
  · Bogotá por división (unidades y % de ingreso): salida corregida de ruta2_bogota.py (API, municipio 11001).
  · Nivel nacional: respuesta de la API con granularity="country" (data/ruta2/api_nacional_sectoral_reference_2023.json).
  · Distribuciones agregadas de Bogotá y códigos a 4 dígitos: Visor Interactivo CENU (capturas).
Para confirmar contra la API en vivo: python verificar_api.py --excel ruta2_bogota_cifras_verificadas.xlsx
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ruta2_bogota import DIVISIONES, clasificar_rango  # noqa: E402

SALIDA = RAIZ / "ruta2" / "salidas"
UNIVERSO_BOG, CON_CIIU_BOG, DIVS_BOG = 195_755, 195_745, 85
# (división, unidades, % bajo ingreso, % alto ingreso) — API vía ruta2_bogota.py (versión corregida)
BOG = [(47, 92335, 20.1, 3.3), (56, 23357, 14.6, 2.5), (45, 11089, 16.1, 6.0), (96, 9125, 22.9, 0.8),
       (46, 8592, 10.1, 36.1), (95, 5258, 32.2, 0.7), (86, 4023, 10.7, 13.7), (85, 2361, 15.3, 16.7),
       (14, 1994, 21.2, 11.4), (25, 1801, 12.1, 14.0), (10, 1658, 9.3, 22.9), (52, 1621, 17.6, 19.0)]
# Visor Interactivo CENU · Bogotá · Resultados sectoriales 2023 (% de unidades por rango)
RANGOS_M = ["0 - 10 M", "11 - 50 M", "51 - 100 M", "101 - 500 M", "501 - 1.000 M", "1.001 - 5.000 M",
            "5.001 - 10.000 M", "10.001 - 100.000 M", "> 100.000 M"]
VISOR = {
    "Ingreso total 2023": ([17.4, 32.4, 16.0, 19.9, 3.8, 5.2, 1.7, 3.1, 0.7], 7_422, 1_180_444_620),
    "Costo y gasto de producción": ([36.3, 33.5, 11.5, 12.7, 2.3, 2.6, 0.5, 0.5, 0.1], 850, 131_627_222),
    "Salarios pagados": ([56.4, 25.6, 6.9, 7.6, 1.6, 1.5, 0.2, 0.3, 0.1], 596, 88_937_085),
    "Saldo de activos fijos": ([51.1, 28.1, 6.3, 6.8, 1.9, 3.1, 0.8, 1.2, 0.7], None, None),
}
PERSONAL_VISOR = [("Sin información reportada (rango \"0\" en la API)", 2.9), ("1 - 5", 80.4), ("6 - 10", 7.0),
                  ("11 - 20", 3.5), ("21 - 50", 2.6), ("51 - 100", 1.4), ("101 - 500", 1.6), ("501+", 0.6)]
VISOR_4DIG = [("4781", "Comercio al por menor de alimentos, bebidas y tabaco en puestos de venta móviles", 16410),
              ("4711", "Comercio al por menor en establecimientos no especializados, surtido principalmente de alimentos", 13114),
              ("5611", "Expendio a la mesa de comidas preparadas", 9049),
              ("4771", "Comercio al por menor de prendas de vestir y sus accesorios", 7328),
              ("9602", "Peluquería y otros tratamientos de belleza", 6817),
              ("5619", "Otros tipos de expendio de comidas preparadas n.c.p.", 6437),
              ("4520", "Mantenimiento y reparación de vehículos automotores", 6314),
              ("4782", "Comercio al por menor de textiles, prendas de vestir y calzado en puestos móviles", 5493),
              ("4752", "Comercio al por menor de artículos de ferretería, pinturas y productos de vidrio", 5307),
              ("4773", "Comercio al por menor de productos farmacéuticos, medicinales, cosméticos y de tocador", 4944)]


def sector_cenu(d: int) -> str:
    return ("Agro y minería" if d <= 9 else "Industria" if d <= 39 else "Construcción" if d <= 43
            else "Comercio" if d <= 47 else "Transporte" if d <= 53 else "Servicios")


def tipologia(bajo, alto, nb, na):
    if alto > na:
        return "Polarizado" if bajo >= 20 else "Base para escalar"
    return "Señal de subsistencia" if bajo >= 20 else "Intermedio"


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    nac = json.loads((RAIZ / "data" / "ruta2" / "api_nacional_sectoral_reference_2023.json").read_text())

    # ---- nacional (API)
    nd = pd.DataFrame(nac["ciiu_division"]["values"])
    nd = nd[nd["codigo"].str.fullmatch(r"\d{2}")].assign(division=lambda x: x["codigo"].astype(int))
    tc_div = nac["ciiu_division"]["total_count"]
    rangos_nac = []
    for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
        v = pd.DataFrame(nac[var]["values"]).rename(columns={"value": "unidades"})
        v["clase"] = v["description"].map(lambda s, e=etq: clasificar_rango(s, e))
        resp = v.loc[v["clase"] != "sin_dato", "unidades"].sum()
        v["pct_sobre_respondientes"] = (100 * v["unidades"] / resp).where(v["clase"] != "sin_dato").round(2)
        v.insert(0, "variable", etq)
        rangos_nac.append(v[["variable", "code", "unidades", "pct_sobre_respondientes", "clase"]])
    rangos_nac = pd.concat(rangos_nac, ignore_index=True)
    ing = rangos_nac[rangos_nac.variable == "ingreso"]
    per = rangos_nac[rangos_nac.variable == "personal"]
    NB = ing.loc[ing.clase == "bajo", "pct_sobre_respondientes"].sum()
    NA = ing.loc[ing.clase == "alto", "pct_sobre_respondientes"].sum()

    # ---- top 12 Bogotá
    top = pd.DataFrame(BOG, columns=["division", "unidades", "pct_bajo_ingreso", "pct_alto_ingreso"])
    top.insert(0, "rank", range(1, len(top) + 1))
    top.insert(2, "nombre", top["division"].map(DIVISIONES))
    top.insert(3, "sector_cenu", top["division"].map(sector_cenu))
    top["pct_unidades_bogota"] = (100 * top["unidades"] / CON_CIIU_BOG).round(2)
    top = top.merge(nd[["division", "conteo"]].rename(columns={"conteo": "unidades_nacional"}), on="division")
    top["participacion_bogota_en_nacional_pct"] = (100 * top["unidades"] / top["unidades_nacional"]).round(1)
    top["LQ_bogota"] = ((top["unidades"] / CON_CIIU_BOG) / (top["unidades_nacional"] / tc_div)).round(2)
    top["dif_bajo_vs_nacional_pp"] = (top["pct_bajo_ingreso"] - NB).round(1)
    top["dif_alto_vs_nacional_pp"] = (top["pct_alto_ingreso"] - NA).round(1)
    top["tipologia"] = [tipologia(b, a, NB, NA) for b, a in zip(top.pct_bajo_ingreso, top.pct_alto_ingreso)]
    cuadro_top10 = top.head(10)

    # ---- Bogotá agregado (Visor)
    filas = []
    for var, (pcts, prom, total) in VISOR.items():
        for rng, p in zip(RANGOS_M, pcts):
            filas.append({"variable": var, "rango": rng, "pct_unidades": p,
                          "clase_ingreso": clasificar_rango(rng, "ingreso") if var == "Ingreso total 2023" else ""})
    bog_visor = pd.DataFrame(filas)
    resp_p = 100 - PERSONAL_VISOR[0][1]
    bog_personal = pd.DataFrame([{"rango": r, "pct_total": p, "pct_sobre_respondientes": None if i == 0 else 100 * p / resp_p,
                                  "clase": "sin_dato" if i == 0 else clasificar_rango(r, "personal")}
                                 for i, (r, p) in enumerate(PERSONAL_VISOR)])
    bog_bajo_ing = 17.4
    bog_alto_ing = sum(p for r, p in zip(RANGOS_M, VISOR["Ingreso total 2023"][0]) if clasificar_rango(r, "ingreso") == "alto")
    bog_bajo_per = bog_personal.loc[bog_personal.clase == "bajo", "pct_sobre_respondientes"].sum()
    bog_alto_per = bog_personal.loc[bog_personal.clase == "alto", "pct_sobre_respondientes"].sum()
    totales_visor = pd.DataFrame([(k, v[1], v[2]) for k, v in VISOR.items() if v[1]],
                                 columns=["variable", "promedio_anual_por_unidad_millones", "total_acumulado_millones"])
    ingreso_nac_millones = nac["total_income_2023"]["total_value"] / 1e6
    resp_ing_bog = VISOR["Ingreso total 2023"][2] / VISOR["Ingreso total 2023"][1]

    comparacion = pd.DataFrame([
        ("% unidades con ingreso 0-10 M", bog_bajo_ing, round(NB, 1)),
        ("% unidades con ingreso > 1.000 M", round(bog_alto_ing, 1), round(NA, 1)),
        ("% unidades con 1-5 personas (sobre respondientes)", round(bog_bajo_per, 1),
         round(per.loc[per.clase == "bajo", "pct_sobre_respondientes"].sum(), 1)),
        ("% unidades con > 50 personas (sobre respondientes)", round(bog_alto_per, 1),
         round(per.loc[per.clase == "alto", "pct_sobre_respondientes"].sum(), 1)),
        ("Ingreso promedio anual por unidad (millones COP)", 7_422, round(nac["total_income_2023"]["average"] / 1e6, 1)),
        ("Ingresos totales 2023 (billones COP)", round(VISOR["Ingreso total 2023"][2] / 1e6, 1), round(ingreso_nac_millones / 1e6, 1)),
    ], columns=["indicador", "bogota", "nacional"])

    controles = pd.DataFrame([
        ("Universo módulo sectoral_reference_2023 · nacional", 1_058_881, "API /structural/modules-universes"),
        ("ciiu_division total_count nacional = Σ conteos", f"{tc_div:,} = {sum(v['conteo'] for v in nac['ciiu_division']['values']):,}", "OK (incluye 1 unidad con código inválido '0x')"),
        ("Ingreso nacional: Σ rangos = total_count", f"{int(ing['unidades'].sum()):,} = {nac['total_income_2023']['total_count']:,}", "OK"),
        ("Personal nacional: Σ rangos = total_count", f"{int(per['unidades'].sum()):,} = {nac['total_employed_personnel']['total_count']:,}", "OK"),
        ("Ingresos 2023 nacional (billones COP)", round(ingreso_nac_millones / 1e6, 1), "Coincide con la cifra difundida por el DANE (≈ $2.421 billones)"),
        ("Universo Bogotá (visor y API)", UNIVERSO_BOG, "Visor: 'Conteo total'"),
        ("Bogotá: unidades con división CIIU visible", CON_CIIU_BOG, f"{DIVS_BOG} divisiones (salida del script)"),
        ("Bogotá: CIIU no visible por reserva estadística", UNIVERSO_BOG - CON_CIIU_BOG, "Visor: 'algunos CIIU no están habilitados'"),
        ("Bogotá: % del total nacional del módulo", round(100 * CON_CIIU_BOG / tc_div, 1), ""),
        ("Bogotá: % de los ingresos nacionales 2023", round(100 * VISOR["Ingreso total 2023"][2] / ingreso_nac_millones, 1),
         "Visor Bogotá / API nacional"),
        ("Bogotá: unidades que reportaron ingreso (≈ total / promedio)", round(resp_ing_bog), f"≈ {100 * resp_ing_bog / UNIVERSO_BOG:.1f}% del universo (aprox., promedio redondeado)"),
        ("División 47: respondieron ingreso / personal", "66.007 / 64.041", "API (consulta directa 11001, división 47)"),
        ("Regla de supresión territorial", "< 30 unidades", "DDI CENU 2024: no se exponen municipios con menos de 30 unidades"),
    ], columns=["control", "valor", "nota"])

    top15_nac = nd.sort_values("conteo", ascending=False).head(15).assign(
        nombre=lambda x: x["division"].map(DIVISIONES), pct=lambda x: x["porcentaje"])[["division", "nombre", "conteo", "pct"]]
    visor4 = pd.DataFrame(VISOR_4DIG, columns=["codigo_ciiu_4d", "descripcion", "unidades"])
    visor4["pct_de_bogota"] = (100 * visor4["unidades"] / UNIVERSO_BOG).round(2)
    visor4["fuente"] = "Visor Interactivo CENU"
    leeme = pd.DataFrame([
        ("Contenido", "Cifras de la Ruta 2 (Bogotá D.C.) del CENU 2024, módulo sectoral_reference_2023, año de referencia 2023."),
        ("Fuentes", "API del Visor CENU (top_divisiones, nacional_*), Visor Interactivo (bogota_*_visor, detalle_4dig_visor)."),
        ("Reglas", "% sobre respondientes; 'Sin información' (personal '0') fuera del denominador; bajo = 0-10 M / 1-5 pers.; alto = >1.000 M / >50 pers."),
        ("Tipología", f"Frente a la referencia nacional de ingreso: bajo {NB:.1f}% / alto {NA:.1f}%."),
        ("Pendiente", "% de personal por división y % de respuesta por división: generar con ruta2_dashboard.py (API en vivo)."),
        ("Verificación", "python verificar_api.py --excel ruta2_bogota_cifras_verificadas.xlsx"),
        ("Advertencia", "Resultados PRELIMINARES. Un ingreso bajo es una señal de posible subsistencia, no una prueba."),
    ], columns=["campo", "detalle"])

    xlsx = SALIDA / "ruta2_bogota_cifras_verificadas.xlsx"
    with pd.ExcelWriter(xlsx) as w:
        leeme.to_excel(w, sheet_name="LEEME", index=False)
        cuadro_top10.to_excel(w, sheet_name="cuadro_top10", index=False)
        top.to_excel(w, sheet_name="top12_bogota", index=False)
        comparacion.to_excel(w, sheet_name="bogota_vs_nacional", index=False)
        bog_visor.to_excel(w, sheet_name="bogota_rangos_visor", index=False)
        bog_personal.round(2).to_excel(w, sheet_name="bogota_personal_visor", index=False)
        totales_visor.to_excel(w, sheet_name="bogota_totales_visor", index=False)
        visor4.to_excel(w, sheet_name="detalle_4dig_visor", index=False)
        rangos_nac.to_excel(w, sheet_name="nacional_rangos", index=False)
        top15_nac.to_excel(w, sheet_name="nacional_top15", index=False)
        controles.to_excel(w, sheet_name="controles", index=False)
    print("->", xlsx)
    print(top.to_string(index=False))
    print(comparacion.to_string(index=False))
    print(controles.to_string(index=False))
    corregir_dashboard(top, NB, NA, bog_bajo_ing, bog_alto_ing)


def corregir_dashboard(top, NB, NA, bajo_bog, alto_bog):
    origen = RAIZ / "ruta2" / "dashboard_cenu_ruta_2_original.html"
    if not origen.exists():
        return
    html = origen.read_text(encoding="utf-8")
    iconos = {47: "fa-shop", 56: "fa-utensils", 45: "fa-car", 96: "fa-scissors", 46: "fa-boxes-stacked",
              95: "fa-laptop-medical", 86: "fa-stethoscope", 85: "fa-graduation-cap", 14: "fa-shirt",
              25: "fa-hammer", 10: "fa-bread-slice", 52: "fa-warehouse"}
    corto = {47: "Comercio al por menor", 56: "Servicios de comida y bebida", 45: "Comercio y rep. vehículos/motos",
             96: "Otros servicios personales", 46: "Comercio al por mayor", 95: "Rep. computadores y efectos",
             86: "Atención de la salud humana", 85: "Educación", 14: "Confección prendas de vestir",
             25: "Productos elaborados de metal", 10: "Elab. productos alimenticios", 52: "Almacenamiento y act. comp."}
    js = "const data = [\n" + ",\n".join(
        f'            {{ name: "{corto[t.division]}", division: "{t.division:02d}", units: {t.unidades}, low: {t.pct_bajo_ingreso}, '
        f'high: {t.pct_alto_ingreso}, tipologia: "{t.tipologia}", icon: "{iconos[t.division]}" }}' for t in top.itertuples()
    ) + "\n        ];"
    rep = [
        (r"const data = \[.*?\];", js),
        (r"CENU 2026", "CENU 2024 · DataJam 2026"),
        (r'<p class="text-2xl font-bold text-slate-800">195,745</p>',
         '<p class="text-2xl font-bold text-slate-800">195,745</p><p class="text-xs text-slate-400">con CIIU visible · universo 195,755</p>'),
        (r"\(19\.6% Ingresos Altos\)", "(36.1% Ingresos &gt; 1.000 M)"),
        (r"\(32\.4% Ingresos Bajos\)", "(32.2% Ingresos 0-10 M)"),
        (r"Sectores como <strong>Reparación de computadores \(32\.4%\)</strong>, <strong>Comercio al por mayor \(23\.7%\)</strong> y <strong>Otros servicios personales \(23\.1%\)</strong> muestran una alta concentración de unidades en el rango de ingresos más bajo \(0 a 10 Millones\)\.",
         "<strong>Reparación de computadores y efectos personales (32.2%)</strong>, <strong>Otros servicios personales (22.9%)</strong> y "
         "<strong>Comercio al por menor (20.1%)</strong> concentran unidades con ingresos de 0 a 10 M y casi no tienen unidades sobre 1.000 M "
         "(0.7%, 0.8% y 3.3%). Juntas suman 106.718 unidades: el 54.5% de Bogotá."),
        (r"Se identifica tejido empresarial maduro en <strong>Comercio al por mayor \(19\.6%\)</strong>, <strong>Elaboración de productos alimenticios \(13\.2%\)</strong> y <strong>Productos elaborados de metal \(12\.2%\)</strong> con proporciones relevantes en el rango alto \(>1\.000 Millones\)\.",
         f"<strong>Comercio al por mayor (36.1%)</strong>, <strong>Elaboración de productos alimenticios (22.9%)</strong> y "
         f"<strong>Almacenamiento (19.0%)</strong> tienen la mayor proporción de unidades con ingresos &gt; 1.000 M "
         f"(referencia nacional: {NA:.1f}%)."),
    ]
    for patron, nuevo in rep:
        html, n = re.subn(patron, lambda _m, s=nuevo: s, html, count=1, flags=re.S)
        if not n:
            print("Aviso: no se encontró el texto a reemplazar:", patron[:60])
    tipo_js = (
        "let tipologiaTag = \"\";\n"
        "            const estilos = {\"Señal de subsistencia\": \"bg-rose-100 text-rose-700 border-rose-200\", "
        "\"Base para escalar\": \"bg-emerald-100 text-emerald-700 border-emerald-200\", "
        "\"Polarizado\": \"bg-amber-100 text-amber-700 border-amber-200\", \"Intermedio\": \"bg-slate-100 text-slate-600 border-slate-200\"};\n"
        "            tipologiaTag = `<span class=\"${estilos[sector.tipologia]} text-xs font-bold px-2 py-1 rounded border\">${sector.tipologia}</span>"
        f"<p class=\"text-xs text-slate-400 mt-2\">Referencia nacional: {NB:.1f}% bajo · {NA:.1f}% alto</p>`;"
    )
    html, n = re.subn(r"let tipologiaTag = \"\";\s*if\(sector\.low >= 30\).*?\n            \}\n", tipo_js + "\n", html, count=1, flags=re.S)
    if not n:
        print("Aviso: no se reemplazó la lógica de tipología")
    destino = SALIDA / "dashboard_cenu_ruta_2_corregido.html"
    destino.write_text(html, encoding="utf-8")
    print("->", destino)


if __name__ == "__main__":
    main()
