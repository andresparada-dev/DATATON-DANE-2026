"""Generador de datos SINTÉTICOS con forma de censo económico, para ensayar el flujo.

ADVERTENCIA: los valores son aleatorios y NO representan cifras reales del DANE.
Sirven solo para probar scripts, gráficas y el reporte antes de recibir los datos oficiales.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Centros aproximados de cinco capitales (para que el mapa se vea plausible) y peso relativo de muestra.
CIUDADES = [
    ("11001", "11", "BOGOTÁ, D.C.", "Bogotá, D.C.", 4.6482, -74.1007, 0.40),
    ("05001", "05", "ANTIOQUIA", "Medellín", 6.2476, -75.5658, 0.20),
    ("76001", "76", "VALLE DEL CAUCA", "Cali", 3.4372, -76.5225, 0.17),
    ("08001", "08", "ATLÁNTICO", "Barranquilla", 10.9685, -74.7813, 0.13),
    ("68001", "68", "SANTANDER", "Bucaramanga", 7.1193, -73.1227, 0.10),
]

# (código CIIU clase, peso) — mezcla típica de economía urbana de pequeña escala
ACTIVIDADES = [
    ("4711", 0.20), ("4721", 0.06), ("4771", 0.05), ("4772", 0.03), ("4752", 0.03), ("4530", 0.02),
    ("5611", 0.09), ("5613", 0.03), ("9602", 0.07), ("9601", 0.01), ("4520", 0.04), ("1081", 0.03),
    ("1410", 0.03), ("6810", 0.02), ("8621", 0.02), ("6910", 0.02), ("6201", 0.01), ("9511", 0.02),
    ("4923", 0.03), ("8559", 0.02), ("4719", 0.04), ("4741", 0.02), ("3110", 0.01), ("4663", 0.02),
    ("5511", 0.01), ("9311", 0.01), ("4773", 0.02), ("1811", 0.01), ("7310", 0.01), ("4111", 0.01),
]

TIPOS = ["Establecimiento fijo", "Vivienda con actividad económica", "Puesto móvil o semifijo"]


def generar(n: int = 20_000, semilla: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    ciudades = pd.DataFrame(CIUDADES, columns=["cod_mpio", "cod_dpto", "departamento", "municipio", "lat", "lon", "peso"])
    ic = rng.choice(len(ciudades), size=n, p=ciudades["peso"] / ciudades["peso"].sum())
    c = ciudades.iloc[ic].reset_index(drop=True)

    # Cada ciudad con 6 "centralidades" comerciales + dispersión residencial
    centros = {m: rng.normal(0, 0.03, size=(6, 2)) for m in ciudades["cod_mpio"]}
    en_centralidad = rng.random(n) < 0.55
    k = rng.integers(0, 6, n)
    off_c = np.array([centros[m][j] for m, j in zip(c["cod_mpio"], k)])
    dispersion = np.where(en_centralidad[:, None], rng.normal(0, 0.004, (n, 2)), rng.normal(0, 0.035, (n, 2)))
    lat = c["lat"].to_numpy() + np.where(en_centralidad, off_c[:, 0], 0) + dispersion[:, 0]
    lon = c["lon"].to_numpy() + np.where(en_centralidad, off_c[:, 1], 0) + dispersion[:, 1]

    codigos, pesos = zip(*ACTIVIDADES)
    pesos = np.array(pesos) / np.sum(pesos)
    ciiu = rng.choice(codigos, size=n, p=pesos)

    tipo = rng.choice(TIPOS, size=n, p=[0.55, 0.33, 0.12])
    base = np.where(tipo == TIPOS[0], 1.2, 0.4)
    personal = np.clip(np.round(rng.lognormal(base, 0.8)), 1, 400).astype(int)

    sexo = rng.choice(["Mujer", "Hombre", "Ambos/Mixto"], size=n, p=[0.42, 0.50, 0.08])
    p_reg = 1 / (1 + np.exp(-(-1.4 + 0.5 * np.log(personal) + 1.2 * (tipo == TIPOS[0]) - 0.25 * (sexo == "Mujer"))))
    registro = rng.random(n) < p_reg
    rut = registro | (rng.random(n) < 0.25)
    contabilidad = registro & (rng.random(n) < 0.7)
    anios = np.round(rng.gamma(1.6, 4.5, n), 1)

    return pd.DataFrame({
        "ID_UE": np.arange(1, n + 1),
        "COD_DPTO": c["cod_dpto"], "DEPARTAMENTO": c["departamento"],
        "COD_MPIO": c["cod_mpio"], "MUNICIPIO": c["municipio"],
        "LATITUD": lat.round(6), "LONGITUD": lon.round(6),
        "TIPO_UNIDAD": tipo, "CIIU": ciiu,
        "PERSONAL_OCUPADO": personal,
        "SEXO_PROPIETARIO": sexo,
        "REGISTRO_MERCANTIL": np.where(registro, "Sí", "No"),
        "RUT": np.where(rut, 1, 2),
        "CONTABILIDAD": np.where(contabilidad, "Sí", "No"),
        "ANIOS_FUNCIONAMIENTO": anios,
        "FUENTE": "SINTETICO - NO ES DATO OFICIAL",
    })
