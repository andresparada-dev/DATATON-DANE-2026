"""Cliente mínimo para la API SODA de datos.gov.co (plataforma Socrata).

Documentación SODA: https://dev.socrata.com/docs/endpoints.html
- Datos:     https://www.datos.gov.co/resource/<id-4x4>.json?$select=...&$where=...&$limit=...&$offset=...
- Catálogo:  https://api.us.socrata.com/api/catalog/v1?domains=www.datos.gov.co&q=<texto>
Un app token (gratuito, https://www.datos.gov.co/profile/edit/developer_settings) sube el límite de
peticiones; se lee de la variable de entorno SOCRATA_APP_TOKEN.
"""

from __future__ import annotations

import os

import pandas as pd

from .base import sesion


class SocrataClient:
    def __init__(self, dominio: str = "www.datos.gov.co", app_token: str | None = None, timeout: int = 60):
        self.dominio = dominio
        self.timeout = timeout
        self.s = sesion()
        token = app_token or os.getenv("SOCRATA_APP_TOKEN")
        if token:
            self.s.headers["X-App-Token"] = token

    def buscar(self, texto: str, limite: int = 20) -> pd.DataFrame:
        """Busca datasets en el catálogo del dominio. Devuelve id, nombre, entidad, actualización."""
        r = self.s.get("https://api.us.socrata.com/api/catalog/v1",
                       params={"domains": self.dominio, "search_context": self.dominio, "q": texto, "limit": limite},
                       timeout=self.timeout)
        r.raise_for_status()
        filas = []
        for item in r.json().get("results", []):
            res = item.get("resource", {})
            filas.append({
                "id": res.get("id"),
                "nombre": res.get("name"),
                "tipo": res.get("type"),
                "actualizado": res.get("data_updated_at") or res.get("updatedAt"),
                "entidad": (item.get("classification", {}).get("domain_metadata") or [{}])[0].get("value")
                if item.get("classification", {}).get("domain_metadata") else None,
                "url": item.get("permalink") or item.get("link"),
            })
        return pd.DataFrame(filas)

    def metadatos(self, dataset_id: str) -> dict:
        r = self.s.get(f"https://{self.dominio}/api/views/{dataset_id}.json", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def consultar(self, dataset_id: str, select: str | None = None, where: str | None = None,
                  order: str | None = None, group: str | None = None, limite: int | None = None,
                  pagina: int = 50_000, **filtros) -> pd.DataFrame:
        """Descarga un dataset (paginando) a DataFrame.

        Ejemplo: consultar("xxxx-xxxx", where="departamento='BOGOTÁ'", limite=1000)
        `filtros` se pasan como igualdades simples (?columna=valor).
        """
        url = f"https://{self.dominio}/resource/{dataset_id}.json"
        params = {k: v for k, v in {"$select": select, "$where": where, "$order": order, "$group": group}.items() if v}
        params.update(filtros)
        if not order and not group:
            params["$order"] = ":id"  # orden estable para paginar
        bloques, offset = [], 0
        while True:
            n = pagina if limite is None else min(pagina, limite - offset)
            if n <= 0:
                break
            r = self.s.get(url, params={**params, "$limit": n, "$offset": offset}, timeout=self.timeout)
            r.raise_for_status()
            datos = r.json()
            if not datos:
                break
            bloques.append(pd.DataFrame(datos))
            offset += len(datos)
            if len(datos) < n:
                break
        return pd.concat(bloques, ignore_index=True) if bloques else pd.DataFrame()

    def descargar_csv(self, dataset_id: str, destino: str) -> str:
        """Descarga el CSV completo (endpoint de exportación) en streaming; útil para tablas grandes."""
        url = f"https://{self.dominio}/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"
        with self.s.get(url, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            with open(destino, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        return destino
