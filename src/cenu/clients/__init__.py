"""Clientes HTTP para fuentes de datos abiertos de Colombia (sin dependencias externas salvo requests)."""

from .base import sesion
from .socrata import SocrataClient
from .nada import NadaClient
from .arcgis import ArcGISClient
from .overpass import consultar_overpass, pois_comercio

__all__ = ["sesion", "SocrataClient", "NadaClient", "ArcGISClient", "consultar_overpass", "pois_comercio"]
