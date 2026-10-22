"""OpenStreetMap vía Overpass API: puntos de interés comerciales para complementar/validar el censo.

OSM no es fuente oficial y su cobertura es desigual, pero sirve para: validar georreferenciación,
contrastar cobertura (¿qué tiene OSM que no esté en el censo y viceversa?) y enriquecer con
paraderos, bancos, cajeros, colegios, hospitales (variables de accesibilidad).
"""

from __future__ import annotations

import pandas as pd

from .base import sesion

URL_OVERPASS = "https://overpass-api.de/api/interpreter"


def consultar_overpass(consulta: str, url: str = URL_OVERPASS, timeout: int = 180) -> pd.DataFrame:
    r = sesion().post(url, data={"data": consulta}, timeout=timeout)
    r.raise_for_status()
    filas = []
    for e in r.json().get("elements", []):
        lat = e.get("lat") or (e.get("center") or {}).get("lat")
        lon = e.get("lon") or (e.get("center") or {}).get("lon")
        filas.append({"osm_id": f"{e['type']}/{e['id']}", "latitud": lat, "longitud": lon, **e.get("tags", {})})
    return pd.DataFrame(filas)


def pois_comercio(sur: float, oeste: float, norte: float, este: float,
                  claves: tuple[str, ...] = ("shop", "amenity", "craft", "office")) -> pd.DataFrame:
    """POIs con etiquetas shop/amenity/craft/office dentro de un bbox (sur, oeste, norte, este).

    Ejemplo (Chapinero, Bogotá aprox.): pois_comercio(4.62, -74.08, 4.68, -74.03)
    """
    bbox = f"{sur},{oeste},{norte},{este}"
    partes = "\n".join(f'  nwr["{c}"]({bbox});' for c in claves)
    consulta = f"[out:json][timeout:120];\n(\n{partes}\n);\nout center tags;"
    return consultar_overpass(consulta)
