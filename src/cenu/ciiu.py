"""Clasificación Industrial Internacional Uniforme CIIU Rev. 4 adaptada para Colombia (A.C.).

Las secciones y rangos de divisiones son los de la CIIU Rev. 4 (ONU), que el DANE adopta
en la versión A.C. Referencia: https://www.dane.gov.co (Clasificaciones -> CIIU Rev. 4 A.C.).
"""

from __future__ import annotations

import re

import pandas as pd

# Sección -> (nombre, división inicial, división final)
SECCIONES: dict[str, tuple[str, int, int]] = {
    "A": ("Agricultura, ganadería, caza, silvicultura y pesca", 1, 3),
    "B": ("Explotación de minas y canteras", 5, 9),
    "C": ("Industrias manufactureras", 10, 33),
    "D": ("Suministro de electricidad, gas, vapor y aire acondicionado", 35, 35),
    "E": ("Distribución de agua; evacuación y tratamiento de aguas residuales, gestión de desechos", 36, 39),
    "F": ("Construcción", 41, 43),
    "G": ("Comercio al por mayor y al por menor; reparación de vehículos automotores y motocicletas", 45, 47),
    "H": ("Transporte y almacenamiento", 49, 53),
    "I": ("Alojamiento y servicios de comida", 55, 56),
    "J": ("Información y comunicaciones", 58, 63),
    "K": ("Actividades financieras y de seguros", 64, 66),
    "L": ("Actividades inmobiliarias", 68, 68),
    "M": ("Actividades profesionales, científicas y técnicas", 69, 75),
    "N": ("Actividades de servicios administrativos y de apoyo", 77, 82),
    "O": ("Administración pública y defensa; seguridad social obligatoria", 84, 84),
    "P": ("Educación", 85, 85),
    "Q": ("Actividades de atención de la salud humana y de asistencia social", 86, 88),
    "R": ("Actividades artísticas, de entretenimiento y recreación", 90, 93),
    "S": ("Otras actividades de servicios", 94, 96),
    "T": ("Actividades de los hogares como empleadores y productores para uso propio", 97, 98),
    "U": ("Actividades de organizaciones y entidades extraterritoriales", 99, 99),
}

# Agrupación de gran sector usada en los boletines de censos económicos / EMICRON.
GRAN_SECTOR: dict[str, str] = {
    **{s: "Industria" for s in ("B", "C", "D", "E")},
    "F": "Construcción",
    "G": "Comercio",
    **{s: "Servicios" for s in ("H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U")},
    "A": "Agropecuario",
}

# Divisiones frecuentes en economía urbana de pequeña escala (para etiquetas legibles).
DIVISIONES_FRECUENTES: dict[int, str] = {
    10: "Elaboración de productos alimenticios",
    14: "Confección de prendas de vestir",
    16: "Transformación de la madera",
    25: "Productos elaborados de metal",
    31: "Fabricación de muebles",
    45: "Comercio y reparación de vehículos",
    46: "Comercio al por mayor",
    47: "Comercio al por menor",
    49: "Transporte terrestre",
    55: "Alojamiento",
    56: "Servicios de comida y bebida",
    61: "Telecomunicaciones",
    62: "Desarrollo de software y consultoría TI",
    68: "Actividades inmobiliarias",
    69: "Actividades jurídicas y de contabilidad",
    85: "Educación",
    86: "Actividades de atención de la salud humana",
    93: "Actividades deportivas y recreativas",
    95: "Reparación de computadores y efectos personales",
    96: "Otros servicios personales (peluquería, lavandería)",
}


def division_desde_codigo(codigo, tres_digitos: str = "grupo") -> int | None:
    """Extrae la división (2 dígitos) desde un código CIIU de 2, 3 o 4 dígitos.

    Un código de 3 dígitos es ambiguo: puede ser un *grupo* (p. ej. 471) o una *clase* de
    4 dígitos que perdió el cero inicial al leerse como número (0111 -> 111).
    `tres_digitos` decide: "grupo" (por defecto) o "clase". `enriquecer_ciiu` lo infiere
    por columna.

    >>> division_desde_codigo("4711")
    47
    >>> division_desde_codigo(471)
    47
    >>> division_desde_codigo(111, tres_digitos="clase")
    1
    """
    if codigo is None or (isinstance(codigo, float) and pd.isna(codigo)):
        return None
    texto = re.sub(r"\D", "", str(codigo).split(".")[0])
    if not texto:
        return None
    if len(texto) == 3 and tres_digitos == "clase":
        texto = "0" + texto
    if len(texto) == 1:
        texto = "0" + texto
    return int(texto[:2])


def _modo_tres_digitos(serie: pd.Series) -> str:
    """Si la mayoría de códigos tiene 4 dígitos, los de 3 son clases sin el cero inicial."""
    largos = serie.dropna().astype(str).str.split(".").str[0].str.replace(r"\D", "", regex=True).str.len()
    if largos.empty:
        return "grupo"
    return "clase" if (largos == 4).mean() >= 0.5 else "grupo"


def seccion_desde_division(division: int | None) -> str | None:
    if division is None:
        return None
    for letra, (_, ini, fin) in SECCIONES.items():
        if ini <= division <= fin:
            return letra
    return None


def enriquecer_ciiu(df: pd.DataFrame, col: str = "ciiu") -> pd.DataFrame:
    """Agrega columnas ciiu_division, ciiu_seccion, ciiu_seccion_nombre y gran_sector."""
    out = df.copy()
    # Si ya viene la sección como letra, se respeta.
    if col in out.columns:
        modo = _modo_tres_digitos(out[col])
        out["ciiu_division"] = out[col].map(lambda c: division_desde_codigo(c, modo))
        out["ciiu_seccion"] = out["ciiu_division"].map(seccion_desde_division)
    if "ciiu_seccion" in out.columns:
        out["ciiu_seccion"] = out["ciiu_seccion"].astype("string").str.upper().str.strip()
        out["ciiu_seccion_nombre"] = out["ciiu_seccion"].map(lambda s: SECCIONES.get(s, (None,))[0] if pd.notna(s) else None)
        out["gran_sector"] = out["ciiu_seccion"].map(GRAN_SECTOR)
    return out
