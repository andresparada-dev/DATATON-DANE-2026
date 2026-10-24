#!/usr/bin/env python3
"""Construye ruta2/salidas/dashboard_ruta2_final.html: dashboard único de la Ruta 2 (Bogotá), alineado con la rúbrica.

Insumos (todos ya verificados):
  · ruta2/insumos/dashboard_data_api.js       → salida de ruta2_dashboard.py en Colab (API, por división)
  · data/ruta2/api_nacional_sectoral_reference_2023.json → API granularity="country"
  · Visor Interactivo CENU (Bogotá): distribuciones agregadas de ingreso y personal, promedio y total de ingresos
Chart.js 4.4.1 va incrustado (sin CDN): el archivo funciona sin internet y se puede pegar en Google Sites.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent
RAIZ = R.parent

UNIVERSO, CON_CIIU = 195_755, 195_745
SECTORES = [("Comercio", 112_016), ("Servicios", 68_420), ("Industria", 10_510), ("Transporte", 3_120), ("Construcción", 1_679)]
RANGOS_ING = ["0 - 10 M", "11 - 50 M", "51 - 100 M", "101 - 500 M", "501 - 1.000 M", "1.001 - 5.000 M",
              "5.001 - 10.000 M", "10.001 - 100.000 M", "> 100.000 M"]
BOG_ING = [17.4, 32.4, 16.0, 19.9, 3.8, 5.2, 1.7, 3.1, 0.7]               # Visor, % unidades que reportaron
RANGOS_PER = ["1 - 5", "6 - 10", "11 - 20", "21 - 50", "51 - 100", "101 - 500", "501+"]
BOG_PER_TOTAL = [80.4, 7.0, 3.5, 2.6, 1.4, 1.6, 0.6]                       # Visor, % del total (2,9 % sin información)
BOG_SIN_INFO_PER = 2.9
ING_PROM_BOG, ING_TOTAL_BOG_MILLONES = 7_422, 1_180_444_620
# Agente de voz ElevenLabs (requiere internet; el resto del dashboard funciona sin conexión)
AGENTE_VOZ = """<!-- Asistente de voz · ElevenLabs Conversational AI -->
<elevenlabs-convai agent-id="agent_5901m5q8fk19fzbsy4zh3d8ngcx4"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>"""


def leer_divisiones():
    js = (R / "insumos" / "dashboard_data_api.js").read_text(encoding="utf-8")
    filas = []
    for obj in re.findall(r"\{(.*?)\}", js, flags=re.S):
        def g(k):
            m = re.search(rf'\b{k}: "([^"]*)"', obj) or re.search(rf'\b{k}: ([^,\s}}]+)', obj)
            return m.group(1)
        filas.append({"div": g("division"), "name": g("name"), "units": int(g("units")), "low": float(g("low")),
                      "high": float(g("high")), "lowP": float(g("lowPers")), "highP": float(g("highPers")),
                      "tipo": g("tipologia")})
    return filas


def main():
    nac = json.loads((RAIZ / "data" / "ruta2" / "api_nacional_sectoral_reference_2023.json").read_text())
    ing = nac["total_income_2023"]["values"]
    tot_i = sum(v["value"] for v in ing)
    nac_ing = [round(100 * v["value"] / tot_i, 2) for v in ing]
    per = [v for v in nac["total_employed_personnel"]["values"] if v["code"] != "0"]
    tot_p = sum(v["value"] for v in per)
    nac_per = [round(100 * v["value"] / tot_p, 2) for v in per]
    bog_per = [round(100 * x / (100 - BOG_SIN_INFO_PER), 2) for x in BOG_PER_TOTAL]
    nac_prom = nac["total_income_2023"]["average"] / 1e6
    nac_total_millones = nac["total_income_2023"]["total_value"] / 1e6
    tc_nac = nac["ciiu_division"]["total_count"]

    divs = leer_divisiones()
    for d in divs:
        d["pct"] = round(100 * d["units"] / CON_CIIU, 1)
        d["mid"] = round(100 - d["low"] - d["high"], 1)
        d["midP"] = round(100 - d["lowP"] - d["highP"], 1)
    top10_pct = round(100 * sum(d["units"] for d in divs[:10]) / CON_CIIU, 1)

    datos = {
        "divs": divs, "rangosIng": RANGOS_ING, "bogIng": BOG_ING, "nacIng": nac_ing,
        "rangosPer": RANGOS_PER, "bogPer": bog_per, "nacPer": nac_per,
        "sectores": [{"s": s, "u": u, "pct": round(100 * u / CON_CIIU, 1)} for s, u in SECTORES],
        "refBajo": round(nac_ing[0], 1), "refAlto": round(sum(nac_ing[5:]), 1),
        "comp": {"bog": [BOG_ING[0], round(sum(BOG_ING[5:]), 1), round(bog_per[0], 1), round(sum(bog_per[4:]), 1)],
                 "nac": [round(nac_ing[0], 1), round(sum(nac_ing[5:]), 1), round(nac_per[0], 1), round(sum(nac_per[4:]), 1)]},
    }
    k = {
        "UNIVERSO": f"{UNIVERSO:,}".replace(",", "."), "CON_CIIU": f"{CON_CIIU:,}".replace(",", "."),
        "COMERCIO": f"{100 * SECTORES[0][1] / CON_CIIU:.1f}".replace(".", ","),
        "TOP10": f"{top10_pct:.1f}".replace(".", ","),
        "BOG_BAJO": "17,4", "NAC_BAJO": f"{nac_ing[0]:.1f}".replace(".", ","),
        "BOG_ALTO": f"{sum(BOG_ING[5:]):.1f}".replace(".", ","), "NAC_ALTO": f"{sum(nac_ing[5:]):.1f}".replace(".", ","),
        "PROM_BOG": f"{ING_PROM_BOG:,}".replace(",", "."), "PROM_NAC": f"{nac_prom:,.0f}".replace(",", "."),
        "PESO_ING": f"{100 * ING_TOTAL_BOG_MILLONES / nac_total_millones:.1f}".replace(".", ","),
        "PESO_UNI": f"{100 * CON_CIIU / tc_nac:.1f}".replace(".", ","),
        "BOG_P15": f"{bog_per[0]:.1f}".replace(".", ","), "NAC_P15": f"{nac_per[0]:.1f}".replace(".", ","),
    }
    for plantilla, salida in (("plantilla_dashboard_final.html", "dashboard_ruta2_final.html"),
                              ("plantilla_dashboard_oscuro.html", "dashboard_ruta2_oscuro.html")):
        html = (R / plantilla).read_text(encoding="utf-8")
        html = html.replace("__DATOS__", json.dumps(datos, ensure_ascii=False))
        for clave, val in k.items():
            html = html.replace(f"__{clave}__", val)
        css = R / "vendor" / "tailwind_oscuro.css"   # npx tailwindcss --content plantilla_dashboard_oscuro.html --minify
        html = html.replace("__TAILWIND__", css.read_text(encoding="utf-8") if css.exists() else "")
        html = html.replace("__AGENTE_VOZ__", AGENTE_VOZ)
        html = html.replace("__CHARTJS__", (R / "vendor" / "chart.umd.4.4.1.js").read_text(encoding="utf-8"))
        pendientes = re.findall(r"__[A-Z0-9_]+__", html)
        assert not pendientes, pendientes
        dest = R / "salidas" / salida
        dest.write_text(html, encoding="utf-8")
        print("->", dest, f"({dest.stat().st_size / 1024:.0f} KB)")
    print(json.dumps({x: datos[x] for x in ("nacIng", "bogPer", "nacPer", "refBajo", "refAlto")}, ensure_ascii=False))
    print(k)


if __name__ == "__main__":
    main()
