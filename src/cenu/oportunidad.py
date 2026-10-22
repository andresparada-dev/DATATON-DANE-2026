"""MVP "Donde Falta, Emprende": desiertos de servicios esenciales y oportunidades de negocio.

Idea: para cada categoría esencial (droguería, tienda, ferretería...) se mide, por celda de la ciudad,
la distancia a la unidad más cercana de esa categoría. Una celda "habitada" (con demanda) a más de
`radio_m` metros es un desierto. Las oportunidades se ordenan por demanda en desierto.

Demanda: si hay población por celda/manzana (CNPV 2018 / MGN) se usa; si no, se aproxima con el
número total de unidades económicas en la celda (actividad urbana). Todo se reporta AGREGADO por celda
(nunca unidades individuales), respetando la reserva estadística.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import spatial

# Categoría -> prefijos de clase CIIU Rev. 4 A.C. (se compara por "empieza por")
CATEGORIAS_ESENCIALES: dict[str, tuple[str, ...]] = {
    "Tienda / minimercado": ("4711", "4719", "4721", "4722", "4723", "4729"),
    "Droguería / farmacia": ("4773",),
    "Panadería": ("1081", "4724"),
    "Ferretería": ("4752",),
    "Papelería": ("4761",),
    "Peluquería / belleza": ("9602",),
    "Restaurante / comidas": ("5611", "5612", "5613", "5619"),
    "Salud (consultorios)": ("8621", "8622", "8691", "8692"),
    "Educación inicial": ("8511", "8512", "8513"),
    "Cuidado (asistencia social)": ("87", "88"),
    "Servicios financieros": ("64", "6612"),
}


def marcar_categorias(df: pd.DataFrame, col: str = "ciiu",
                      categorias: dict[str, tuple[str, ...]] = CATEGORIAS_ESENCIALES) -> pd.Series:
    """Devuelve la categoría esencial de cada unidad (o NA)."""
    codigo = df[col].astype("string").str.replace(r"\D", "", regex=True)
    # clases con cero inicial perdido (p. ej. 111) no son esenciales urbanas; se dejan como están
    salida = pd.Series(pd.NA, index=df.index, dtype="string")
    for nombre, prefijos in categorias.items():
        m = codigo.str.startswith(prefijos).fillna(False) & salida.isna()
        salida[m] = nombre
    return salida


def desiertos(df: pd.DataFrame, tam_celda_m: int = 250, radio_m: int = 500,
              poblacion_celdas: pd.DataFrame | None = None, min_demanda: float = 1,
              categorias: dict[str, tuple[str, ...]] = CATEGORIAS_ESENCIALES) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula distancia por celda al servicio más cercano de cada categoría.

    Devuelve (celdas, resumen):
      celdas:  una fila por celda con demanda, dist_<cat> (m) y desierto_<cat> (bool)
      resumen: por categoría -> unidades, % celdas y % demanda en desierto, saturación media
    poblacion_celdas: DataFrame opcional con columnas celda, poblacion (misma grilla: spatial.grilla).
    """
    d = df.dropna(subset=["latitud", "longitud"]).copy()
    d[["latitud", "longitud"]] = d[["latitud", "longitud"]].astype(float)
    d["categoria"] = marcar_categorias(d, categorias=categorias)
    celdas = spatial.grilla(d, tam_m=tam_celda_m).rename(columns={"valor": "unidades_totales"})
    if poblacion_celdas is not None:
        celdas = celdas.merge(poblacion_celdas[["celda", "poblacion"]], on="celda", how="left")
        celdas["demanda"] = celdas["poblacion"].fillna(0)
    else:
        celdas["demanda"] = celdas["unidades_totales"]
    celdas = celdas[celdas["demanda"] >= min_demanda].reset_index(drop=True)

    filas = []
    for cat in categorias:
        destinos = d[d["categoria"] == cat]
        col = f"dist_{cat}"
        if destinos.empty:
            celdas[col] = np.inf
        else:
            celdas[col] = spatial.distancia_mas_cercana(celdas, destinos) * 1000
        celdas[f"desierto_{cat}"] = celdas[col] > radio_m
        n_cat = len(destinos)
        filas.append({
            "categoria": cat,
            "unidades": n_cat,
            "pct_celdas_desierto": 100 * celdas[f"desierto_{cat}"].mean(),
            "pct_demanda_desierto": 100 * celdas.loc[celdas[f"desierto_{cat}"], "demanda"].sum() / celdas["demanda"].sum(),
            "demanda_por_unidad": celdas["demanda"].sum() / n_cat if n_cat else np.inf,
            "dist_mediana_m": float(np.median(celdas[col])) if n_cat else np.inf,
        })
    # Categorías sin ninguna unidad van al final (en datos reales suelen indicar un problema de códigos CIIU)
    resumen = (pd.DataFrame(filas).assign(_sin=lambda x: x["unidades"] == 0)
               .sort_values(["_sin", "pct_demanda_desierto"], ascending=[True, False]).drop(columns="_sin")
               .reset_index(drop=True))
    return celdas, resumen


def top_oportunidades(celdas: pd.DataFrame, categoria: str, n: int = 10, radio_m: int = 500) -> pd.DataFrame:
    """Celdas en desierto de `categoria` con mayor demanda (dónde abrir primero)."""
    col = f"dist_{categoria}"
    t = celdas[celdas[col] > radio_m].sort_values("demanda", ascending=False).head(n)
    return t[["celda", "latitud", "longitud", "demanda", "unidades_totales", col]].rename(
        columns={col: "distancia_al_mas_cercano_m"}).reset_index(drop=True)
