from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = "datatón-cenu-2026-toolkit/0.1 (+https://github.com/andresparada-dev/dataton-dane-2026)"


def sesion(reintentos: int = 4, backoff: float = 2.0) -> requests.Session:
    """Sesión con reintentos exponenciales (2s, 4s, 8s, 16s) ante 429/5xx y errores de red."""
    s = requests.Session()
    retry = Retry(total=reintentos, backoff_factor=backoff, status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET", "POST"))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.headers["User-Agent"] = USER_AGENT
    return s
