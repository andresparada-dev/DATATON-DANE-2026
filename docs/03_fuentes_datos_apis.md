# 03 · Catálogo técnico de APIs y fuentes oficiales de datos para la Datatón CENU (DANE)

**Fecha de corte:** 21 de octubre de 2026
**Archivo CSV asociado:** [`data/catalogo_fuentes.csv`](../data/catalogo_fuentes.csv)

> **Nota de nombre.** La operación oficial se llama **Censo Económico Nacional Urbano (CENU) 2024**. La recolección se hizo entre 2024 y 2025, y los resultados (preliminares, nov-2024 a abr-2026) se difunden en 2025 y 2026. "CENU 2026" es el nombre de la datatón, no de la operación. Ver `01_cenu_2026.md`.

---

## 0. Cómo se verificó (léalo antes de usar el catálogo)

Esta sesión tuvo dos limitaciones fuertes, y conviene tenerlas en cuenta:

1. **WebFetch no resolvió DNS** (`getaddrinfo ENOTFOUND`) para *ningún* dominio `.gov.co` ni para `api.us.socrata.com`, `dev.socrata.com`, `inegi.org.mx`, `overpass-api.de`, `wiki.openstreetmap.org` ni `ihsn.github.io`. **Sí funcionó** con `github.com`, `raw.githubusercontent.com` y `gist.github.com`. El `curl` del contenedor solo llega a `pypi.org` (el proxy devuelve 403 a datos.gov.co).
2. **Se agotó el cupo de WebSearch** (200 búsquedas por turno, compartido entre agentes) antes de terminar. Las fuentes del bloque 5 (TerriData, MinCIT, DIAN, REDATAM, CIIU) quedaron sin verificar.

Por eso cada fuente lleva uno de estos niveles:

| Nivel | Significado |
|---|---|
| **SI-fetch** | Leí el contenido real: código fuente en GitHub, JSON de PyPI o especificación OpenAPI. |
| **SI-indice** | La URL o el ID exacto aparecieron en resultados del buscador, apuntando al dominio oficial, con título y metadatos que coinciden. **No** hice una petición en vivo al endpoint. |
| **PARCIAL** | Existe la fuente o el patrón, pero falta confirmar un parámetro, un campo o una URL concreta. |
| **NO VERIFICADO** | Viene de conocimiento previo. Hay que confirmarlo antes de usarlo. |

**Primera tarea del equipo, con red abierta:** correr el script de humo de la sección 9. Valida en un solo paso todos los endpoints marcados SI-indice.

---

## 1. datos.gov.co (plataforma Socrata / Tyler Data & Insights)

### 1.1 Cómo funciona la API SODA

| Elemento | Valor | Verificación |
|---|---|---|
| Endpoint de datos (SODA 2.x) | `https://www.datos.gov.co/resource/{4x4}.json` (también `.csv` y `.geojson`) | SI-fetch: sodapy usa `DEFAULT_API_PATH = "/resource/"`, y el MCP `colombian-open-data-mcp` usa `RESOURCE_API_BASE = "https://www.datos.gov.co/resource"`. También SI-indice: aparecen URLs como `https://www.datos.gov.co/resource/c82u-588k.csv`. |
| Descarga completa | `https://www.datos.gov.co/api/views/{4x4}/rows.csv?accessType=DOWNLOAD` | SI-indice (aparece para `c82u-588k`, `72fa-9d9m` y `9mn6-ky8i`). |
| Exportación v3 | `https://www.datos.gov.co/api/v3/views/{4x4}/export.csv?accessType=DOWNLOAD` | SI-indice. |
| Metadatos y columnas | `https://www.datos.gov.co/api/views/{4x4}.json` y `https://www.datos.gov.co/api/views/metadata/v1/{4x4}` | SI-fetch (código de `colombian-open-data-mcp/socrata.py`). |
| Permalink | `https://www.datos.gov.co/d/{4x4}` | SI-fetch (mismo código) y SI-indice (`/d/86xb-sqr3`). |
| OData | `https://www.datos.gov.co/OData.svc/{4x4}` | SI-indice (`/OData.svc/ctcp-462n`). |
| Ficha para desarrolladores | `https://dev.socrata.com/foundry/www.datos.gov.co/{4x4}` | SI-fetch (citada en gist de RUES). |
| Catálogo global (Discovery API) | `https://api.us.socrata.com/api/catalog/v1?domains=www.datos.gov.co&search_context=www.datos.gov.co&q=...&only=dataset&limit=..&offset=..` | SI-fetch (constantes en `socrata.py`). Sin respuesta en vivo. |
| Catálogo por dominio | `https://www.datos.gov.co/api/catalog/v1?q=...` | SI-fetch (sodapy: `DATASETS_PATH = "/api/catalog/v1"` sobre el dominio). |
| Facetas | `https://www.datos.gov.co/api/catalog/v1/domain_categories`, `/domain_tags`, `/owners` | SI-fetch (código MCP). |
| App token | Cabecera `X-App-Token: <token>` o parámetro `$$app_token=<token>` | SI-fetch para la cabecera (sodapy envía `X-App-token`). SI-indice para el parámetro (aparece `$$app_token=YOURAPIKEY` en el README de `Macorreag/colombiaData`). |
| Límite por defecto | 1000 filas por petición (`DEFAULT_LIMIT = 1000` en sodapy). Para paginar se usan `$limit` y `$offset` con `$order` estable. | SI-fetch (sodapy). El tope máximo de SODA no pudo verificarse (dev.socrata.com inaccesible). |

**Cláusulas SoQL** (sintaxis estándar de Socrata; la documentación oficial no se pudo abrir en esta sesión): `$select`, `$where`, `$order`, `$group`, `$having`, `$limit`, `$offset`, `$q` (texto libre) y filtros simples `campo=valor`. Ejemplos:

```bash
# Primeras 2 filas
curl -s "https://www.datos.gov.co/resource/gdxc-w37w.json?\$limit=2"

# Filtro simple por campo (patrón tomado del README de Macorreag/colombiaData)
curl -s "https://www.datos.gov.co/resource/xdk5-pm3f.csv?\$select=dpto&nom_mpio=Florencia"

# Con token y paginación
curl -s -H "X-App-Token: $SOCRATA_APP_TOKEN" \
  "https://www.datos.gov.co/resource/c82u-588k.json?\$select=codigo_camara,matricula,razon_social&\$limit=50000&\$offset=0&\$order=:id"

# Consultar por NIT (patrón del gist YoanSinH, SI-fetch)
curl -s "https://www.datos.gov.co/resource/c82u-588k.json?\$select=codigo_camara,matricula&nit=901998870"

# Columnas reales de un dataset (hacerlo SIEMPRE antes de agregar)
curl -s "https://www.datos.gov.co/api/views/c82u-588k.json" | jq '.columns[] | {fieldName, dataTypeName}'

# Buscar datasets en el catálogo
curl -s "https://api.us.socrata.com/api/catalog/v1?domains=www.datos.gov.co&search_context=www.datos.gov.co&q=camara%20de%20comercio&only=dataset&limit=50"
```

```python
# pip install sodapy pandas   (sodapy 2.2.0 confirmado en PyPI)
import os, pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", os.getenv("SOCRATA_APP_TOKEN"), timeout=60)  # token puede ser None
meta = client.get_metadata("c82u-588k")                      # columnas y descripción
rows = client.get("gdxc-w37w", limit=2)                      # muestra
df = pd.DataFrame.from_records(client.get_all("gdxc-w37w"))  # generador paginado (1000 por página)

# Agregación del lado del servidor (SoQL $select/$group). Validar antes los nombres de campo con get_metadata.
agg = client.get("c82u-588k",
                 select="codigo_camara, count(*) as n",
                 group="codigo_camara", limit=100)
```

Licencia: cada dataset declara la suya. La más común en datos.gov.co es CC BY-SA 4.0 (confirmado en el índice para `t7kp-7a7c` y `p6dx-8zbt`). Autenticación: no se necesita para leer. El app token es gratuito y evita el *throttling*.

### 1.2 Datasets verificados en datos.gov.co

| ID 4x4 | Nombre | Publicador | Notas | Verif. |
|---|---|---|---|---|
| `gdxc-w37w` | DIVIPOLA - Códigos municipios | DANE (Mapas Nacionales) | Corte más reciente en el índice: 30-dic-2024. Unas 1.122 filas (municipios, ANM y distritos). Página: `https://www.datos.gov.co/Mapas-Nacionales/DIVIPOLA-C-digos-municipios/gdxc-w37w` | SI-indice y SI-fetch (README de `Macorreag/colombiaData`) |
| `82nj-9vvy` | VISTA_DIVIPOLA - Códigos municipios | DANE | Vista derivada de la anterior | SI-indice |
| `xaxy-8nri` | DIVIPOLA - Códigos cabeceras - Centros poblados | DANE | 9 columnas: códigos y nombres de departamento, municipio y centro poblado, tipo (CM = cabecera municipal, CP = centro poblado, ANM = área no municipalizada) y coordenadas | SI-indice |
| `t7kp-7a7c` | DIVIPOLA - Códigos departamentos geolocalizado | DANE (Geoportal) | CC BY-SA 4.0, actualizado el 18-may-2026 | SI-indice |
| `xdk5-pm3f` | (DIVIPOLA municipios, otra versión) | — | Se usa en el ejemplo `?$select=dpto&nom_mpio=Florencia` | SI-fetch (README GitHub). Título sin confirmar. |
| `kqut-4h4r` | Directorio Georreferenciado de Entidades Públicas - DIVIPOLA | Función Pública | | SI-indice |
| `543m-7w2p` | Manzana (MGN versión 2025, shapefile) | DANE | Enlaza al hub CDGE de DANE | SI-indice |
| `c82u-588k` | **Personas Naturales, Personas Jurídicas y Entidades Sin Ánimo de Lucro (RUES)** | Confecámaras | Extracto del Registro Mercantil sincronizado en el RUES. **Unos 9,4 millones de filas** (9.436.330 al 04-oct-2026, según un issue de GitHub). Campos confirmados: `codigo_camara`, `camara_comercio`, `matricula`, `inscripcion_proponente`, `razon_social`, `nit`, `estado_matricula`, `fecha_matricula` (formato AAAAMMDD), `ultimo_ano_renovado`, `cod_ciiu_act_econ_pri`. **Atención:** un comentario de usuario dice que no se actualiza desde abril de 2024, aunque el conteo de filas sí cambia entre 2025 y 2026. Hay que confirmarlo con `rowsUpdatedAt` en `/api/views/c82u-588k.json`. | SI-indice y SI-fetch (gists e issue) |
| `6cat-2gcs` | 10.000 Empresas más Grandes del País | Supersociedades | 14 columnas: NIT, razón social, región, departamento y ciudad de domicilio, CIIU, macrosector, ingresos operacionales, ganancia o pérdida, activos, pasivos, patrimonio y año de corte. Actualizado en sep-2026. | SI-indice y SI-fetch (README de `santigg23/api_datos_libres_empresas_col`) |
| `pfdp-zks5` | Estados Financieros NIIF - Estado de Situación Financiera | Supersociedades | Formato largo (NIT, fecha de corte, concepto, valor). Actualizado en jul-2026. | SI-indice |
| `6hqw-m3dm` | Estados Financieros NIIF - Carátula | Supersociedades | Formato largo | SI-indice |
| `y3gh-x5g7` | Estados Financieros NIIF - Otro Resultado Integral | Supersociedades | | SI-indice |
| `ctcp-462n` | Estados Financieros NIIF - Estado de Flujo de Efectivo | Supersociedades | Se vio por OData | SI-indice |
| `prwj-nzxa` | (posible Estado de Resultado Integral NIIF) | Supersociedades | Aparece en la misma búsqueda, sin título visible | PARCIAL |
| `bzeh-ecuk` | Estructura empresarial según municipio y tamaño de empresa | (Comercio, Industria y Turismo) | El título es el que mejor encaja con la datatón, pero no se vieron sus columnas | PARCIAL |
| `gwqv-sqvs` | Base de datos de empresas y/o entidades activas - Jurisdicción Cámara de Comercio de Ibagué (corte 30-sep-2026) | CC Ibagué | Tamaño por ingresos (Decreto 1074/2015) y municipio | SI-indice |
| `wf53-j577` | Empresas Cámara de Comercio de Bucaramanga | CC Bucaramanga | Tamaño, municipio y departamento | SI-indice |
| `3vbk-w3sc` | Códigos CIIU por municipio | CC Ocaña | Conteos por municipio, CIIU y forma jurídica | SI-indice |
| `y69t-3r2t` | Empresas registradas | (Sincelejo) | Con CIIU | SI-indice |
| `xrhy-spbe` | SAS y EU - Cámara de Comercio Barranquilla | CC Barranquilla | | SI-indice |
| `8ae5-pgsh` | Base de datos PYMES Cámara de Comercio Piedemonte Araucano | CC Piedemonte Araucano | | SI-indice |
| `86xb-sqr3` | Establecimientos de comercio (La Unión) | Municipio | De 2018, pequeño | SI-indice |
| `jbjy-vk9h` | SECOP II - Contratos Electrónicos | ANCP-CCE | Unos 5,9 millones de filas | SI-indice y SI-fetch (README `radicadouno-mcp`) |
| `p6dx-8zbt` | SECOP II - Procesos de Contratación | ANCP-CCE | Entre 8,5 y 9,2 millones de filas, 59 columnas, CC BY-SA 4.0 | SI-indice y SI-fetch |
| `p8vk-huva` | SECOP II - Contratos Electrónicos ACTIVOS (vista) | ANCP-CCE | 49 columnas | SI-indice |
| `d9na-abhe` | SECOP II - BPIN por Proceso | ANCP-CCE | | SI-indice |
| `7294-7mwg` | Encuesta de Micronegocios - EMICRON - 2025 (ficha) | DANE | Ficha de metadatos que enlaza a microdatos.dane.gov.co | SI-indice |
| `qwcq-r679`, `j4cz-rzbx`, `h98w-pe4v`, `wecr-97j3`, `mcpt-3dws`, `gifa-4us7` | GEIH 2023, 2022, 2021, 2020 y genéricas (fichas) | DANE | Fichas de metadatos; los microdatos están en ANDA | SI-indice |
| `7qmw-skyg` | Medición de Pobreza Monetaria y Desigualdad 2025 | DANE | | SI-indice |

**No encontrado:** ningún dataset del **CENU** en datos.gov.co, ni de licencias de funcionamiento o de informalidad agregada por municipio. Tampoco apareció un "RUES establecimientos de comercio" nacional distinto de `c82u-588k`.

---

## 2. Microdatos DANE: ANDA / NADA

### 2.1 Portal y API

- Portal: `https://microdatos.dane.gov.co/index.php/catalog` (570 operaciones y 224.012 variables al 03-sep-2026, SI-indice).
- Exportación del catálogo completo (SI-indice): `https://microdatos.dane.gov.co/index.php/catalog/export/print?collection[]=&ps=5000&sort_by=proddate&sort_order=desc`
- Fichas: `/index.php/catalog/{id}`, `/catalog/{id}/study-description`, `/catalog/{id}/related-materials`, `/catalog/{id}/get-microdata`, `/catalog/{id}/data-dictionary/F{n}` y `/catalog/{id}/variable/F{n}/V{m}` (todas SI-indice).
- **API NADA.** La especificación OpenAPI oficial del IHSN (`ihsn/nada/api-documentation/catalog/openapi.yaml`, SI-fetch) define el servidor `/index.php/api` con estas rutas, todas GET:
  - `/catalog/search` con parámetros `sk`, `from`, `to`, `collection`, `country`, `dtype`, `ps`, `page`, `sort_by`, `sort_order`, `format`, `sid`, `repo`, `varcount`, `created`, `include_facets`, …
  - `/catalog/{IDNo}` (parámetro `id_format`), `/catalog/{IDNo}/data_files`, `/catalog/{IDNo}/data_files/{fileId}/variables`
  - `/catalog/{IDNo}/variables` (`sk`, `ps`, `page`), `/catalog/{IDNo}/variables/{varId}`, `/catalog/variables` (búsqueda transversal)
  - `/catalog/collections`, `/catalog/collections/{repoId}`, `/catalog/latest`, `/catalog/stats`, `/catalog/data_access_codes`
  - `/catalog/ddi/{IDNo}` (XML DDI) y `/catalog/json/{IDNo}`
  - Otros portales NADA (Banco Mundial, FAO, OIT) usan exactamente `…/index.php/api/catalog` (SI-fetch, código de `nadaverse`). **Que la instancia del DANE exponga estas rutas es NO VERIFICADO en vivo**, pero el portal es NADA (rutas `/index.php/catalog/...` idénticas).
- Acceso: los microdatos anonimizados de uso público son **gratuitos con registro** (SI-indice). Algunas operaciones económicas (EAM, por ejemplo) están bajo "manejo especial por reserva estadística" (Ley 79/1993, art. 5). La descarga de archivos exige iniciar sesión, así que no es una API abierta.
- Formatos: normalmente ZIP con CSV, SAV (SPSS) y DTA (Stata) por módulo (NO VERIFICADO para cada estudio). Se leen con `pyreadstat` o `pandas`.

```bash
curl -s "https://microdatos.dane.gov.co/index.php/api/catalog/search?sk=micronegocios&ps=50&format=json"
curl -s "https://microdatos.dane.gov.co/index.php/api/catalog/875?id_format=id"
curl -s "https://microdatos.dane.gov.co/index.php/api/catalog/875/variables?id_format=id&ps=500"
curl -s "https://microdatos.dane.gov.co/index.php/api/catalog/variables?sk=CIIU&ps=100"
```

```python
import requests, pandas as pd
BASE = "https://microdatos.dane.gov.co/index.php/api/catalog"
r = requests.get(f"{BASE}/search", params={"sk": "micronegocios", "ps": 100, "format": "json"}, timeout=60)
studies = pd.json_normalize(r.json()["result"]["rows"])   # estructura NADA 5; validar claves
vars_ = requests.get(f"{BASE}/875/variables", params={"id_format": "id", "ps": 1000}).json()
# Microdatos descargados a mano (ZIP) -> pyreadstat
import pyreadstat
df, meta = pyreadstat.read_sav("Modulo_identificacion.sav")   # nombre de archivo ilustrativo
```

### 2.2 IDs de catálogo confirmados (SI-indice)

| Operación | ID catálogo | URL |
|---|---|---|
| EMICRON 2025 | **914** | https://microdatos.dane.gov.co/index.php/catalog/914 |
| EMICRON 2024 | **875** | https://microdatos.dane.gov.co/index.php/catalog/875 |
| EMICRON 2023 | **832** | https://microdatos.dane.gov.co/index.php/catalog/832 |
| EMICRON 2022 | **796** | https://microdatos.dane.gov.co/index.php/catalog/796 |
| EMICRON 2021 | **742** | https://microdatos.dane.gov.co/catalog/742 |
| EMICRON 2020 | **712** | https://microdatos.dane.gov.co/catalog/712 |
| EMICRON 2019 | **681** | https://microdatos.dane.gov.co/index.php/catalog/681 |
| GEIH 2026 | **900** | https://microdatos.dane.gov.co/index.php/catalog/900 |
| GEIH 2025 | **853** | https://microdatos.dane.gov.co/index.php/catalog/853 |
| GEIH 2024 (DANE-DIMPE-GEIH-2024) | **819** | https://microdatos.dane.gov.co/index.php/catalog/819 |
| GEIH 2023 | **782** | https://microdatos.dane.gov.co/index.php/catalog/782 |
| GEIH factores de expansión departamentales 2007-2025 | **789** | https://microdatos.dane.gov.co/index.php/catalog/789 |
| Pobreza monetaria 2024 | **874** | https://microdatos.dane.gov.co/index.php/catalog/874 |
| ECV 2024 | **861** | https://microdatos.dane.gov.co/index.php/catalog/861 |
| CNPV 2018 (incluye material del MGN integrado con censo) | **643** | https://microdatos.dane.gov.co/index.php/catalog/643 |
| Censo General 2005 (incluye módulo de unidades económicas, CIIU Rev.3 `E16_CIIURV3`) | **421** | https://microdatos.dane.gov.co/index.php/catalog/421 |
| Censo 1993 | 113 | https://microdatos.dane.gov.co/index.php/catalog/113 |
| 3er Censo Nacional Agropecuario 2014 | **513** | https://microdatos.dane.gov.co/index.php/catalog/513 |
| EAM (Encuesta Anual Manufacturera; varias vigencias) | 802, 836, 871, 888 | Por ejemplo, https://microdatos.dane.gov.co/index.php/catalog/871/get-microdata. Existe la ficha DANE-DIMPE-EAM-2023 con el archivo `BDATOS-EAM-2023.zip`, pero no se pudo confirmar qué ID corresponde a cada año. |
| Encuesta Ambiental Industrial 2023 | 880 | |
| Censo de Edificaciones CEED 2007-2026 II | 873 | |
| Coordenada Urbana 2014-2016 | 428 | |
| Colección Comercio interno | `CII-Microdatos` | https://microdatos.dane.gov.co/index.php/catalog/CII-Microdatos |
| **CENU 2024** | **No encontrado** | No apareció ficha del CENU en el catálogo. La ficha metodológica menciona como producto "bases de microdatos anonimizadas", sin fecha. |
| Directorio Estadístico de Empresas (DEE) | No está en ANDA | Se publica por geovisor y descargas agregadas (ver 3.4) |

---

## 3. Geoportal DANE: MGN, DIVIPOLA y servicios ArcGIS

### 3.1 ArcGIS REST (ArcGIS Server 11.3)

- Raíces (SI-indice): `https://geoportal.dane.gov.co/mparcgis/rest/services` y `https://portalgis.dane.gov.co/mparcgis/rest/services`. Info del servidor: `https://geoportal.dane.gov.co/mparcgis/rest/info` (seguridad por token habilitada; los servicios públicos se consultan sin token).
- Carpetas vistas en la raíz: `Divipola`, `MGN1993` … `MGN2025`, **`CENU`**, **`CONTEO_UNIDADES_ECONOMICAS`**, `Grilla_DANE`, `INDICADORES_*`, `TestAnalitica`, `Serv_niveles_geograficos`. **No se pudo listar el contenido de `CENU` ni de `CONTEO_UNIDADES_ECONOMICAS`.** Es lo primero que hay que abrir con red: `.../rest/services/CENU?f=pjson`.
- Servicios confirmados (SI-indice):

| Servicio | URL | Capas y notas |
|---|---|---|
| DIVIPOLA MGN 2025 | `https://portalgis.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2025/FeatureServer` (también `/layers` en geoportal.dane.gov.co) | Capa 319 = Departamento |
| DIVIPOLA MGN 2024 | `https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2024/MapServer` y `/FeatureServer/layers` | MaxRecordCount 2000. Formatos JSON, geoJSON y PBF. |
| **Capas MGN 2024 (urbano)** | `https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer` | **246 = Sector Urbano, 214 = Sección Urbana, 215 = Manzana** |
| Entidades territoriales y áreas metropolitanas | `https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_EntidadesTerritorialesyAM_SE/MapServer` | Grupo "MGN Urbano" con sector, sección y manzana censal |
| Deptos, municipios y ANM 2018 | `https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DeptosMpiosANM_2018/MapServer` | MaxRecordCount 1000 |
| MGN 1994 municipio | `https://geoportal.dane.gov.co/mparcgis/rest/services/MGN1994/Serv_Capas_MGN_1994/FeatureServer/317` | Campo `MPIO_CCDGO` (código DANE del municipio) |

Ejemplo de consulta a una capa (sintaxis estándar de ArcGIS REST; los parámetros coinciden con los del cliente `esri.py`, SI-fetch):

```bash
# Conteo de manzanas MGN2024 de Bogotá (validar antes el nombre de campo con .../215?f=pjson)
curl -s "https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer/215/query?where=MPIO_CDPMP%3D%2711001%27&returnCountOnly=true&f=json"

# Página de 2000 manzanas en GeoJSON
curl -s "https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer/215/query?where=1%3D1&outFields=*&outSR=4326&resultOffset=0&resultRecordCount=2000&f=geojson"
```

```python
# pip install esridump geopandas   (esridump 1.13.0 en PyPI: descarga paginada de capas Esri)
from esridump.dumper import EsriDumper
import geopandas as gpd
url = "https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer/246"  # sector urbano
feats = list(EsriDumper(url, extra_query_args={"where": "DPTO_CCDGO='11'"}))  # validar el campo
gdf = gpd.GeoDataFrame.from_features(feats, crs="EPSG:4326")
```

> Los nombres de campo `MPIO_CDPMP` y `DPTO_CCDGO` para las capas 215 y 246 son **NO VERIFICADOS**. El único confirmado es `MPIO_CCDGO`, en MGN1994. El manual del MGN dice que el código de manzana censal tiene 22 posiciones y que las posiciones 21 y 22 son la manzana. Antes de consultar, lea `.../MapServer/215?f=pjson`.

### 3.2 Hub ArcGIS del DANE (CDGE)

- `https://cdge-dane-danehub.hub.arcgis.com/datasets/1f88b146756f4a6dac586c813b7040b3_215` es "Manzana - MGN integrado, versión 2024" (SI-indice). Los Hub suelen ofrecer descarga CSV, GeoJSON, SHP y KML, y una API GeoService (NO VERIFICADO para este ítem).

### 3.3 Descargas del Geoportal (SHP, GPKG y XLSX)

| Recurso | URL | Verif. |
|---|---|---|
| Página de descarga de datos geoestadísticos (conteo de unidades económicas por municipio 2021, SHP y GeoJSON) | `https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/?cod=45` | SI-indice |
| Página de descarga provisional (MGN2021, MGN2018 en SHP y déficit habitacional por manzana) | `https://www.dane.gov.co/files/geoportal-provisional/index.html` | SI-indice |
| Manual de uso MGN 2023 | `https://geoportal.dane.gov.co/descargas/mgn_2023/MGN2023_ManualDeUso.pdf` | SI-indice |
| Guía de descarga MGN | `https://geoportal.dane.gov.co/descargas/descarga_mgn/GuiaDescargaVisualiz_CO.pdf` | SI-indice |
| Catálogo de geovisores y servicios (PDF) | `https://geoportal.dane.gov.co/descargas/mmra/CatalogoGeoportal-GeovisoresServicios.pdf` | SI-indice |
| Listado DIVIPOLA en Excel (`Listados_DIVIPOLA.xlsx`) | Se cita en la respuesta PQR del DANE `https://www.dane.gov.co/files/pqr/Respuesta-202510034970.pdf`. No se conoce la URL directa. | PARCIAL |

### 3.4 Geovisores

| Geovisor | URL | Verif. |
|---|---|---|
| Consulta del MGN | `https://geoportal.dane.gov.co/geovisores/territorio/mgn-marco-geoestadistico-nacional/` | SI-indice |
| Servicios web geográficos | `https://geoportal.dane.gov.co/geovisores/territorio/servicios-web-geograficos/` | SI-indice |
| Directorio Estadístico de Empresas (empresas activas, solo personas jurídicas; exporta CSV agregado con `;` y Excel) | `https://geoportal.dane.gov.co/geovisores/economia/directorio-estadistico-de-empresas/` | SI-indice |
| Geovisor de Estadísticas Integradas del CENU | Lo menciona el Geoportal, sin URL directa | PARCIAL |
| Portal MGN | `https://geoportal.dane.gov.co/mgn/` | SI-indice |

---

## 4. DANE web: CENU, CNUE, boletines y documentación

| Recurso | URL | Verif. |
|---|---|---|
| CENU - resultados preliminares (2.005.613 unidades económicas visibles en 1.102 municipios; periodo de referencia 2023) | `https://censoeconomiconacionalurbano.dane.gov.co/resultados/` | SI-indice |
| CENU - sitio de difusión | `https://difusioncensoeconomiconacionalurbano.dane.gov.co/` | SI-indice |
| CENU - documento metodológico (nov-2025) | `https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/documento-metodologico-cenu-20251110.pdf` | SI-indice |
| CENU - ficha técnica | `https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf` | SI-indice |
| CENU - página DANE | `https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/censo-economico-de-colombia/censo-economico-nacional-urbano` | SI-indice |
| CENU - boletín sectorial (patrón `files/operaciones/CENU/`) | `https://www.dane.gov.co/files/operaciones/CENU/bol-CENU-Turismo-2023.pdf` | SI-indice |
| Conteo Nacional de Unidades Económicas 2021 (XLSX por departamento y municipio, geovisor) | `https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/censo-economico-de-colombia/conteo-de-unidades-economicas-2021` | SI-indice |
| EMICRON - boletines y presentaciones (patrón `files/operaciones/EMICRON/{tipo}-EMICRON-{periodo}.pdf`) | `https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2024.pdf`, `bol-Departamentos-EMICRON-2024.pdf`, `bol-EMICRON-IVtrim2024.pdf`, `pres-EMICRONVendedoresAmbulantes-2025.pdf` | SI-indice. Los anexos XLSX probablemente siguen el patrón `anex-EMICRON-{periodo}.xlsx` (**NO VERIFICADO**). |
| Directorio Estadístico de Empresas - ficha metodológica | `https://bibliotecadoctecnica.dane.gov.co/static/documentos/DIG/DEE/DEE_Ficha%20metodol%C3%B3gica.pdf` | SI-indice |
| Biblioteca de documentación técnica (buscador) | `https://bibliotecadoctecnica.dane.gov.co/inventario/buscador` | SI-indice |
| REDATAM (CNPV 2018 y 2005) | El DANE ofrece un sistema REDATAM para los censos 2005 y 2018 (SI-indice). La URL exacta del motor (`systema*.dane.gov.co/bincol/RpWebEngine.exe/...`) es **NO VERIFICADO**. | PARCIAL |
| CIIU Rev. 4 A.C. (clasificación y correlativas) | Página de nomenclaturas del SEN en dane.gov.co, sin URL exacta confirmada. Las cámaras usan CIIU Rev.4 A.C. con dígitos extra (SI-indice, no oficial). | NO VERIFICADO |
| GEIH informalidad y PIB departamental (anexos) | Patrones `https://www.dane.gov.co/files/operaciones/...` sin confirmar | NO VERIFICADO |
| Sistema Estadístico Nacional (SEN) | `https://www.dane.gov.co/index.php/sistema-estadistico-nacional-sen` | NO VERIFICADO (WebFetch falló por DNS) |

---

## 5. Otras fuentes nacionales

| Fuente | Acceso | Detalle | Verif. |
|---|---|---|---|
| **RUES (Confecámaras), API interna** | REST JSON no oficial | `https://ruesapi.rues.org.co/WEB2/api/Expediente/DetalleRM/{id_rm}`, donde `id_rm = codigo_camara + "00" + matricula` (12 dígitos; ej. `210082976812`). Devuelve `registros[]` con `razon_social`, `cod_ciiu_act_econ_pri`, `ciiu4`, `fecha_matricula`, `fecha_renovacion`, `ultimo_ano_renovado`, `fecha_cancelacion`, `estado`, `organizacion_juridica`, `categoria_matricula`, `mun_comercial`, `dir_comercial`, `indicador_empresa_bic`, … La búsqueda avanzada pasó a `https://elasticprd.rues.org.co/api/ConsultasRUES/BusquedaAvanzadaRM`. **No está documentada, cambia a menudo y tiene datos de contacto personales: úsela solo para validar puntualmente.** | SI-fetch (gists `cdiaz` y `YoanSinH`) |
| **Supersociedades** | Informes y Power BI | "Las 10.000 empresas más grandes" 2026 (datos a 31-dic-2025), con herramienta Power BI. Reutilización libre citando la fuente (Ley 1712/2014). Datos tabulares en datos.gov.co: `6cat-2gcs` y NIIF. | SI-indice |
| **Colombia Compra Eficiente (SECOP II)** | SODA | `jbjy-vk9h`, `p6dx-8zbt`, `p8vk-huva`. Cliente Python `pysecop` 1.4.4 en PyPI. | SI-indice y SI-fetch |
| **Banco de la República - SUAMECA** | REST JSON **no oficial** (obtenido por ingeniería inversa) | Base `https://suameca.banrep.gov.co/estadisticas-economicas-back/rest/estadisticaEconomicaRestService`. Rutas: `consultaMenuXopcion?opcion=CATALOGO_DATOS`, `consultaMenuXId?idMenu={id}`, `consultaInformacionSerieXTipoDato?idSerie={ids}&tipoDato=0&cantDatos={n}`, `consultaSerieActiva?idSeries={id}`. Cabeceras `Accept: application/json`, `Origin` y `Referer` de suameca. Series: 1 = TRM, 59 = TPM, 15000 = IPC, 15271 = PIB trimestral, 15313 = desempleo. | SI-fetch (README de `MunirJalil/banrep-suameca`; repositorio con un solo commit) |
| TerriData (DNP) | Descarga XLSX y CSV y fichas municipales | `https://terridata.dnp.gov.co` tiene unos 1.750 indicadores en 24 dimensiones (dato de un README de GitHub). Endpoint de descarga sin confirmar. | NO VERIFICADO |
| MinCIT - perfiles económicos regionales | PDF y XLSX | `https://www.mincit.gov.co/estudios-economicos/perfiles-economicos-por-departamentos` | NO VERIFICADO |
| DIAN - estadísticas RUT y recaudo | XLSX | `https://www.dian.gov.co/dian/cifras/` | NO VERIFICADO |
| ICDE - catálogo nacional de datos geográficos | Catálogo | `https://www.icde.gov.co/datos-y-recursos/marco-geoestadistico-nacional-manzana-censal` | SI-indice |
| Esri Colombia - MGN 2021 municipio | ArcGIS REST | `https://ags.esri.co/arcgis/rest/services/MGN/MGN_2021_MUNICIPIO/MapServer` | SI-indice |
| Superservicios - DIVIPOLA | ArcGIS REST | `https://geoportal.superservicios.gov.co/server/rest/services/Divipola/Division_politico_administrativa/FeatureServer/layers` (0 = Municipios, campo `DPTO_CCDGO`; MaxRecordCount 2000) | SI-indice |

---

## 6. Portales territoriales (Bogotá, Medellín, Cali)

| Portal | Tipo | Endpoint | Verif. |
|---|---|---|---|
| Datos Abiertos Bogotá | CKAN | `https://datosabiertos.bogota.gov.co/api/3/action/package_search?q=...`, `package_show?id=...`, `datastore_search?resource_id=...&limit=..&offset=..`. **`datastore_search_sql` no está disponible.** Solo alrededor del 27 % de los recursos marcados con DataStore devuelve filas. | SI-fetch (código de `colombian-open-data-mcp/ckan.py`) |
| Datos Abiertos Cali | CKAN | `https://datos.cali.gov.co/api/3/action/...` | SI-fetch (mismo código) |
| Valle del Cauca | CKAN | `https://datosabiertos.valledelcauca.gov.co/api/3/action/...` | SI-fetch |
| Cartagena | CKAN | `https://datosabiertos.cartagena.gov.co/api/3/action/...` | SI-fetch |
| Catastro Bogotá (UAECD) | ArcGIS REST | Host `serviciosgis.catastrobogota.gov.co`; las capas se descubren desde el catálogo CKAN. Rutas exactas sin confirmar. | PARCIAL |
| Hábitat Bogotá | ArcGIS REST | Host `portalgis.habitatbogota.gov.co` | PARCIAL |
| IDECA / Mapas Bogotá | ArcGIS REST y descarga | `https://www.ideca.gov.co` | NO VERIFICADO |
| Jardín Botánico de Bogotá (ejemplo con `COD_DANE_A` por manzana) | ArcGIS REST | `https://geoportal.jbb.gov.co/agc/rest/services/SIGAU/ArboladoTerritorio/MapServer/2` | SI-indice |
| Medellín - servidor de mapas | ArcGIS REST | `https://www.medellin.gov.co/servidormapas/rest/services/ServiciosCatastro/HistoricoCatastral/MapServer/160?f=pjson` (Manzana_2024, campo `cobama`), `.../ServiciosCiudad/CartografiaBase/MapServer/20` | SI-indice |
| MEData (Medellín) | Portal de datos | `https://medata.gov.co` | NO VERIFICADO |

```python
import requests
r = requests.get("https://datosabiertos.bogota.gov.co/api/3/action/package_search",
                 params={"q": "establecimientos comercio", "rows": 50}, timeout=60)
for p in r.json()["result"]["results"]:
    print(p["name"], [(res["format"], res["url"]) for res in p["resources"]])
```

---

## 7. Fuentes no gubernamentales y de referencia

### 7.1 OpenStreetMap: Overpass API (POIs comerciales)

- Endpoint: `https://overpass-api.de/api/interpreter` (por POST o por GET con `data=`). SI-fetch: es el `default_url` de `overpy`. Licencia ODbL 1.0: hay que atribuir "© OpenStreetMap contributors" y, si se redistribuye una base derivada, compartirla igual.
- Uso en la datatón: sirve como contraste o "verdad de campo" de la densidad comercial frente al CENU, por ejemplo locales `shop=*` y `amenity=*` por sector urbano del MGN.

```bash
curl -s -X POST https://overpass-api.de/api/interpreter --data-urlencode 'data=
[out:json][timeout:180];
area["name"="Bogotá"]["boundary"="administrative"]["admin_level"="7"]->.a;
( nwr["shop"](area.a); nwr["amenity"~"restaurant|cafe|bar|fast_food|pharmacy|bank"](area.a); nwr["craft"](area.a); nwr["office"](area.a); );
out center tags;'
```

```python
import overpy   # overpy 0.7 en PyPI
api = overpy.Overpass()   # usa http://overpass-api.de/api/interpreter
res = api.query('[out:json][timeout:120];area["name"="Bogotá"]["admin_level"="7"]->.a;node["shop"](area.a);out;')
pois = [(n.id, float(n.lat), float(n.lon), n.tags.get("shop"), n.tags.get("name")) for n in res.nodes]
```

> El `admin_level` y el nombre del área de Bogotá en OSM son **NO VERIFICADOS**. Use `osmnx.features_from_place("Bogotá, Colombia", tags={"shop": True})` (osmnx 2.1.1 en PyPI) como alternativa robusta.

### 7.2 INEGI DENUE (México), como referencia de diseño de API

Directorio de establecimientos con API pública. Es un buen modelo para la propuesta de "API de unidades económicas del CENU". Base: `https://www.inegi.org.mx/app/api/denue/v1/consulta/`. Rutas (SI-fetch, código de INEGIpy `_denue.py`):

- `Buscar/{condiciones}/{lat},{lon}/{metros<=5000}/{token}`
- `Ficha/{clave}/{token}`
- `Nombre/{nombre}/{entidad}/{reg_ini}/{reg_fin}/{token}`
- `BuscarEntidad/{condiciones}/{entidad}/{reg_ini}/{reg_fin}/{token}`
- `BuscarAreaActEstr/...` y `Cuantificar/{actividad}/{area}/{estrato}/{token}`

Requiere un token gratuito: `https://www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify`. Documentación: `https://www.inegi.org.mx/servicios/api_denue.html`. Cliente Python: `inegipy` 2.0.0.

```bash
curl -s "https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/todos/19.4326,-99.1332/250/$INEGI_TOKEN"
```

---

## 8. Librerías Python (versiones confirmadas en PyPI, 21-oct-2026)

| Paquete | Versión | Para qué sirve | Nota |
|---|---|---|---|
| `sodapy` | 2.2.0 | Cliente SODA de datos.gov.co (`get`, `get_all`, `get_metadata`, `datasets`) | Mantenedor @afeld desde mar-2025 |
| `pysocrata` | 0.2.1 | Metadatos del catálogo Socrata | |
| `socrata-py` | 1.2.0 | SDK oficial para **publicar** en Socrata | No se necesita para leer |
| `pysecop` | 1.4.4 | Consultas SECOP I y II sobre datos.gov.co | De la comunidad |
| `pandas` | 3.0.6 | Tablas | Pandas 3 trae cambios de API (copy-on-write y dtype string por defecto) |
| `polars` | 2.0.0 | Tablas grandes (RUES de 9,4 millones de filas) | |
| `duckdb` | 2.0.0 | SQL local sobre CSV y Parquet; lee `https://...csv` con httpfs | |
| `pyarrow` | 26.0.0 | Parquet | |
| `geopandas` | 1.2.0 | MGN, manzanas y uniones espaciales | |
| `pyogrio` | 0.13.0 | Lectura rápida de SHP y GPKG | |
| `shapely` | 2.2.0 | Geometrías | |
| `esridump` | 1.13.0 | Descarga paginada de capas ArcGIS REST a GeoJSON | El nombre en PyPI es `esridump`, no `pyesridump` |
| `arcgis2geojson` | 3.1.3 | Convierte JSON de Esri a GeoJSON | |
| `arcgis` | 2.4.4 | ArcGIS API for Python (Hub y FeatureLayer) | Pesado |
| `pyreadstat` | 1.3.7 | Lee .sav, .dta y .sas7bdat de microdatos DANE con etiquetas | |
| `savReaderWriter` | 3.4.2 | SPSS (alternativa antigua) | |
| `openpyxl` | 3.1.5 | Anexos XLSX del DANE | |
| `requests` | 2.34.2 | HTTP | |
| `ckanapi` | 4.11 | CKAN de Bogotá, Cali, Valle y Cartagena | |
| `pynada` | 0.0.35 | Cliente de la API NADA (microdatos DANE) | Sin probar contra el DANE |
| `overpy` | 0.7 | Overpass | |
| `overpass` | 0.8.2 | Overpass (alternativa) | |
| `osmnx` | 2.1.1 | POIs y redes de OSM | |
| `inegipy` | 2.0.0 | DENUE e indicadores del INEGI (referencia) | |

**Paquetes específicos para Colombia o el DANE:** en PyPI **no existen** `pydane`, `danepy`, `divipola`, `colombia-data`, `datos-gov-co`, `banrep`, `pybanrep`, `geih`, `terridata` ni `microdatos`. Ojo: `dane` (0.4.3) es otro proyecto (CLARIAH) y `rues` (0.1.1.3) es de algoritmos genéticos. `econ-utils-co` dice estar en PyPI en su README, pero **la API JSON de PyPI no lo devuelve**. Hay repositorios útiles en GitHub (verificados por fetch): `alcastaro/colombian-open-data-mcp` (clientes Socrata, CKAN y Esri para Colombia), `MunirJalil/banrep-suameca`, `Macorreag/colombiaData`, `saulortega/divipola` (Go) y `aulageo/divipola` (GeoJSON).

---

## 9. Script de humo (correr con red abierta para pasar de SI-indice a SI-fetch)

> En este repositorio ya está implementado: `python scripts/descargar_fuentes.py smoke` (deja `reports/smoke_fuentes.csv`). El bloque siguiente es la versión independiente, sin dependencias del repo.

```python
# smoke_test_fuentes.py: corre en segundos y deja un CSV con el estado HTTP de cada fuente
import requests, csv, time
H = {"User-Agent": "dataton-cenu/0.1"}
URLS = {
 "soda_divipola": "https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=2",
 "soda_rues": "https://www.datos.gov.co/resource/c82u-588k.json?$limit=2",
 "soda_rues_meta": "https://www.datos.gov.co/api/views/c82u-588k.json",
 "soda_10k": "https://www.datos.gov.co/resource/6cat-2gcs.json?$limit=2",
 "soda_estructura": "https://www.datos.gov.co/resource/bzeh-ecuk.json?$limit=2",
 "soda_cp": "https://www.datos.gov.co/resource/xaxy-8nri.json?$limit=2",
 "socrata_catalog": "https://api.us.socrata.com/api/catalog/v1?domains=www.datos.gov.co&search_context=www.datos.gov.co&q=censo%20economico&limit=20",
 "nada_search": "https://microdatos.dane.gov.co/index.php/api/catalog/search?sk=micronegocios&format=json",
 "nada_emicron24": "https://microdatos.dane.gov.co/index.php/api/catalog/875?id_format=id",
 "arcgis_root": "https://geoportal.dane.gov.co/mparcgis/rest/services?f=pjson",
 "arcgis_cenu": "https://geoportal.dane.gov.co/mparcgis/rest/services/CENU?f=pjson",
 "arcgis_conteo": "https://geoportal.dane.gov.co/mparcgis/rest/services/CONTEO_UNIDADES_ECONOMICAS?f=pjson",
 "arcgis_mgn24_manzana": "https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2024/Serv_CapasMGN_2024/MapServer/215?f=pjson",
 "arcgis_divipola25": "https://portalgis.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2025/FeatureServer/layers?f=pjson",
 "ckan_bogota": "https://datosabiertos.bogota.gov.co/api/3/action/package_search?q=comercio&rows=5",
 "overpass_status": "https://overpass-api.de/api/status",
 "cenu_resultados": "https://censoeconomiconacionalurbano.dane.gov.co/resultados/",
}
with open("smoke_fuentes.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "url", "status", "bytes", "ms"])
    for k, u in URLS.items():
        t = time.time()
        try:
            r = requests.get(u, headers=H, timeout=60); s, b = r.status_code, len(r.content)
        except Exception as e:
            s, b = f"ERR {type(e).__name__}", 0
        w.writerow([k, u, s, b, int((time.time() - t) * 1000)]); print(k, s, b)
```

---

## 10. Recomendaciones para la datatón

1. **Columna vertebral territorial:** DIVIPOLA (`gdxc-w37w` y `xaxy-8nri`) más el MGN 2024 o 2025 (ArcGIS `Serv_CapasMGN_2024`, capas 246, 214 y 215, o el SHP del hub). Con eso se unen el CENU, el RUES, la EMICRON y OSM por `cod_mpio`, sector o sección urbana.
2. **Universo formal frente a censado:** RUES `c82u-588k`, agregado por cámara, municipio, CIIU y año de matrícula o renovación, frente a las unidades del CENU por municipio. La brecha entre ambos es un indicador de informalidad registral. Revise la fecha de actualización real del RUES.
3. **Profundidad económica:** EMICRON 2024 y 2025 (ANDA 875 y 914) para ventas, costos, formalización y TIC de micronegocios. Las grandes empresas salen de `6cat-2gcs` y de los NIIF de Supersociedades.
4. **Validación geográfica independiente:** POIs de OSM vía Overpass y el CNUE 2021 (`?cod=45` y los XLSX por municipio) para medir el cambio 2021 a 2024.
5. **Diseño de producto:** use la API DENUE del INEGI como referencia para proponer al DANE una API de unidades económicas (búsqueda por radio, por actividad y conteos agregados).
6. **Pendiente crítico:** abrir las carpetas ArcGIS `CENU` y `CONTEO_UNIDADES_ECONOMICAS`, y la sección de resultados o el visor del CENU, para ubicar los datos del CENU publicados por sector o sección.
