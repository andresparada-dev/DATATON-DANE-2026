"""Cliente para el Archivo Nacional de Datos (ANDA) del DANE, construido sobre NADA (IHSN / Banco Mundial).

Catálogo web: https://microdatos.dane.gov.co/index.php/catalog
API NADA (pública, solo lectura):
    /index.php/api/catalog/search?sk=<texto>&ps=<tamaño>&page=<n>
    /index.php/api/catalog/<idno>                  metadatos del estudio
    /index.php/api/catalog/<idno>/variables        lista de variables (diccionario)
    /index.php/api/catalog/<idno>/data_files       archivos de datos
Los microdatos se descargan desde la pestaña "Obtener microdatos" del estudio (a veces exige registro).
"""

from __future__ import annotations

import pandas as pd

from .base import sesion


class NadaClient:
    def __init__(self, base: str = "https://microdatos.dane.gov.co/index.php", timeout: int = 60):
        self.base = base.rstrip("/")
        self.timeout = timeout
        self.s = sesion()

    def _get(self, ruta: str, **params) -> dict:
        r = self.s.get(f"{self.base}/api/{ruta.lstrip('/')}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def buscar(self, texto: str, por_pagina: int = 50) -> pd.DataFrame:
        j = self._get("catalog/search", sk=texto, ps=por_pagina)
        filas = j.get("result", {}).get("rows", [])
        cols = ["id", "idno", "title", "year_start", "year_end", "nation", "repositoryid", "created", "changed"]
        df = pd.DataFrame(filas)
        df = df[[c for c in cols if c in df.columns]]
        if "id" in df.columns:
            df["url"] = self.base + "/catalog/" + df["id"].astype(str)
        return df

    def estudio(self, idno: str) -> dict:
        return self._get(f"catalog/{idno}")

    def variables(self, idno: str) -> pd.DataFrame:
        j = self._get(f"catalog/{idno}/variables")
        return pd.DataFrame(j.get("variables", j if isinstance(j, list) else []))

    def archivos(self, idno: str) -> pd.DataFrame:
        j = self._get(f"catalog/{idno}/data_files")
        datos = j.get("datafiles", j)
        return pd.DataFrame(list(datos.values()) if isinstance(datos, dict) else datos)
