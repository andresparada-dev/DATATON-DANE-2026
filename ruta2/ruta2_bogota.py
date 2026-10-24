#!/usr/bin/env python3
"""DataJam CENU 2026 · RUTA 2 — "Economía real del territorio: sectores, empleo e ingresos" · BOGOTÁ D.C.

Uso en Google Colab (una celda):
    !wget -q https://raw.githubusercontent.com/andresparada-dev/DATATON-DANE-2026/main/ruta2/ruta2_bogota.py
    !python ruta2_bogota.py
o local:  python ruta2/ruta2_bogota.py   [--top 12] [--municipio 11001] [--debug]

Hace lo que pide la Ruta 2:
  1) Unidades por división CIIU (variable ciiu_division, módulo sectoral_reference_2023) en Bogotá.
  2) Para las N divisiones con más unidades: distribución por rangos de total_income_2023 y
     total_employed_personnel (filtrando variable_filters.ciiu_division).
  3) % por rango sobre los que RESPONDIERON + % de respuesta + unidades sin dato.
  4) Indicadores: % rangos bajos (ingreso 0-10 M; 0-5 personas) y % rangos altos (ingreso >1.000 M; >50 personas).
  5) Top 10, por gran sector, gráfico de barras apiladas y recomendación de política (borrador).
Salida: ruta2_resultados.xlsx (cuadro_top, rangos_detalle, divisiones, por_sector, clasificacion_rangos)
        ruta2_barras_ingreso.png, ruta2_barras_personal.png, ruta2_resumen.md, ruta2_respuestas_api.json

Si la API cambia el formato, correr con --debug y ajustar PAYLOAD_BASE / LLAVES_* abajo.
Resultados PRELIMINARES del CENU: decirlo en la presentación.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests

BASE = "https://censoeconomiconacionalurbano.dane.gov.co/backend"
MODULO = "sectoral_reference_2023"
BOGOTA = "11001"          # DIVIPOLA municipio Bogotá D.C. (departamento 11)

# ---------------------------------------------------------------- CIIU Rev. 4 A.C. — divisiones
DIVISIONES = {
    1: "Agricultura, ganadería, caza", 2: "Silvicultura y extracción de madera", 3: "Pesca y acuicultura",
    5: "Extracción de carbón", 6: "Extracción de petróleo y gas", 7: "Extracción de minerales metalíferos",
    8: "Extracción de otras minas y canteras", 9: "Apoyo a la explotación de minas",
    10: "Elaboración de productos alimenticios", 11: "Elaboración de bebidas", 12: "Productos de tabaco",
    13: "Fabricación de productos textiles", 14: "Confección de prendas de vestir", 15: "Cuero y calzado",
    16: "Transformación de la madera", 17: "Papel y cartón", 18: "Actividades de impresión",
    19: "Coque y refinación de petróleo", 20: "Sustancias y productos químicos", 21: "Productos farmacéuticos",
    22: "Productos de caucho y plástico", 23: "Otros minerales no metálicos", 24: "Metalúrgicas básicas",
    25: "Productos elaborados de metal", 26: "Productos informáticos, electrónicos y ópticos",
    27: "Aparatos y equipo eléctrico", 28: "Maquinaria y equipo n.c.p.", 29: "Vehículos automotores",
    30: "Otros tipos de equipo de transporte", 31: "Fabricación de muebles", 32: "Otras industrias manufactureras",
    33: "Instalación, mantenimiento y reparación de maquinaria", 35: "Electricidad, gas y vapor",
    36: "Captación y suministro de agua", 37: "Evacuación de aguas residuales", 38: "Gestión de desechos",
    39: "Saneamiento ambiental", 41: "Construcción de edificios", 42: "Obras de ingeniería civil",
    43: "Actividades especializadas de construcción", 45: "Comercio y reparación de vehículos y motos",
    46: "Comercio al por mayor", 47: "Comercio al por menor", 49: "Transporte terrestre",
    50: "Transporte acuático", 51: "Transporte aéreo", 52: "Almacenamiento y actividades complementarias",
    53: "Correo y mensajería", 55: "Alojamiento", 56: "Servicios de comida y bebida",
    58: "Edición", 59: "Cine, video, TV y música", 60: "Programación y transmisión",
    61: "Telecomunicaciones", 62: "Desarrollo de software y consultoría TI", 63: "Servicios de información",
    64: "Servicios financieros", 65: "Seguros y pensiones", 66: "Actividades auxiliares financieras",
    68: "Actividades inmobiliarias", 69: "Actividades jurídicas y de contabilidad",
    70: "Administración empresarial y consultoría de gestión", 71: "Arquitectura e ingeniería; ensayos técnicos",
    72: "Investigación científica y desarrollo", 73: "Publicidad y estudios de mercado",
    74: "Otras actividades profesionales y técnicas", 75: "Actividades veterinarias",
    77: "Alquiler y arrendamiento", 78: "Actividades de empleo", 79: "Agencias de viajes y turismo",
    80: "Seguridad e investigación privada", 81: "Servicios a edificios y paisajismo",
    82: "Actividades administrativas y de apoyo de oficina", 84: "Administración pública y defensa",
    85: "Educación", 86: "Atención de la salud humana", 87: "Atención residencial medicalizada",
    88: "Asistencia social sin alojamiento", 90: "Actividades creativas, artísticas y de entretenimiento",
    91: "Bibliotecas, archivos y museos", 92: "Juegos de azar y apuestas", 93: "Actividades deportivas y recreativas",
    94: "Asociaciones", 95: "Reparación de computadores y efectos personales",
    96: "Otros servicios personales (peluquería, lavandería...)", 97: "Hogares como empleadores",
    98: "Hogares productores para uso propio", 99: "Organizaciones extraterritoriales",
}


def gran_sector(div: int) -> str:
    if div <= 9:
        return "Agro y minería"
    if div <= 39:
        return "Industria"
    if div <= 43:
        return "Construcción"
    if div <= 47:
        return "Comercio"
    return "Servicios"


# ---------------------------------------------------------------- utilidades
def _norm(t) -> str:
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()


def es_sin_dato(desc) -> bool:
    d = _norm(desc)
    return any(k in d for k in ("sin informacion", "sin clasificar", "no informa", "no sabe", "no responde", "sin dato",
                                "no aplica", "ns/nr", "sin respuesta"))


def limites(desc) -> tuple[float, float]:
    """(inferior, superior) numérico de un rango leído desde su descripción. Ingreso se lleva a MILLONES."""
    d = _norm(desc)
    nums = [float(x.replace(".", "").replace(",", ".")) for x in re.findall(r"\d[\d.,]*", d)]
    if not nums:
        return (float("nan"), float("nan"))
    escala = 1.0
    if "mil millones" in d or "mm" in d.split():
        escala = 1000.0
    elif "millon" in d:
        escala = 1.0
    elif max(nums) >= 100_000:          # viene en pesos
        escala = 1e-6
    nums = [n * escala for n in nums]
    if any(k in d for k in ("mas de", "mayor", "superior", "o mas", "y mas", ">")):
        return (nums[0], float("inf")) if len(nums) == 1 else (nums[0], nums[-1])
    if any(k in d for k in ("menos de", "hasta", "menor", "<")) and len(nums) == 1:
        return (0.0, nums[0])
    return (nums[0], nums[-1])


def clasificar_rango(desc, variable: str) -> str:
    """bajo / medio / alto / sin_dato según los umbrales de la guía (ingreso 10 M y 1.000 M; personal 5 y 50)."""
    if es_sin_dato(desc):
        return "sin_dato"
    lo, hi = limites(desc)
    if variable == "ingreso":
        bajo_max, alto_min = 10.0, 1000.0
    else:
        bajo_max, alto_min = 5.0, 50.0
    if hi == hi and hi <= bajo_max + 1e-9:
        return "bajo"
    if lo == lo and lo >= alto_min - 1e-9 and lo > bajo_max:
        return "alto"
    return "medio"


# ---------------------------------------------------------------- cliente API
class CENU:
    def __init__(self, base=BASE, debug=False):
        self.base, self.debug = base.rstrip("/"), debug
        self.s = requests.Session()
        self.s.headers.update({"Accept": "application/json", "Content-Type": "application/json",
                               "User-Agent": "datajam-cenu-2026-ruta2"})
        self.payload_ok = None
        self.log = []

    def get(self, ruta, **params):
        r = self.s.get(f"{self.base}/{ruta.lstrip('/')}", params=params, timeout=90)
        r.raise_for_status()
        return r.json()

    def post(self, ruta, body):
        for intento in range(4):
            try:
                r = self.s.post(f"{self.base}/{ruta.lstrip('/')}", json=body, timeout=120)
                if r.status_code in (429, 502, 503, 504):
                    time.sleep(2 ** (intento + 1))
                    continue
                return r
            except requests.RequestException:
                time.sleep(2 ** (intento + 1))
        raise RuntimeError(f"La API no respondió a {ruta} (¿saturada? usar respaldo CSV del equipo DICE)")

    def openapi_schema(self):
        """Imprime el esquema del body de /structural/general (para verificar nombres de campos)."""
        try:
            spec = self.get("openapi.json")
        except Exception as e:  # noqa: BLE001
            print("No se pudo leer openapi.json:", e)
            return None
        op = spec.get("paths", {}).get("/structural/general", {}).get("post", {})
        ref = (op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}))
        comps = spec.get("components", {}).get("schemas", {})

        def resolver(s, prof=0):
            if prof > 4 or not isinstance(s, dict):
                return s
            if "$ref" in s:
                return resolver(comps.get(s["$ref"].split("/")[-1], {}), prof + 1)
            return {k: (resolver(v, prof + 1) if isinstance(v, dict) else
                        [resolver(x, prof + 1) for x in v] if isinstance(v, list) else v) for k, v in s.items()}

        esquema = resolver(ref)
        if self.debug:
            print(json.dumps(esquema, ensure_ascii=False, indent=1)[:4000])
        return esquema

    def estructural(self, variables, filtros=None, granularidad="country", municipio=BOGOTA):
        """POST /structural/general probando variantes hasta obtener datos; recuerda la que funcionó."""
        filtros = dict(filtros or {})
        variantes = []
        for mid in ([municipio], [int(municipio)]):
            for gran in (granularidad, "municipality"):
                for mod_key in ("module", "module_name", None):
                    body = {"granularity": gran, "variables": variables,
                            "variable_filters": {"municipality_ids": mid, **filtros}}
                    if mod_key:
                        body[mod_key] = MODULO
                    variantes.append(body)
        if self.payload_ok:
            ok = json.loads(json.dumps(self.payload_ok))
            ok["variables"] = variables
            ok["variable_filters"] = {"municipality_ids": ok["variable_filters"]["municipality_ids"], **filtros}
            variantes.insert(0, ok)
        ultimo = None
        for body in variantes:
            r = self.post("structural/general", body)
            ultimo = (r.status_code, r.text[:500])
            if r.ok:
                j = r.json()
                filas = extraer_categorias(j)
                if filas:
                    if self.payload_ok is None:
                        print("Payload que funciona:", json.dumps(body, ensure_ascii=False))
                    self.payload_ok = body
                    self.log.append({"body": body, "respuesta": j})
                    return filas
            elif self.debug:
                print(r.status_code, json.dumps(body, ensure_ascii=False), r.text[:300])
        raise RuntimeError(f"Ninguna variante de payload funcionó. Última respuesta: {ultimo}. "
                           "Correr con --debug y revisar el esquema impreso.")


def extraer_categorias(j, variable=None) -> list[dict]:
    """Recorre la respuesta y devuelve [{variable, code, description, value}] de los objetos con code+value."""
    genericos = {"data", "results", "result", "values", "categories", "items", "rows", "response"}
    salida = []

    def walk(x, var):
        if isinstance(x, dict):
            if {"code", "value"} <= set(x) and not isinstance(x["value"], (dict, list)):
                salida.append({"variable": var, "code": x.get("code"),
                               "description": x.get("description", x.get("label", x.get("code"))), "value": x["value"]})
                return
            propio = x.get("variable") or x.get("variable_name") or x.get("name")
            var = propio if isinstance(propio, str) else var
            for k, val in x.items():
                if isinstance(val, (dict, list)):
                    walk(val, var if k in genericos else k if var is None or k.endswith(("_2023", "_division", "personnel")) else var)
        elif isinstance(x, list):
            for e in x:
                walk(e, var)

    walk(j, variable)
    for f in salida:
        try:
            f["value"] = float(f["value"])
        except (TypeError, ValueError):
            f["value"] = float("nan")
    return salida


# ---------------------------------------------------------------- análisis
def distribucion(api: CENU, variable_api: str, etiqueta: str, division) -> pd.DataFrame:
    filas = api.estructural([variable_api], {"ciiu_division": [division]})
    df = pd.DataFrame(filas)
    # si la respuesta también trae la variable del filtro (ciiu_division), se descarta
    no_ciiu = ~df["variable"].astype(str).str.contains("ciiu", case=False)
    if no_ciiu.any():
        df = df[no_ciiu]
    df["variable"] = etiqueta
    df["clase"] = df["description"].map(lambda d: clasificar_rango(d, etiqueta))
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--municipio", default=BOGOTA)
    ap.add_argument("--top", type=int, default=12, help="divisiones a detallar (10-15)")
    ap.add_argument("--salida", default=".")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)

    api = CENU(debug=a.debug)
    api.openapi_schema()
    try:
        print("Universos por módulo:", json.dumps(api.get("modules-universes"), ensure_ascii=False)[:600])
    except Exception as e:  # noqa: BLE001
        print("modules-universes no disponible:", e)

    # 1) Unidades por división CIIU
    divs = pd.DataFrame(api.estructural(["ciiu_division"]))
    divs = divs[~divs["description"].map(es_sin_dato)] if divs["description"].notna().any() else divs
    divs["division"] = pd.to_numeric(divs["code"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
    sin_div = divs[divs["division"].isna()]
    divs = divs.dropna(subset=["division"]).astype({"division": int})
    divs["nombre"] = divs["division"].map(DIVISIONES).fillna(divs["description"])
    divs["gran_sector"] = divs["division"].map(gran_sector)
    divs = divs.groupby(["division", "nombre", "gran_sector"], as_index=False)["value"].sum().rename(columns={"value": "unidades"})
    total = divs["unidades"].sum()
    divs["pct_unidades"] = 100 * divs["unidades"] / total
    divs = divs.sort_values("unidades", ascending=False, ignore_index=True)
    print(f"\nBogotá: {total:,.0f} unidades con división CIIU en {len(divs)} divisiones "
          f"(sin división válida: {sin_div['value'].sum():,.0f})")
    por_sector = divs.groupby("gran_sector", as_index=False)["unidades"].sum()
    por_sector["pct"] = 100 * por_sector["unidades"] / total
    por_sector = por_sector.sort_values("unidades", ascending=False)

    # 2) Rangos de ingreso y personal para las top N divisiones
    detalle, resumen = [], []
    for _, d in divs.head(a.top).iterrows():
        cod = int(d["division"])
        fila = {"division": cod, "nombre": d["nombre"], "gran_sector": d["gran_sector"], "unidades": d["unidades"]}
        for var_api, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
            dist = None
            for codigo in (f"{cod:02d}", str(cod), cod):
                try:
                    dist = distribucion(api, var_api, etq, codigo)
                    if len(dist):
                        break
                except RuntimeError:
                    continue
            if dist is None or dist.empty:
                print(f"  ! sin datos de {etq} para división {cod}")
                continue
            resp = dist.loc[dist["clase"] != "sin_dato", "value"].sum()
            sin = dist.loc[dist["clase"] == "sin_dato", "value"].sum()
            # unidades sin dato = unidades de la división − las que respondieron (regla de la guía)
            sin_dato = max(d["unidades"] - resp, 0)
            dist = dist.assign(division=cod, nombre=d["nombre"],
                               pct_sobre_respondientes=lambda x: 100 * x["value"] / resp if resp else float("nan"))
            dist.loc[dist["clase"] == "sin_dato", "pct_sobre_respondientes"] = float("nan")
            detalle.append(dist)
            fila[f"respondieron_{etq}"] = resp
            fila[f"pct_respuesta_{etq}"] = 100 * resp / d["unidades"] if d["unidades"] else float("nan")
            fila[f"sin_dato_{etq}"] = sin_dato
            fila[f"pct_bajo_{etq}"] = 100 * dist.loc[dist["clase"] == "bajo", "value"].sum() / resp if resp else float("nan")
            fila[f"pct_alto_{etq}"] = 100 * dist.loc[dist["clase"] == "alto", "value"].sum() / resp if resp else float("nan")
        resumen.append(fila)
        print(f"  {cod:02d} {d['nombre'][:45]:45s} {d['unidades']:>9,.0f}  "
              f"bajo ing {fila.get('pct_bajo_ingreso', float('nan')):5.1f}%  alto ing {fila.get('pct_alto_ingreso', float('nan')):5.1f}%")

    cuadro = pd.DataFrame(resumen)
    rangos = pd.concat(detalle, ignore_index=True) if detalle else pd.DataFrame()
    cuadro["tipologia"] = cuadro.apply(tipologia, axis=1)
    top10 = cuadro.head(10).copy()
    clasif = (rangos[["variable", "code", "description", "clase"]].drop_duplicates().sort_values(["variable", "code"])
              if len(rangos) else pd.DataFrame())

    # 3) Excel + gráficos + resumen
    xlsx = out / "ruta2_resultados.xlsx"
    with pd.ExcelWriter(xlsx) as w:
        top10.round(2).to_excel(w, sheet_name="cuadro_top", index=False)
        rangos.round(2).to_excel(w, sheet_name="rangos_detalle", index=False)
        divs.round(2).to_excel(w, sheet_name="divisiones", index=False)
        por_sector.round(2).to_excel(w, sheet_name="por_sector", index=False)
        clasif.to_excel(w, sheet_name="clasificacion_rangos", index=False)
    (out / "ruta2_respuestas_api.json").write_text(json.dumps(api.log, ensure_ascii=False)[:20_000_000])
    graficar(rangos, top10, "ingreso", out / "ruta2_barras_ingreso.png")
    graficar(rangos, top10, "personal", out / "ruta2_barras_personal.png")
    escribir_resumen(out / "ruta2_resumen.md", total, divs, por_sector, top10)
    print(f"\nListo: {xlsx}\n       {out / 'ruta2_barras_ingreso.png'}\n       {out / 'ruta2_resumen.md'}")
    print("REVISAR la hoja clasificacion_rangos: confirma que cada rango quedó como bajo/medio/alto correctamente.")


def tipologia(f) -> str:
    bi, ai = f.get("pct_bajo_ingreso", float("nan")), f.get("pct_alto_ingreso", float("nan"))
    bp, apr = f.get("pct_bajo_personal", float("nan")), f.get("pct_alto_personal", float("nan"))
    if bi == bi and bi >= 70 and (bp != bp or bp >= 80):
        return "Señal de subsistencia (mayoría en rangos bajos)"
    if (ai == ai and ai >= 5) or (apr == apr and apr >= 3):
        return "Con base para escalar (proporción relevante en rangos altos)"
    return "Mixto / intermedio"


def graficar(rangos: pd.DataFrame, top10: pd.DataFrame, etq: str, ruta: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    if rangos.empty:
        return
    r = rangos[(rangos["variable"] == etq) & (rangos["clase"] != "sin_dato") & rangos["division"].isin(top10["division"])]
    if r.empty:
        return
    orden_cat = (r.groupby(["code", "description"])["value"].sum().reset_index()
                 .assign(lo=lambda x: x["description"].map(lambda d: limites(d)[0])).sort_values("lo"))
    piv = r.pivot_table(index="division", columns="description", values="pct_sobre_respondientes", aggfunc="sum").fillna(0)
    piv = piv[[c for c in orden_cat["description"] if c in piv.columns]]
    piv = piv.reindex(top10["division"][::-1])
    piv.index = [f"{d:02d} {DIVISIONES.get(d, '')[:38]}" for d in piv.index]
    n = piv.shape[1]
    azules = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#104281", "#0d366b"]
    colores = [azules[int(i * (len(azules) - 1) / max(n - 1, 1))] for i in range(n)]
    fig, ax = plt.subplots(figsize=(11, 0.5 * len(piv) + 2))
    izq = [0.0] * len(piv)
    for c, col in zip(piv.columns, colores):
        ax.barh(piv.index, piv[c], left=izq, color=col, edgecolor="white", linewidth=1.5, label=str(c)[:30])
        izq = [a + b for a, b in zip(izq, piv[c])]
    ax.set_xlim(0, 100)
    ax.set_xlabel("% de unidades que respondieron")
    titulo = "ingresos 2023" if etq == "ingreso" else "personal ocupado"
    ax.set_title(f"Bogotá D.C. — Top 10 divisiones CIIU por rango de {titulo} (CENU, preliminar)", loc="left",
                 fontweight="bold")
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", frameon=False, fontsize=8, title="Rango (de menor a mayor)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def escribir_resumen(ruta: Path, total, divs, por_sector, top10):
    L = [f"# Ruta 2 · Bogotá D.C. — Sectores, empleo e ingresos (CENU, resultados PRELIMINARES)\n",
         f"- Unidades económicas con división CIIU: **{total:,.0f}**",
         "- Por gran sector: " + "; ".join(f"{r.gran_sector} {r.pct:.1f}%" for r in por_sector.itertuples()),
         "- Top 3 divisiones: " + "; ".join(f"{r.division:02d} {r.nombre} ({r.pct_unidades:.1f}%)" for r in divs.head(3).itertuples()),
         "\n## Cuadro top 10\n", top10.round(1).to_string(index=False), "\n## Lectura"]
    if "pct_bajo_ingreso" in top10:
        sub = top10.sort_values("pct_bajo_ingreso", ascending=False).iloc[0]
        esc = top10.sort_values("pct_alto_ingreso", ascending=False).iloc[0]
        L += [f"- Mayor señal de subsistencia: **{sub['nombre']}**: {sub['pct_bajo_ingreso']:.1f}% de las que respondieron "
              f"ingresó 0–10 M en 2023 (respuesta {sub['pct_respuesta_ingreso']:.0f}%).",
              f"- Mayor potencial de escalamiento: **{esc['nombre']}**: {esc['pct_alto_ingreso']:.1f}% con ingresos > 1.000 M.",
              "- Rangos bajos = SEÑAL de posible subsistencia/informalidad, no prueba.",
              "- % calculados sobre las unidades que respondieron; se reporta aparte el % de respuesta."]
    ruta.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
