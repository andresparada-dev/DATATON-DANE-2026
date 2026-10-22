import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cenu import ciiu, indicators as ind, schema, spatial, synthetic  # noqa: E402


@pytest.fixture(scope="module")
def df():
    crudo = synthetic.generar(3000, semilla=1)
    return ciiu.enriquecer_ciiu(schema.normalizar(crudo, verbose=False))


def test_ciiu_division_y_seccion():
    assert ciiu.division_desde_codigo("4711") == 47
    assert ciiu.division_desde_codigo(471) == 47
    assert ciiu.division_desde_codigo(111, tres_digitos="clase") == 1
    assert ciiu.seccion_desde_division(47) == "G"
    assert ciiu.seccion_desde_division(56) == "I"
    assert ciiu.seccion_desde_division(4) is None


def test_ciiu_infiere_clases_sin_cero():
    d = ciiu.enriquecer_ciiu(pd.DataFrame({"ciiu": [4711, 5611, 111, 9602]}))
    assert d["ciiu_seccion"].tolist() == ["G", "I", "A", "S"]


def test_normalizar_alias_y_tipos():
    crudo = pd.DataFrame({
        "Cód. Municipio": ["5001", "11001"], "Actividad CIIU": ["4711", "5611"],
        "Total ocupados": ["3", "1"], "Matrícula mercantil": ["Sí", "No"], "Lat": ["6,2", "4,6"], "Lon": ["-75.5", "-74.1"],
        "Sexo": [2, 1],
    })
    d = schema.normalizar(crudo, verbose=False)
    assert d["cod_mpio"].tolist() == ["05001", "11001"]
    assert d["cod_dpto"].tolist() == ["05", "11"]
    assert d["registro_mercantil"].tolist() == [True, False]
    assert d["latitud"].tolist() == [6.2, 4.6]
    assert d["sexo_propietario"].tolist() == ["Mujer", "Hombre"]
    assert "ciiu" in d.columns and "personal_ocupado" in d.columns


def test_lq_promedio_ponderado_es_uno(df):
    lq = ind.cociente_localizacion(df, "municipio", "ciiu_seccion")
    m = df.groupby(["municipio", "ciiu_seccion"]).size().unstack(fill_value=0)
    pesos = m.sum(axis=1) / m.values.sum()
    # el promedio de LQ ponderado por tamaño de región es 1 en cada sector
    assert np.allclose((lq.mul(pesos, axis=0)).sum(axis=0), 1.0)


def test_hhi_rango(df):
    h = ind.hhi_diversificacion(df, "municipio", "ciiu_division")
    assert ((h["hhi"] > 0) & (h["hhi"] <= 1)).all()


def test_formalidad_y_kpis(df):
    f = ind.indice_formalidad(df, "gran_sector")
    assert f["indice_formalidad"].between(0, 100).all()
    k = ind.resumen_kpis(df)
    assert k["unidades_economicas"] == len(df)
    assert 0 <= k["pct_registro_mercantil"] <= 100


def test_brecha_oferta():
    d = pd.DataFrame({"zona": ["a"] * 10 + ["b"] * 2, "sector": ["x"] * 12})
    pob = pd.DataFrame({"zona": ["a", "b"], "poblacion": [1000, 1000]})
    b = ind.brecha_oferta(d, "zona", "sector", pob, min_esperado=0)
    assert b.iloc[0]["zona"] == "b" and b.iloc[0]["brecha"] > 0


def test_espacial(df):
    g = spatial.grilla(df, 500)
    assert g["valor"].sum() == len(df)
    assert abs(spatial.haversine_km(4.6, -74.1, 4.6, -74.1)) < 1e-9
    assert spatial.haversine_km(4.0, -74.0, 5.0, -74.0) == pytest.approx(111.2, rel=0.01)
    bog = df[df["municipio"] == "Bogotá, D.C."]
    etiquetas = spatial.clusters_dbscan(bog, eps_m=200, min_muestras=10)
    assert (etiquetas >= 0).any()
    dist = spatial.distancia_mas_cercana(bog.head(5), bog)
    assert np.allclose(dist, 0)


def test_moran_detecta_agrupamiento():
    rng = np.random.default_rng(0)
    coords = rng.uniform(0, 0.1, (300, 2)) + [4.6, -74.1]
    valores = coords[:, 0] * 100 + rng.normal(0, 0.1, 300)  # gradiente norte-sur
    r = spatial.morans_i(valores, coords, k=8, permutaciones=99)
    assert r["I"] > 0.5 and r["p_valor"] < 0.05
    z = spatial.getis_ord_gi_star(valores, coords, radio_km=1.5)
    assert z[np.argmax(valores)] > 1.96
