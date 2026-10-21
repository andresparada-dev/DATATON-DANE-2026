import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cenu import ciiu, oportunidad, schema, synthetic  # noqa: E402
from cenu.clients import ArcGISClient, NadaClient, SocrataClient  # noqa: E402


class Resp:
    def __init__(self, payload):
        self._p = payload
        self.status_code = 200

    def json(self):
        return self._p

    def raise_for_status(self):
        pass


def test_socrata_pagina_hasta_agotar(monkeypatch):
    filas = [{"cod": str(i)} for i in range(5)]
    llamadas = []

    def fake_get(url, params=None, timeout=None):
        llamadas.append(params)
        o, n = params["$offset"], params["$limit"]
        return Resp(filas[o:o + n])

    c = SocrataClient()
    monkeypatch.setattr(c.s, "get", fake_get)
    df = c.consultar("gdxc-w37w", pagina=2)
    assert len(df) == 5 and len(llamadas) == 3
    assert llamadas[0]["$order"] == ":id"


def test_socrata_respeta_limite(monkeypatch):
    c = SocrataClient()
    monkeypatch.setattr(c.s, "get", lambda url, params=None, timeout=None: Resp([{"a": 1}] * params["$limit"]))
    assert len(c.consultar("x", limite=7, pagina=5)) == 7


def test_nada_buscar(monkeypatch):
    c = NadaClient()
    payload = {"result": {"rows": [{"id": 875, "idno": "DANE-DIMPE-EMICRON-2024", "title": "EMICRON 2024", "year_start": 2024}]}}
    monkeypatch.setattr(c.s, "get", lambda url, params=None, timeout=None: Resp(payload))
    df = c.buscar("micronegocios")
    assert df.loc[0, "url"].endswith("/catalog/875")


def test_arcgis_pagina_y_extrae_xy(monkeypatch):
    c = ArcGISClient()
    feats = [{"attributes": {"id": i}, "geometry": {"x": -74.0, "y": 4.6}} for i in range(3)]

    def fake_get(url, params=None, timeout=None):
        o, n = params["resultOffset"], params["resultRecordCount"]
        page = feats[o:o + n]
        return Resp({"features": page, "exceededTransferLimit": o + n < len(feats)})

    monkeypatch.setattr(c.s, "get", fake_get)
    df = c.consultar("https://x/MapServer/0", pagina=2)
    assert len(df) == 3 and {"latitud", "longitud"} <= set(df.columns)


def test_marcar_categorias():
    d = pd.DataFrame({"ciiu": ["4773", "4711", "8790", "6201", None]})
    cats = oportunidad.marcar_categorias(d)
    assert cats.tolist()[:3] == ["Droguería / farmacia", "Tienda / minimercado", "Cuidado (asistencia social)"]
    assert pd.isna(cats.iloc[3]) and pd.isna(cats.iloc[4])


def test_desiertos_y_oportunidades():
    df = ciiu.enriquecer_ciiu(schema.normalizar(synthetic.generar(4000, semilla=3), verbose=False))
    bog = df[df["municipio"] == "Bogotá, D.C."]
    celdas, resumen = oportunidad.desiertos(bog, tam_celda_m=300, radio_m=500)
    fila = resumen.set_index("categoria").loc["Tienda / minimercado"]
    assert fila["unidades"] > 0 and 0 <= fila["pct_demanda_desierto"] <= 100
    top = oportunidad.top_oportunidades(celdas, "Droguería / farmacia", 5)
    assert (top["distancia_al_mas_cercano_m"] > 500).all()
    assert top["demanda"].is_monotonic_decreasing
