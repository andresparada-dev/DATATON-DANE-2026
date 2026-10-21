"""Toolkit para la Datatón CENU 2026 (Censo Económico Nacional Urbano - DANE).

Módulos:
    schema      Normaliza cualquier tabla de unidades económicas a un esquema estándar.
    ciiu        Clasificación CIIU Rev. 4 A.C. (secciones y mapeo división -> sección).
    indicators  Indicadores económicos (densidad, LQ, HHI, formalidad, brecha de género...).
    spatial     Análisis espacial sin dependencias pesadas (DBSCAN, grilla, Moran's I, Gi*).
    synthetic   Datos SINTÉTICOS para ensayar el flujo antes del evento.
    report      Reporte automático (gráficas + Markdown/HTML) a partir de un DataFrame.
    clients     Clientes para datos.gov.co (Socrata), microdatos DANE (NADA),
                servicios ArcGIS REST (geoportal) y OpenStreetMap (Overpass).
"""

__version__ = "0.1.0"
