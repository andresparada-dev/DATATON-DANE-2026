#!/usr/bin/env python3
"""Genera ruta2/Ruta2_Bogota_CENU.ipynb: notebook autónomo de entrega (Colab o Jupyter), sin dependencias del repo."""

from pathlib import Path

import nbformat as nbf

C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s.strip()))  # noqa: E731
code = lambda s: C.append(nbf.v4.new_code_cell(s.strip()))  # noqa: E731

md("""
# DataJam CENU 2026 · Ruta 2 — Economía real del territorio: sectores, empleo e ingresos
**Territorio:** Bogotá D.C. (DIVIPOLA 11001) · **Equipo:** [nombre del equipo] · **Integrantes:** [nombres]

**Pregunta reto:** ¿Cómo se distribuye la actividad económica en Bogotá? ¿Dónde hay más oportunidades para emprender?

**Fuente:** API del Visor Interactivo del CENU 2024 (DANE), `POST /api/v1/structural/general`, módulo `sectoral_reference_2023` (año de referencia 2023). **Resultados preliminares.**

**Reglas de la guía aplicadas**
1. Universo del módulo reportado (`/structural/modules-universes`).
2. Porcentajes sobre las unidades que **respondieron**; "Sin información" (en personal, el rango `"0"`, rotulado en el Visor como *Sin información reportada*) es **no respuesta** y sale del denominador. El % de respuesta y las unidades sin dato se reportan aparte.
3. Filtros por territorio (`municipality_ids`) y por actividad (`variable_filters.ciiu_division`).
4. Ingreso y personal se leen **como rangos** (no se suman pesos ni personas).
5. Bajo = ingreso 0–10 M / 1–5 personas · Alto = ingreso > 1.000 M / > 50 personas.
6. Regla de supresión: no se publican municipios con menos de 30 unidades; algunos CIIU no son visibles por reserva estadística.
""")

code("""
import json, re, time
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE = "https://censoeconomiconacionalurbano.dane.gov.co/backend/api/v1"
MODULO = "sectoral_reference_2023"
MUNICIPIO = "11001"        # Bogotá D.C.
TOP_N = 12                 # se detallan 12; el cuadro de entrega es el top 10
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
""")

md("## 1. Cliente de la API")
code("""
S = requests.Session()
S.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
LOG = []   # respuestas crudas (trazabilidad)

def post(ruta, body):
    for intento in range(4):                      # reintentos exponenciales (2, 4, 8, 16 s)
        try:
            r = S.post(f"{BASE}/{ruta}", json=body, timeout=120)
            if r.status_code in (429, 502, 503, 504):
                time.sleep(2 ** (intento + 1)); continue
            r.raise_for_status()
            j = r.json(); LOG.append({"body": body, "respuesta": j}); return j
        except requests.RequestException as e:
            if intento == 3: raise
            time.sleep(2 ** (intento + 1))

def buscar_variable(x, var):
    \"\"\"Encuentra {total_count, values} de `var` en la respuesta (municipios -> id -> variables -> var).\"\"\"
    if isinstance(x, dict):
        if isinstance(x.get(var), dict) and "values" in x[var]:
            return x[var]
        for v in x.values():
            r = buscar_variable(v, var)
            if r is not None: return r
    elif isinstance(x, list):
        for v in x:
            r = buscar_variable(v, var)
            if r is not None: return r
    return None

def consultar(variables, filtros=None, municipio=MUNICIPIO, nacional=False):
    \"\"\"Devuelve {variable: {"total_count": n, "values": DataFrame(code, description, value)}}.\"\"\"
    if nacional:
        body = {"module": MODULO, "variables": variables, "granularity": "country"}
    else:
        body = {"module": MODULO, "variables": variables,
                "variable_filters": {"municipality_ids": [municipio], **(filtros or {})}}
    j = post("structural/general", body)
    out = {}
    for var in variables:
        res = buscar_variable(j, var) or {"values": []}
        vals = pd.DataFrame([{   # categóricas: codigo/descripcion/conteo · rangos: code/description/value
            "code": v.get("codigo", v.get("code")),
            "description": v.get("descripcion") or v.get("description") or v.get("codigo", v.get("code")),
            "value": float(v.get("conteo", v.get("value")) or 0)} for v in res.get("values", [])])
        out[var] = {"total_count": res.get("total_count"), "values": vals}
    return out
""")

md("## 2. Reglas: clasificación de rangos y no respuesta")
code("""
def _norm(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\\s+", " ", t).strip()

def es_sin_dato(desc, variable):
    d = _norm(desc)
    if any(k in d for k in ("sin informacion", "sin clasificar", "no informa", "sin dato", "no responde")):
        return True
    return variable == "personal" and d == "0"      # Visor: "Sin información reportada"

def limites(desc):
    \"\"\"(inferior, superior) de un rango en MILLONES ('0 - 10 M', '1.001 - 5.000 M', '> 100.000 M', '501+').\"\"\"
    d = _norm(desc)
    nums = [float(x.replace(".", "").replace(",", ".")) for x in re.findall(r"\\d[\\d.,]*", d)]
    if not nums: return (float("nan"), float("nan"))
    if any(k in d for k in ("mas de", "mayor", ">", "+")):
        return (nums[0], float("inf")) if len(nums) == 1 else (nums[0], nums[-1])
    return (nums[0], nums[-1])

def clase_rango(desc, variable):
    if es_sin_dato(desc, variable): return "sin_dato"
    lo, hi = limites(desc)
    bajo_max, alto_min = (10, 1000) if variable == "ingreso" else (5, 51)
    if hi <= bajo_max: return "bajo"
    if lo >= alto_min: return "alto"
    return "medio"

def indicadores(vals, variable):
    \"\"\"% bajo/medio/alto sobre respondientes, respondientes y sin dato.\"\"\"
    if vals.empty: return {}
    v = vals.assign(clase=vals["description"].map(lambda s: clase_rango(s, variable)))
    resp = v.loc[v.clase != "sin_dato", "value"].sum()
    sin = v.loc[v.clase == "sin_dato", "value"].sum()
    p = lambda c: 100 * v.loc[v.clase == c, "value"].sum() / resp if resp else float("nan")
    return {f"respondieron_{variable}": resp, f"sin_info_{variable}": sin,
            f"pct_bajo_{variable}": p("bajo"), f"pct_medio_{variable}": p("medio"), f"pct_alto_{variable}": p("alto")}

# Prueba rápida de las reglas con los rangos que publica la API
for t in ["0 - 10 M", "501 - 1.000 M", "1.001 - 5.000 M", "10.001 - 100.000 M", "> 100.000 M"]:
    print(f"{t:22s} ingreso  -> {clase_rango(t, 'ingreso')}")
for t in ["0", "1 - 5", "21 - 50", "51 - 100", "501+"]:
    print(f"{t:22s} personal -> {clase_rango(t, 'personal')}")
""")

md("## 3. Clasificación CIIU Rev. 4 A.C. (divisiones) y sectores CENU")
code("""
DIVISIONES = {1:"Agricultura, ganadería, caza",2:"Silvicultura",3:"Pesca y acuicultura",5:"Extracción de carbón",6:"Petróleo y gas",
 7:"Minerales metalíferos",8:"Otras minas y canteras",9:"Apoyo a minería",10:"Elaboración de productos alimenticios",11:"Elaboración de bebidas",
 12:"Tabaco",13:"Productos textiles",14:"Confección de prendas de vestir",15:"Cuero y calzado",16:"Madera",17:"Papel y cartón",
 18:"Impresión",19:"Coque y refinación",20:"Sustancias químicas",21:"Farmacéuticos",22:"Caucho y plástico",23:"Minerales no metálicos",
 24:"Metalúrgicas básicas",25:"Productos elaborados de metal",26:"Informáticos y electrónicos",27:"Equipo eléctrico",28:"Maquinaria n.c.p.",
 29:"Vehículos automotores",30:"Otro equipo de transporte",31:"Muebles",32:"Otras manufacturas",33:"Instalación y reparación de maquinaria",
 35:"Electricidad y gas",36:"Agua",37:"Aguas residuales",38:"Gestión de desechos",39:"Saneamiento",41:"Construcción de edificios",
 42:"Obras civiles",43:"Construcción especializada",45:"Comercio y reparación de vehículos y motos",46:"Comercio al por mayor",
 47:"Comercio al por menor",49:"Transporte terrestre",50:"Transporte acuático",51:"Transporte aéreo",52:"Almacenamiento y actividades complementarias",
 53:"Correo y mensajería",55:"Alojamiento",56:"Servicios de comida y bebida",58:"Edición",59:"Cine, video y música",60:"Programación y transmisión",
 61:"Telecomunicaciones",62:"Software y consultoría TI",63:"Servicios de información",64:"Servicios financieros",65:"Seguros y pensiones",
 66:"Auxiliares financieras",68:"Inmobiliarias",69:"Jurídicas y contabilidad",70:"Consultoría de gestión",71:"Arquitectura e ingeniería",
 72:"Investigación y desarrollo",73:"Publicidad y mercadeo",74:"Otras profesionales",75:"Veterinarias",77:"Alquiler y arrendamiento",
 78:"Actividades de empleo",79:"Agencias de viajes",80:"Seguridad privada",81:"Servicios a edificios",82:"Apoyo de oficina",
 84:"Administración pública",85:"Educación",86:"Atención de la salud humana",87:"Atención residencial",88:"Asistencia social",
 90:"Artes y entretenimiento",91:"Bibliotecas y museos",92:"Juegos de azar",93:"Deportes y recreación",94:"Asociaciones",
 95:"Reparación de computadores y efectos personales",96:"Otros servicios personales (peluquería, lavandería)",97:"Hogares empleadores",
 98:"Hogares productores",99:"Organizaciones extraterritoriales"}

def sector_cenu(d):
    return ("Agro y minería" if d <= 9 else "Industria" if d <= 39 else "Construcción" if d <= 43
            else "Comercio" if d <= 47 else "Transporte" if d <= 53 else "Servicios")
""")

md("## 4. Universos por módulo")
code("""
try:
    universos = S.get(f"{BASE}/structural/modules-universes", timeout=60).json()
except Exception as e:
    universos = {}; print("modules-universes no disponible:", e)
universos
""")

md("## 5. Unidades por división CIIU en Bogotá")
code("""
r = consultar(["ciiu_division"])["ciiu_division"]
d = r["values"]
validos = d["code"].astype(str).str.fullmatch(r"\\d{2}")
divisiones = (d[validos].assign(division=lambda x: x["code"].astype(int))
              .groupby("division", as_index=False)["value"].sum().rename(columns={"value": "unidades"}))
divisiones["nombre"] = divisiones["division"].map(DIVISIONES)
divisiones["sector_cenu"] = divisiones["division"].map(sector_cenu)
CON_CIIU = int(divisiones["unidades"].sum())
divisiones["pct_unidades"] = 100 * divisiones["unidades"] / CON_CIIU
divisiones = divisiones.sort_values("unidades", ascending=False, ignore_index=True)
divisiones.insert(0, "rank", divisiones.index + 1)
print(f"Unidades con división CIIU visible: {CON_CIIU:,} en {len(divisiones)} divisiones · total_count API: {r['total_count']}")
print(f"Códigos no válidos: {int(d.loc[~validos, 'value'].sum())}")
divisiones.head(15).round(2)
""")

code("""
por_sector = divisiones.groupby("sector_cenu", as_index=False)["unidades"].sum().sort_values("unidades", ascending=False)
por_sector["pct"] = 100 * por_sector["unidades"] / CON_CIIU
top10_pct = 100 * divisiones.head(10)["unidades"].sum() / CON_CIIU
print(f"Las 10 divisiones más grandes concentran el {top10_pct:.1f} % de las unidades")
por_sector.round(1)
""")

md("## 6. Rangos de ingreso 2023 y personal ocupado por división (top N)")
code("""
filas, detalle = [], []
for x in divisiones.head(TOP_N).itertuples():
    fila = {"rank": x.rank, "division": x.division, "nombre": x.nombre, "sector_cenu": x.sector_cenu,
            "unidades": x.unidades, "pct_unidades": x.pct_unidades}
    res = consultar(["total_income_2023", "total_employed_personnel"], {"ciiu_division": [f"{x.division:02d}"]})
    for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal")):
        vals = res[var]["values"]
        fila.update(indicadores(vals, etq))
        if f"respondieron_{etq}" in fila:
            fila[f"pct_respuesta_{etq}"] = 100 * fila[f"respondieron_{etq}"] / x.unidades
            fila[f"sin_dato_{etq}"] = x.unidades - fila[f"respondieron_{etq}"]
            detalle.append(vals.assign(division=x.division, variable=etq,
                                       clase=vals["description"].map(lambda s, e=etq: clase_rango(s, e))))
    filas.append(fila)
cuadro = pd.DataFrame(filas)
rangos_detalle = pd.concat(detalle, ignore_index=True)
resp = rangos_detalle[rangos_detalle.clase != "sin_dato"].groupby(["division", "variable"])["value"].sum().rename("respondieron")
rangos_detalle = rangos_detalle.join(resp, on=["division", "variable"])
rangos_detalle["pct_sobre_respondientes"] = (100 * rangos_detalle["value"] / rangos_detalle["respondieron"]).where(rangos_detalle.clase != "sin_dato")
cuadro[["division", "nombre", "unidades", "pct_respuesta_ingreso", "pct_bajo_ingreso", "pct_alto_ingreso",
        "pct_bajo_personal", "pct_alto_personal"]].round(1)
""")

md("## 7. Referencias: Bogotá agregado y nivel nacional")
code("""
agg = consultar(["total_income_2023", "total_employed_personnel"])            # Bogotá, todas las divisiones
bog = {etq: indicadores(agg[var]["values"], etq) for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal"))}
try:
    nac_raw = consultar(["total_income_2023", "total_employed_personnel"], nacional=True)
    nac = {etq: indicadores(nac_raw[var]["values"], etq) for var, etq in (("total_income_2023", "ingreso"), ("total_employed_personnel", "personal"))}
except Exception as e:
    print("Nivel nacional no disponible por la API; se usan los valores ya verificados:", e)
    nac_raw = None
    nac = {"ingreso": {"pct_bajo_ingreso": 23.76, "pct_alto_ingreso": 6.12}, "personal": {"pct_bajo_personal": 87.92, "pct_alto_personal": 2.04}}
REF_BAJO, REF_ALTO = nac["ingreso"]["pct_bajo_ingreso"], nac["ingreso"]["pct_alto_ingreso"]
comparacion = pd.DataFrame({
    "indicador": ["% ingreso 0-10 M", "% ingreso > 1.000 M", "% personal 1-5", "% personal > 50"],
    "bogota": [bog["ingreso"].get("pct_bajo_ingreso"), bog["ingreso"].get("pct_alto_ingreso"),
               bog["personal"].get("pct_bajo_personal"), bog["personal"].get("pct_alto_personal")],
    "nacional": [REF_BAJO, REF_ALTO, nac["personal"]["pct_bajo_personal"], nac["personal"]["pct_alto_personal"]]})
comparacion.round(1)
""")

md("## 8. Cuadro top 10 (entregable) con tipología")
code("""
def tipologia(bajo, alto):
    if pd.isna(bajo) or pd.isna(alto): return "Sin datos"
    if alto > REF_ALTO: return "Polarizado" if bajo >= 20 else "Base para escalar"
    return "Señal de subsistencia" if bajo >= 20 else "Intermedio"

cuadro["tipologia"] = [tipologia(b, a) for b, a in zip(cuadro.pct_bajo_ingreso, cuadro.pct_alto_ingreso)]
cuadro_top10 = cuadro.head(10)
cuadro_top10[["rank", "division", "nombre", "unidades", "pct_unidades", "pct_respuesta_ingreso", "pct_bajo_ingreso",
              "pct_alto_ingreso", "pct_respuesta_personal", "pct_bajo_personal", "pct_alto_personal", "tipologia"]].round(1)
""")

md("## 9. Controles de calidad")
code("""
controles = pd.DataFrame([
    ("Universo nacional del módulo", (universos.get(MODULO) or {}).get("universe")),
    ("Unidades con división CIIU visible (Bogotá)", CON_CIIU),
    ("total_count ciiu_division (API)", r["total_count"]),
    ("Σ divisiones = total_count", "OK" if r["total_count"] in (None, int(d["value"].sum())) else "REVISAR"),
    ("Σ rangos ingreso Bogotá = total_count", "OK" if agg["total_income_2023"]["total_count"] in (None, agg["total_income_2023"]["values"]["value"].sum()) else "REVISAR"),
    ("Σ rangos personal Bogotá = total_count", "OK" if agg["total_employed_personnel"]["total_count"] in (None, agg["total_employed_personnel"]["values"]["value"].sum()) else "REVISAR"),
    ("Sin información de personal (Bogotá)", bog["personal"].get("sin_info_personal")),
    ("Referencia nacional % bajo / % alto ingreso", f"{REF_BAJO:.1f} / {REF_ALTO:.1f}"),
], columns=["control", "valor"])
controles
""")

md("## 10. Gráfico de barras apiladas por rango (entregable)")
code("""
ROJO, GRIS, AZUL = "#e34948", "#c9c8c1", "#2a78d6"
fig, axs = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
t = cuadro_top10.iloc[::-1]
etiquetas = [f"{x.division:02d} {x.nombre[:32]}" for x in t.itertuples()]
for ax, etq, titulo, rotulos in ((axs[0], "ingreso", "Ingresos 2023", ("0–10 M", "11–1.000 M", "> 1.000 M")),
                                 (axs[1], "personal", "Personal ocupado", ("1–5", "6–50", "> 50"))):
    izq = 0
    for col, color, rot in ((f"pct_bajo_{etq}", ROJO, rotulos[0]), (f"pct_medio_{etq}", GRIS, rotulos[1]), (f"pct_alto_{etq}", AZUL, rotulos[2])):
        ax.barh(etiquetas, t[col], left=izq, color=color, edgecolor="white", linewidth=1.5, label=rot)
        izq = izq + t[col].values
    ax.set_xlim(0, 100); ax.set_title(f"{titulo} (% sobre respondientes)", loc="left", fontweight="bold", pad=28)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("Bogotá D.C. · Top 10 divisiones CIIU por rango · CENU 2024 preliminar", x=0.01, ha="left", fontweight="bold")
plt.tight_layout(); plt.savefig("ruta2_barras_apiladas.png", dpi=150, bbox_inches="tight"); plt.show()
""")

md("## 11. Mapa de oportunidades: ¿subsistencia o escalamiento?")
code("""
fig, ax = plt.subplots(figsize=(10, 6.5))
colores = [AZUL if a > REF_ALTO else ROJO if b >= 20 else "#9b9a92" for b, a in zip(cuadro.pct_bajo_ingreso, cuadro.pct_alto_ingreso)]
ax.scatter(cuadro.pct_bajo_ingreso, cuadro.pct_alto_ingreso, s=cuadro.unidades / 60, c=colores, alpha=.6, edgecolor="white")
for x in cuadro.itertuples():
    ax.annotate(f"{x.division:02d}", (x.pct_bajo_ingreso, x.pct_alto_ingreso), fontsize=9, xytext=(5, 3), textcoords="offset points")
ax.axvline(REF_BAJO, ls="--", color="grey", lw=1); ax.axhline(REF_ALTO, ls="--", color="grey", lw=1)
ax.set_xlabel("% con ingreso 2023 de 0–10 M"); ax.set_ylabel("% con ingreso 2023 > 1.000 M")
ax.set_title("Bogotá: subsistencia vs. escalamiento (líneas = referencia nacional; tamaño = unidades)", loc="left", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("ruta2_cuadrantes.png", dpi=150); plt.show()
""")

md("## 12. Exportar entregables (Excel, datos del dashboard, respuestas crudas)")
code("""
with pd.ExcelWriter("ruta2_resultados.xlsx") as w:
    cuadro_top10.round(2).to_excel(w, sheet_name="cuadro_top", index=False)
    cuadro.round(2).to_excel(w, sheet_name="cuadro_completo", index=False)
    rangos_detalle.round(2).to_excel(w, sheet_name="rangos_detalle", index=False)
    divisiones.round(3).to_excel(w, sheet_name="divisiones", index=False)
    por_sector.round(2).to_excel(w, sheet_name="por_sector", index=False)
    comparacion.round(2).to_excel(w, sheet_name="bogota_vs_nacional", index=False)
    controles.to_excel(w, sheet_name="controles", index=False)

data_js = "const data = [\\n" + ",\\n".join(
    f'  {{ name: {json.dumps(x.nombre, ensure_ascii=False)}, division: "{x.division:02d}", units: {int(x.unidades)}, '
    f'low: {x.pct_bajo_ingreso:.1f}, high: {x.pct_alto_ingreso:.1f}, lowPers: {x.pct_bajo_personal:.1f}, '
    f'highPers: {x.pct_alto_personal:.1f}, tipologia: {json.dumps(x.tipologia, ensure_ascii=False)} }}'
    for x in cuadro.itertuples()) + "\\n];"
open("dashboard_data.js", "w", encoding="utf-8").write(data_js)
json.dump(LOG, open("ruta2_respuestas_api.json", "w"), ensure_ascii=False)
print("Listo: ruta2_resultados.xlsx · ruta2_barras_apiladas.png · ruta2_cuadrantes.png · dashboard_data.js · ruta2_respuestas_api.json")
""")

md("## 13. Respuesta a la pregunta reto y recomendación de política local")
code("""
sub = cuadro[cuadro.tipologia == "Señal de subsistencia"]
esc = cuadro[cuadro.tipologia == "Base para escalar"].sort_values("pct_alto_ingreso", ascending=False)
comercio = por_sector.set_index("sector_cenu").loc["Comercio", "pct"]
print(f"• El comercio concentra el {comercio:.1f} % de las unidades y las 10 divisiones más grandes el {top10_pct:.1f} %.")
print("• Señal de subsistencia (ingreso bajo ≥ 20 % y alto ≤ referencia nacional): " +
      ", ".join(f"{x.division:02d} {x.nombre} ({x.pct_bajo_ingreso:.1f} % bajo, {x.pct_alto_ingreso:.1f} % alto)" for x in sub.itertuples()))
print(f"  Suman {int(sub.unidades.sum()):,} unidades ({100 * sub.unidades.sum() / CON_CIIU:.1f} % de Bogotá).")
print("• Oportunidades para emprender (ingreso alto > referencia nacional): " +
      ", ".join(f"{x.division:02d} {x.nombre} ({x.pct_alto_ingreso:.1f} %)" for x in esc.itertuples()))
""")

md("""
**Recomendación de política local**
1. **Formalizar sin ahogar** (divisiones con señal de subsistencia): Régimen Simple, microcrédito como alternativa al "gota a gota", pagos digitales y certificación de oficios.
2. **Encadenar mayoristas (46) con minoristas (47):** programas de proveeduría, crédito de proveedor y compras agrupadas.
3. **Emprender con techo:** capital semilla, compras públicas y crédito productivo en las divisiones con base para escalar.

**Advertencias:** resultados **preliminares**; los % son sobre quienes respondieron (la respuesta se reporta aparte); un rango bajo es una **señal** de posible subsistencia, no una prueba; la API publica por municipio (no por localidad).
""")

code("""
# Descargar los entregables (solo en Google Colab)
try:
    from google.colab import files
    for f in ["ruta2_resultados.xlsx", "ruta2_barras_apiladas.png", "ruta2_cuadrantes.png", "dashboard_data.js"]:
        files.download(f)
except ImportError:
    print("Fuera de Colab: los archivos quedaron en la carpeta actual.")
""")

nb = nbf.v4.new_notebook()
nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
dest = Path(__file__).resolve().parent / "Ruta2_Bogota_CENU.ipynb"
nbf.write(nb, dest)
print("->", dest)
