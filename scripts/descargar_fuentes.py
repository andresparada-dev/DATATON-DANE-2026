#!/usr/bin/env python3
"""Descarga y prueba de fuentes oficiales (correr con internet: salas de la universidad / casa).

Subcomandos:
  smoke                         Prueba HTTP de las fuentes clave -> reports/smoke_fuentes.csv
  divipola                      DIVIPOLA municipios (datos.gov.co gdxc-w37w) -> data/referencia/
  socrata ID [--where] [--select] [--limite]   Cualquier dataset de datos.gov.co -> data/raw/<ID>.csv
  buscar-socrata "texto"        Busca datasets en datos.gov.co
  nada-buscar "texto"           Busca estudios en microdatos.dane.gov.co (ANDA)
  nada-variables ID             Diccionario de variables de un estudio ANDA (p. ej. 875 = EMICRON 2024)
  arcgis-listar [URL]           Lista servicios/capas de una carpeta ArcGIS (por defecto la carpeta CENU del DANE)
  arcgis-capa URL [--where]     Descarga una capa ArcGIS a GeoJSON (p. ej. manzanas MGN)
  osm S O N E                   POIs comerciales de OpenStreetMap en un bbox

IDs verificados por índice de búsqueda (ver docs/03_fuentes_datos_apis.md). Confirmar siempre las columnas
con `socrata ID --limite 5` antes de filtrar.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from cenu.clients import ArcGISClient, NadaClient, SocrataClient, pois_comercio, sesion  # noqa: E402

GEO_DANE = "https://geoportal.dane.gov.co/mparcgis/rest/services"
MGN2024 = "https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer"

DATASETS = {
    "gdxc-w37w": "DIVIPOLA - Códigos municipios (DANE)",
    "xaxy-8nri": "DIVIPOLA - Cabeceras y centros poblados (DANE)",
    "t7kp-7a7c": "DIVIPOLA - Departamentos geolocalizado (DANE)",
    "c82u-588k": "RUES - Personas naturales, jurídicas y ESAL (Confecámaras) ~9,4 M filas",
    "6cat-2gcs": "10.000 empresas más grandes (Supersociedades)",
    "bzeh-ecuk": "Estructura empresarial según municipio y tamaño",
    "jbjy-vk9h": "SECOP II - Contratos electrónicos",
}

SMOKE = {
    "DANE web": "https://www.dane.gov.co",
    "CENU resultados": "https://censoeconomiconacionalurbano.dane.gov.co/resultados/",
    "CENU difusión": "https://difusioncensoeconomiconacionalurbano.dane.gov.co/",
    "ANDA catálogo": "https://microdatos.dane.gov.co/index.php/catalog",
    "ANDA API búsqueda": "https://microdatos.dane.gov.co/index.php/api/catalog/search?sk=micronegocios&ps=5",
    "ANDA API EMICRON 2024": "https://microdatos.dane.gov.co/index.php/api/catalog/875",
    "ArcGIS DANE raíz": f"{GEO_DANE}?f=pjson",
    "ArcGIS carpeta CENU": f"{GEO_DANE}/CENU?f=pjson",
    "ArcGIS carpeta Conteo UE": f"{GEO_DANE}/CONTEO_UNIDADES_ECONOMICAS?f=pjson",
    "MGN 2024 manzana (215)": f"{MGN2024}/215?f=pjson",
    "MGN 2024 sector urbano (246)": f"{MGN2024}/246?f=pjson",
    "Socrata catálogo": "https://api.us.socrata.com/api/catalog/v1?domains=www.datos.gov.co&q=divipola&limit=1",
    **{f"datos.gov.co {k}": f"https://www.datos.gov.co/resource/{k}.json?$limit=1" for k in DATASETS},
    "Bogotá CKAN": "https://datosabiertos.bogota.gov.co/api/3/action/package_search?q=comercio&rows=1",
    "Overpass OSM": "https://overpass-api.de/api/status",
}


def smoke() -> None:
    s = sesion(reintentos=1)
    filas = []
    for nombre, url in SMOKE.items():
        try:
            r = s.get(url, timeout=30)
            filas.append({"fuente": nombre, "url": url, "http": r.status_code, "bytes": len(r.content),
                          "tipo": r.headers.get("content-type", "")[:40]})
        except Exception as e:  # noqa: BLE001 — se reporta cualquier fallo de red
            filas.append({"fuente": nombre, "url": url, "http": None, "bytes": 0, "tipo": type(e).__name__})
        print(f"{str(filas[-1]['http']):>5}  {nombre}")
    out = RAIZ / "reports" / "smoke_fuentes.csv"
    out.parent.mkdir(exist_ok=True)
    pd.DataFrame(filas).to_csv(out, index=False)
    print("->", out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("smoke")
    sub.add_parser("divipola")
    p = sub.add_parser("socrata")
    p.add_argument("id")
    p.add_argument("--where")
    p.add_argument("--select")
    p.add_argument("--limite", type=int, default=None)
    p = sub.add_parser("buscar-socrata")
    p.add_argument("texto")
    p = sub.add_parser("nada-buscar")
    p.add_argument("texto")
    p = sub.add_parser("nada-variables")
    p.add_argument("id")
    p = sub.add_parser("arcgis-listar")
    p.add_argument("url", nargs="?", default=f"{GEO_DANE}/CENU")
    p = sub.add_parser("arcgis-capa")
    p.add_argument("url")
    p.add_argument("--where", default="1=1")
    p.add_argument("--salida", default=None)
    p = sub.add_parser("osm")
    for c in ("sur", "oeste", "norte", "este"):
        p.add_argument(c, type=float)
    a = ap.parse_args()

    raw = RAIZ / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    if a.cmd == "smoke":
        smoke()
    elif a.cmd == "divipola":
        df = SocrataClient().consultar("gdxc-w37w")
        ruta = RAIZ / "data" / "referencia" / "divipola_municipios.csv"
        df.to_csv(ruta, index=False)
        print(df.head(), "\n->", ruta, len(df), "filas")
    elif a.cmd == "socrata":
        df = SocrataClient().consultar(a.id, select=a.select, where=a.where, limite=a.limite)
        ruta = raw / f"{a.id}.csv"
        df.to_csv(ruta, index=False)
        print(df.head(), "\ncolumnas:", list(df.columns), "\n->", ruta, len(df), "filas")
    elif a.cmd == "buscar-socrata":
        print(SocrataClient().buscar(a.texto).to_string())
    elif a.cmd == "nada-buscar":
        print(NadaClient().buscar(a.texto).to_string())
    elif a.cmd == "nada-variables":
        v = NadaClient().variables(a.id)
        ruta = RAIZ / "data" / "referencia" / f"anda_{a.id}_variables.csv"
        v.to_csv(ruta, index=False)
        print(v.head(30).to_string(), "\n->", ruta)
    elif a.cmd == "arcgis-listar":
        info = ArcGISClient().info(a.url)
        for k in ("folders", "services", "layers"):
            for x in info.get(k, []):
                print(k[:-1], json.dumps(x, ensure_ascii=False))
    elif a.cmd == "arcgis-capa":
        ruta = Path(a.salida) if a.salida else raw / "capa_arcgis.geojson"
        gj = ArcGISClient().geojson(a.url, where=a.where, destino=str(ruta))
        print(len(gj.get("features", [])), "features ->", ruta,
              "(máx. por página = maxRecordCount; para más, usar ArcGISClient.consultar o esridump)")
    elif a.cmd == "osm":
        df = pois_comercio(a.sur, a.oeste, a.norte, a.este)
        ruta = raw / "osm_pois.csv"
        df.to_csv(ruta, index=False)
        print(len(df), "POIs ->", ruta)


if __name__ == "__main__":
    main()
