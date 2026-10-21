# Datatón CENU 2026: Censo Económico Nacional Urbano (DANE)

Kit de preparación para la **Datatón del Censo Económico Nacional Urbano**, el sábado 24 de octubre de 2026 en la Universidad de La Salle (sede Chapinero, Auditorio Cincuentenario). El reto va de 7:50 a 9:50 y cada equipo tiene 5 minutos de pitch.

> **Dato clave:** el nombre oficial de la operación es **CENU 2024**. La recolección fue en 2024-2025 y los resultados se publican por entregas en 2025-2026. Contó **2.005.613 unidades económicas urbanas visibles** en 1.102 municipios, y es el primer censo económico desde 1990.

## Contenido

| Carpeta | Qué hay |
|---|---|
| [`docs/01_cenu_2024_contexto.md`](docs/01_cenu_2024_contexto.md) | Qué es el CENU: marco legal, presupuesto, cronograma, metodología, cuestionarios, resultados publicados (1.ª y 3.ª entrega), inconsistencias entre versiones y unos 40 enlaces oficiales |
| [`docs/02_historico_censos_y_operaciones.md`](docs/02_historico_censos_y_operaciones.md) | Censos de 1945, 1953/54, 1970/71, 1990, 2005, CNA 2014, CNPV 2018 y CENU 2024; EMICRON, GEIH, EAM/EAC/EAS, PIB departamental, RUES; comparativa con México (DENUE), Perú, Ecuador, Chile y Brasil |
| [`docs/03_fuentes_datos_apis.md`](docs/03_fuentes_datos_apis.md) | Catálogo técnico de 57 fuentes: SODA de datos.gov.co (IDs verificados), API NADA de microdatos DANE (IDs de catálogo), ArcGIS REST del Geoportal (MGN, CENU), CKAN de Bogotá, Overpass, DENUE y librerías Python |
| [`docs/04_analisis_profundo.md`](docs/04_analisis_profundo.md) | **Análisis con cifras oficiales:** 10 hallazgos, comparación 1990→2024, Conteo 2021 vs CENU, unidades vs PIB, CENU vs EMICRON, venta en calle, informalidad, plan de análisis y limitaciones |
| [`docs/05_ideas_negocio_y_estrategia.md`](docs/05_ideas_negocio_y_estrategia.md) | **18 ideas de negocio y política** con matriz de impacto y factibilidad, top 3, casos internacionales, fórmulas, cronograma minuto a minuto, roles, pitch y 14 preguntas del jurado con respuesta |
| [`docs/06_guia_dia_evento.md`](docs/06_guia_dia_evento.md) | Guía rápida del día: checklist, comandos, árbol de decisión de la idea y cifras clave |
| [`pitch/plantilla_pitch.md`](pitch/plantilla_pitch.md) | Plantilla de 7 diapositivas para 5 minutos |
| [`data/cifras_oficiales/`](data/cifras_oficiales) | Cifras publicadas (CENU, Conteo 2021, históricos, EMICRON, GEIH, PIB), **cada una con URL de fuente** |
| [`data/catalogo_fuentes.csv`](data/catalogo_fuentes.csv) | Catálogo de fuentes y APIs en formato tabular |
| `src/cenu/` | Toolkit de Python (abajo) |
| `scripts/` | Herramientas de línea de comandos (abajo) |
| [`notebooks/00_quickstart_cenu.ipynb`](notebooks/00_quickstart_cenu.ipynb) | Notebook de arranque, compatible con Google Colab |
| [`reports/ejemplo_sintetico/`](reports/ejemplo_sintetico) | Ejemplo del reporte automático, hecho con **datos sintéticos** |

## Uso rápido

```bash
pip install -r requirements.txt            # opcional: folium pyreadstat geopandas
python -m pytest -q                        # 15 pruebas

# 1) Análisis automático de cualquier archivo de unidades económicas (CSV/XLSX/Parquet/SAV/DTA)
python scripts/analisis_rapido.py --input data/raw/<archivo> --region municipio
python scripts/analisis_rapido.py --sintetico 20000          # ensayo con datos SINTÉTICOS

# 2) MVP "Donde Falta, Emprende": desiertos de servicios esenciales por celda
python scripts/donde_falta.py --input data/raw/<archivo> --municipio "Bogotá" --radio 500
python scripts/donde_falta.py --sintetico

# 3) Fuentes oficiales (requiere internet)
python scripts/descargar_fuentes.py smoke                     # estado HTTP de cada API
python scripts/descargar_fuentes.py divipola                  # DIVIPOLA municipios
python scripts/descargar_fuentes.py nada-buscar "censo economico"
python scripts/descargar_fuentes.py arcgis-listar             # servicios de la carpeta CENU del Geoportal
python scripts/descargar_fuentes.py socrata c82u-588k --limite 1000   # RUES

# 4) Regenerar las gráficas del análisis con cifras oficiales
python scripts/analisis_cifras_oficiales.py
```

En Colab: abrir `notebooks/00_quickstart_cenu.ipynb` y ejecutar todo. La primera celda clona el repositorio.

## Toolkit `src/cenu`

| Módulo | Funciones |
|---|---|
| `schema` | `normalizar()` reconoce columnas por alias (sin tildes ni mayúsculas, por palabra o subcadena) y las lleva a un esquema estándar: códigos DIVIPOLA con ceros, booleanos de Sí/No o 1/2, sexo, coordenadas. También `perfil_calidad()` |
| `ciiu` | Secciones CIIU Rev. 4 A.C. (A–U), mapeo de división a sección, gran sector, y detección de clases que perdieron el cero inicial |
| `indicators` | `resumen_kpis`, `conteo_por`, `densidad_empresarial`, `cociente_localizacion` (LQ), `hhi_diversificacion` (HHI y Shannon), `indice_formalidad`, `brecha_genero`, `distribucion_tamano`, `distribucion_antiguedad`, `brecha_oferta`. Todas aceptan `peso=` para factores de expansión o tablas agregadas |
| `spatial` | `grilla`, `clusters_dbscan`, `resumen_clusters`, `distancia_mas_cercana`, `morans_i`, `getis_ord_gi_star`. Solo usa numpy y scikit-learn, sin geopandas |
| `oportunidad` | Categorías esenciales por CIIU, `desiertos()` y `top_oportunidades()` |
| `report` | `generar_reporte()`: PNG, Markdown y HTML autocontenido, más los CSV de cada tabla |
| `clients` | `SocrataClient` (datos.gov.co), `NadaClient` (microdatos DANE), `ArcGISClient` (Geoportal y MGN), `pois_comercio` (OSM). Todos con reintentos exponenciales |
| `synthetic` | Datos **sintéticos** para ensayar. No son cifras oficiales |

## Advertencias

- Las cifras del CENU son **preliminares** y varias vienen de prensa que cita al DANE. Hay que verificarlas en el boletín oficial antes de publicarlas. Cada cifra tiene su URL en `data/cifras_oficiales/`.
- **Reserva estadística** (Ley 79/1993; art. 37 de la Ley 2335/2023): publicar solo agregados y nunca unidades identificables.
- La investigación se hizo el 21-oct-2026 desde un entorno sin acceso directo a dominios `.gov.co`. Los endpoints quedaron verificados por índice de búsqueda; antes de depender de ellos, confirmarlos con `scripts/descargar_fuentes.py smoke`.
- La organización no ha publicado las bases ni los datos de la datatón. Las ideas y el toolkit están pensados para adaptarse a microdatos o a tablas agregadas.
