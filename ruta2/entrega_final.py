"""Ruta 2 · arma ruta2_entrega_final.xlsx (cuadro top 10 por división, sectores reales, detalle 4 dígitos del visor, controles)
a partir de ruta2_resultados.xlsx (salida de ruta2_bogota.py). Uso: python entrega_final.py"""
import pandas as pd
r = pd.read_excel("ruta2_resultados.xlsx", sheet_name=None)          # salida del script (datos API)
div, top = r["divisiones"].copy(), r["cuadro_top"].copy()
UNIVERSO_BOG = 195_755                                               # visor / API (10 con CIIU suprimido)

def sector_cenu(d):
    return ("Agro y minería" if d <= 9 else "Industria" if d <= 39 else "Construcción" if d <= 43
            else "Comercio" if d <= 47 else "Transporte" if d <= 53 else "Servicios")
div["sector_cenu"] = div["division"].map(sector_cenu)
sect = div.groupby("sector_cenu", as_index=False)["unidades"].sum().sort_values("unidades", ascending=False)
sect["pct_sobre_unidades_con_CIIU"] = (100 * sect["unidades"] / sect["unidades"].sum()).round(1)

def tipo(bajo, alto, NB=23.8, NA=6.1):
    if pd.isna(bajo) or pd.isna(alto):
        return "Sin datos"
    if alto > NA:
        return "Polarizado" if bajo >= 20 else "Base para escalar"
    return "Señal de subsistencia" if bajo >= 20 else "Intermedio"

cuadro = pd.DataFrame({
    "División CIIU": top["division"].map(lambda x: f"{int(x):02d}"),
    "Actividad": top["nombre"], "Sector": top["division"].map(sector_cenu),
    "Unidades económicas": top["unidades"].astype(int),
    "% respuesta ingreso": top["pct_respuesta_ingreso"].round(1),
    "% bajo ingreso (0-10 M)": top["pct_bajo_ingreso"].round(1),
    "% alto ingreso (>1.000 M)": top["pct_alto_ingreso"].round(1),
    "% respuesta personal": top["pct_respuesta_personal"].round(1),
    "% bajo personal (1-5)": top["pct_bajo_personal"].round(1),
    "% alto personal (>50)": top["pct_alto_personal"].round(1),
    "Tipología (vs nacional 23,8 % / 6,1 %)": [tipo(b, a) for b, a in zip(top["pct_bajo_ingreso"], top["pct_alto_ingreso"])],
})
visor = pd.DataFrame([  # Visor Interactivo CENU (treemap Bogotá), solo conteos; códigos visibles
    ("4781", "Comercio al por menor de alimentos, bebidas y tabaco en puestos móviles", 16410),
    ("4711", "Comercio al por menor no especializado (tiendas, minimercados)", 13114),
    ("5611", "Expendio a la mesa de comidas preparadas", 9049),
    ("4771", "Comercio al por menor de prendas de vestir", 7328),
    ("9602", "Peluquería y otros tratamientos de belleza", 6817),
    ("5619", "Otros tipos de expendio de comidas preparadas", 6437),
    ("4520", "Mantenimiento y reparación de vehículos automotores", 6314),
    ("4782", "Comercio al por menor de textiles y calzado en puestos móviles", 5493),
    ("4752", "Comercio al por menor de artículos de ferretería", 5307),
    ("4773", "Comercio al por menor de productos farmacéuticos y de tocador", 4944),
], columns=["Código CIIU (4 díg.)", "Actividad", "Unidades"])
visor["% de Bogotá"] = (100 * visor["Unidades"] / UNIVERSO_BOG).round(1)
control = pd.DataFrame([
    ("Universo Bogotá (módulo sectoral_reference_2023)", UNIVERSO_BOG),
    ("Unidades con división CIIU visible", int(div["unidades"].sum())),
    ("CIIU no visible por reserva estadística (anonimización)", UNIVERSO_BOG - int(div["unidades"].sum())),
    ("Referencia nacional % bajo ingreso", 23.8), ("Referencia nacional % alto ingreso", 6.1),
], columns=["Control", "Valor"])

with pd.ExcelWriter("ruta2_entrega_final.xlsx") as w:
    cuadro.to_excel(w, sheet_name="cuadro_top10", index=False)
    sect.to_excel(w, sheet_name="por_sector", index=False)
    visor.to_excel(w, sheet_name="detalle_4dig_visor", index=False)
    r["rangos_detalle"].to_excel(w, sheet_name="rangos_detalle", index=False)
    control.to_excel(w, sheet_name="controles", index=False)
print(cuadro.to_string(index=False)); print(sect.to_string(index=False)); print(control.to_string(index=False))
