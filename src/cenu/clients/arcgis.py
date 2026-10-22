"""Cliente genérico para servicios ArcGIS REST (FeatureServer / MapServer).

El Geoportal del DANE y varias alcaldías (IDECA Bogotá, MEData Medellín) publican capas en ArcGIS.
Para descubrir capas: abrir la URL del servicio + "?f=pjson" en el navegador.
Consulta: <url_capa>/query?where=1=1&outFields=*&f=json&resultOffset=0&resultRecordCount=2000
"""

from __future__ import annotations

import pandas as pd

from .base import sesion


class ArcGISClient:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self.s = sesion()

    def info(self, url_capa: str) -> dict:
        r = self.s.get(url_capa, params={"f": "pjson"}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def consultar(self, url_capa: str, where: str = "1=1", campos: str = "*", geometria: bool = True,
                  pagina: int = 2000, limite: int | None = None, sr: int = 4326) -> pd.DataFrame:
        """Descarga atributos (y centroides x/y si hay geometría de puntos) paginando."""
        filas, offset = [], 0
        while True:
            n = pagina if limite is None else min(pagina, limite - offset)
            if n <= 0:
                break
            r = self.s.get(f"{url_capa.rstrip('/')}/query", params={
                "where": where, "outFields": campos, "returnGeometry": str(geometria).lower(),
                "outSR": sr, "f": "json", "resultOffset": offset, "resultRecordCount": n,
            }, timeout=self.timeout)
            r.raise_for_status()
            j = r.json()
            if "error" in j:
                raise RuntimeError(j["error"])
            feats = j.get("features", [])
            for f in feats:
                fila = dict(f.get("attributes", {}))
                g = f.get("geometry") or {}
                if "x" in g and "y" in g:
                    fila["longitud"], fila["latitud"] = g["x"], g["y"]
                filas.append(fila)
            offset += len(feats)
            if not feats or not j.get("exceededTransferLimit", len(feats) == n):
                break
        return pd.DataFrame(filas)

    def geojson(self, url_capa: str, where: str = "1=1", campos: str = "*", destino: str | None = None) -> dict:
        """Descarga como GeoJSON (útil para polígonos: manzanas, sectores, comunas)."""
        r = self.s.get(f"{url_capa.rstrip('/')}/query", params={
            "where": where, "outFields": campos, "f": "geojson", "outSR": 4326}, timeout=self.timeout)
        r.raise_for_status()
        if destino:
            with open(destino, "wb") as f:
                f.write(r.content)
        return r.json()
