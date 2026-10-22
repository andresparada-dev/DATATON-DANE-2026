"""Esquema estándar de una unidad económica y normalizador de columnas.

El día de la datatón no sabremos con certeza los nombres de columnas del archivo que entregue
el DANE. `normalizar` detecta columnas por alias (sin tildes, sin mayúsculas, por subcadenas)
y las renombra al esquema estándar para que el resto del toolkit funcione sin cambios.
"""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

# columna estándar -> descripción
ESQUEMA: dict[str, str] = {
    "id_unidad": "Identificador de la unidad económica",
    "cod_dpto": "Código DIVIPOLA del departamento (2 dígitos)",
    "departamento": "Nombre del departamento",
    "cod_mpio": "Código DIVIPOLA del municipio (5 dígitos)",
    "municipio": "Nombre del municipio",
    "clase": "Clase geográfica (cabecera / centro poblado / rural)",
    "sector_urbano": "Sector/sección/manzana del MGN o localidad/comuna",
    "latitud": "Latitud WGS84",
    "longitud": "Longitud WGS84",
    "tipo_unidad": "Tipo: establecimiento fijo, vivienda con actividad, puesto móvil/semifijo",
    "ciiu": "Código CIIU Rev. 4 A.C. (2-4 dígitos)",
    "ciiu_seccion": "Sección CIIU (letra A-U)",
    "actividad": "Descripción de la actividad económica",
    "personal_ocupado": "Número de personas ocupadas",
    "sexo_propietario": "Sexo de la persona propietaria",
    "registro_mercantil": "Tiene registro mercantil / matrícula en cámara de comercio (bool)",
    "rut": "Tiene RUT (bool)",
    "contabilidad": "Lleva contabilidad / registros (bool)",
    "anios_funcionamiento": "Años de funcionamiento",
    "ingresos": "Ingresos / ventas (valor monetario)",
    "estado": "Estado de la unidad (activa, cerrada, desocupada...)",
    "factor_expansion": "Factor de expansión (si aplica para muestras)",
}

# alias normalizados (sin tildes, minúsculas, '_' en vez de espacios). Se prueba primero coincidencia exacta,
# luego "contiene". El orden importa: alias más específicos primero.
ALIAS: dict[str, list[str]] = {
    "id_unidad": ["id_unidad", "id_ue", "idue", "id_establecimiento", "consecutivo", "id", "nro_formulario", "directorio"],
    "cod_dpto": ["cod_dpto", "cod_depto", "coddepto", "dpto", "cod_dane_dpto", "u_dpto", "codigo_departamento", "dp"],
    "departamento": ["departamento", "nom_dpto", "nombre_departamento", "depto"],
    "cod_mpio": ["cod_mpio", "codmpio", "cod_municipio", "u_mpio", "codigo_municipio", "divipola", "mpio_ccdgo", "cod_dane"],
    "municipio": ["municipio", "nom_mpio", "nombre_municipio", "ciudad", "mpio_cnmbr"],
    "clase": ["clase", "area", "clase_geo", "cabecera"],
    "sector_urbano": ["localidad", "comuna", "sector_urbano", "setu_ccdgo", "secu_ccdgo", "manzana", "mz", "upz", "barrio"],
    "latitud": ["latitud", "lat", "y", "coord_y"],
    "longitud": ["longitud", "lon", "lng", "long", "x", "coord_x"],
    "tipo_unidad": ["tipo_unidad", "tipo_ue", "tipo_establecimiento", "tipo", "tipo_de_unidad", "categoria_unidad"],
    "ciiu": ["ciiu", "cod_ciiu", "ciiu4", "ciiu_rev4", "codigo_ciiu", "actividad_economica_cod", "act_ciiu"],
    "ciiu_seccion": ["seccion_ciiu", "ciiu_seccion", "seccion"],
    "actividad": ["actividad", "descripcion_actividad", "desc_actividad", "actividad_economica", "nombre_actividad"],
    "personal_ocupado": ["personal_ocupado", "pers_ocup", "total_ocupados", "ocupados", "num_empleados", "empleados", "personal", "trabajadores"],
    "sexo_propietario": ["sexo_propietario", "sexo_prop", "sexo_dueno", "sexo", "genero"],
    "registro_mercantil": ["registro_mercantil", "camara_comercio", "matricula_mercantil", "registro_camara", "reg_mercantil"],
    "rut": ["rut", "tiene_rut", "registro_unico_tributario"],
    "contabilidad": ["contabilidad", "lleva_contabilidad", "registros_contables", "libros"],
    "anios_funcionamiento": ["anios_funcionamiento", "anos_funcionamiento", "tiempo_funcionamiento", "antiguedad", "anios"],
    "ingresos": ["ingresos", "ventas", "valor_ventas", "ingreso_mensual", "ingresos_mes"],
    "estado": ["estado", "estado_unidad", "condicion"],
    "factor_expansion": ["factor_expansion", "fex", "fex_c", "factor"],
}

VERDADEROS = {"si", "sí", "s", "1", "true", "verdadero", "yes", "y", "x"}
FALSOS = {"no", "n", "0", "2", "false", "falso"}


def _slug(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "_", texto.strip().lower())
    return texto.strip("_")


def mapear_columnas(columnas: list[str]) -> dict[str, str]:
    """Devuelve {columna_original: columna_estandar} para las columnas reconocidas."""
    slugs = {c: _slug(c) for c in columnas}
    asignadas: dict[str, str] = {}
    usadas: set[str] = set()
    # 1) coincidencia exacta; 2) el alias es una palabra del nombre ("actividad_ciiu" -> ciiu);
    # 3) el slug empieza por el alias; 4) el alias está contenido (alias >= 4 letras)
    for fase in ("exacta", "palabra", "prefijo", "contiene"):
        for estandar, alias in ALIAS.items():
            if estandar in asignadas.values():
                continue
            for a in alias:
                candidato = None
                for original, s in slugs.items():
                    if original in usadas:
                        continue
                    if (fase == "exacta" and s == a) or \
                       (fase == "palabra" and len(a) >= 3 and "_" not in a and a in s.split("_")) or \
                       (fase == "prefijo" and len(a) >= 3 and s.startswith(a + "_")) or \
                       (fase == "contiene" and len(a) >= 4 and a in s):
                        candidato = original
                        break
                if candidato:
                    asignadas[candidato] = estandar
                    usadas.add(candidato)
                    break
    return asignadas


def a_booleano(serie: pd.Series) -> pd.Series:
    """Convierte Sí/No, 1/2, True/False... a booleano con nulos (convención DANE: 1=Sí, 2=No)."""
    def conv(v):
        if pd.isna(v):
            return pd.NA
        if isinstance(v, bool):
            return v
        t = str(int(v)) if isinstance(v, (int, float)) else _slug(v)
        if t in VERDADEROS:
            return True
        if t in FALSOS:
            return False
        return pd.NA
    return serie.map(conv).astype("boolean")


def normalizar(df: pd.DataFrame, mapeo_manual: dict[str, str] | None = None, verbose: bool = True) -> pd.DataFrame:
    """Renombra columnas al esquema estándar y tipifica las conocidas.

    mapeo_manual: {columna_original: columna_estandar} para forzar asignaciones.
    Las columnas no reconocidas se conservan sin cambios.
    """
    mapeo = mapear_columnas(list(df.columns))
    if mapeo_manual:
        mapeo = {k: v for k, v in mapeo.items() if v not in mapeo_manual.values()}
        mapeo.update(mapeo_manual)
    out = df.rename(columns=mapeo).copy()
    if verbose:
        print("Columnas reconocidas:")
        for o, e in mapeo.items():
            print(f"  {o!r:>30} -> {e}")
        faltantes = [c for c in ("ciiu", "personal_ocupado", "cod_mpio", "latitud", "longitud") if c not in out.columns]
        if faltantes:
            print("Columnas clave no encontradas (usar mapeo_manual):", faltantes)

    for c in ("cod_dpto", "cod_mpio"):
        if c in out.columns:
            ancho = 2 if c == "cod_dpto" else 5
            out[c] = (out[c].astype("string").str.replace(r"\.0$", "", regex=True)
                      .str.replace(r"\D", "", regex=True).str.zfill(ancho))
    if "cod_mpio" in out.columns and "cod_dpto" not in out.columns:
        out["cod_dpto"] = out["cod_mpio"].str[:2]
    for c in ("latitud", "longitud", "personal_ocupado", "anios_funcionamiento", "ingresos", "factor_expansion"):
        if c in out.columns:
            out[c] = pd.to_numeric(out[c].astype("string").str.replace(",", ".", regex=False), errors="coerce")
    for c in ("registro_mercantil", "rut", "contabilidad"):
        if c in out.columns:
            out[c] = a_booleano(out[c])
    if "sexo_propietario" in out.columns:
        out["sexo_propietario"] = out["sexo_propietario"].map(_normalizar_sexo)
    if "latitud" in out.columns and "longitud" in out.columns:
        # Colombia: lat ~ -4.3..13.5, lon ~ -82..-66. Si vienen invertidas, se corrigen.
        invertidas = out["latitud"].lt(-60) & out["longitud"].between(-5, 14)
        if invertidas.any():
            out.loc[invertidas, ["latitud", "longitud"]] = out.loc[invertidas, ["longitud", "latitud"]].values
    return out


def _normalizar_sexo(v):
    if pd.isna(v):
        return pd.NA
    t = _slug(v)
    if t in {"1", "h", "hombre", "m", "masculino", "male"}:
        return "Hombre"
    if t in {"2", "mujer", "f", "femenino", "female"}:
        return "Mujer"
    if t in {"3", "ambos", "mixto", "sociedad", "compartido"}:
        return "Ambos/Mixto"
    return "Otro/No informa"


def perfil_calidad(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla rápida de calidad: tipo, % nulos, nº de valores únicos y ejemplo."""
    filas = []
    for c in df.columns:
        s = df[c]
        filas.append({
            "columna": c,
            "tipo": str(s.dtype),
            "pct_nulos": round(100 * s.isna().mean(), 2),
            "unicos": s.nunique(dropna=True),
            "ejemplo": s.dropna().iloc[0] if s.notna().any() else None,
        })
    return pd.DataFrame(filas)
