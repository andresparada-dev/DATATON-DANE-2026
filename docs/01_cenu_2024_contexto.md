# 01 · Censo Económico Nacional Urbano (CENU 2024) y Datatón CENU 2026 — dossier de investigación

**Fecha de corte:** 21 de octubre de 2026
**Método:** solo funcionó WebSearch. WebFetch falló con error DNS (`getaddrinfo ENOTFOUND`) en **todos** los dominios probados: dane.gov.co, censoeconomiconacionalurbano.dane.gov.co, difusioncensoeconomiconacionalurbano.dane.gov.co, portafolio.co, larepublica.co, valoraanalitik.com y unstats.un.org. El proxy del contenedor también bloquea curl (403). Por eso **ningún PDF ni página oficial se leyó completo**. Las cifras vienen de fragmentos indexados por el buscador, de páginas del DANE o de prensa, y cada una lleva su URL de origen. Además se agotó el límite de búsquedas web de la sesión (200), así que algunos puntos quedaron sin verificar.

> **Aclaración de nombre.** El nombre oficial de la operación es **"Censo Económico Nacional Urbano (CENU) 2024"**. La recolección se hizo entre 2024 y comienzos de 2025, y la difusión de resultados ocurre en 2025-2026. No encontré ninguna fuente que lo llame "CENU 2026". Ese rótulo parece venir del año de la datatón y de la difusión.

Leyenda: **[OFICIAL]** = documento o página del DANE o del Estado (vista solo en fragmento del buscador). **[PRENSA]** = medio de comunicación. **NO CONFIRMADO** = no se pudo verificar.

---

## 1. Qué es el CENU

### 1.1 Definición y objetivo
- Es una operación estadística estratégica del DANE. Busca "consolidar un marco de información integral sobre las unidades económicas en las zonas urbanas de todos los municipios con cabecera urbana" [OFICIAL, Documento Metodológico DSO-CENU-MET-001 V2, nov-2025]: https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/documento-metodologico-cenu-20251110.pdf
- **Objetivo general** según la ficha metodológica: "obtener datos estadísticos actualizados sobre las principales variables económicas de las unidades ubicadas en cabeceras municipales y centros poblados del territorio nacional". La operación es de carácter **universal**, es decir, busca todas las unidades de observación [OFICIAL, Ficha Metodológica DSO-CENU-FME-001 v1, 21-ago-2024]: https://censoeconomiconacionalurbano.dane.gov.co/images/2024/agosto/Ficha-Metodologica_CENU_FME-001_v1_2024_08_21.pdf
- **Objetivo específico** citado: aportar insumos para actualizar los marcos estadísticos y los directorios empresariales del DANE (misma ficha).
- **Sectores cubiertos:** industria manufacturera, comercio, servicios, construcción, transporte y administración pública, entre otros (misma ficha). Ley 2294/2023, art. 95: "industria, comercio, servicios, construcción y transporte".
- **Cobertura solo urbana.** El DANE explica que la medición económica del sector rural ya la hacen otras operaciones estadísticas [OFICIAL, fragmento del documento metodológico]: https://www.dane.gov.co/files/operaciones/CENU/DSO-CENU-MET-001.pdf
- **Usos declarados:**
  - Actualizar el año base del PIB y rediseñar las encuestas económicas, según Piedad Urdinola, directora del DANE [PRENSA, El Tiempo]: https://www.eltiempo.com/amp/economia/sectores/los-ultimos-datos-del-censo-economico-urbano-del-dane-que-no-se-realizaba-hace-mas-de-34-anos-en-colombia-3570240
  - Ser insumo del Sistema de Información de la Economía Popular (SIEP), según el art. 90 de la Ley 2294/2023 [OFICIAL, proyecto de decreto CENU]: https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-MemoriaJustificativa-2024.pdf
- Es el **primer censo económico en 34 años**: el anterior fue el de 1990 [PRENSA, Semana]: https://www.semana.com/economia/capsulas/articulo/colombia-actualiza-su-mapa-economico-urbano-tras-34-anos-con-el-nuevo-censo-economico-del-dane/202538/

### 1.2 Marco legal
| Norma | Contenido | Fuente |
|---|---|---|
| **Ley 2294 de 2023** (PND 2022-2026 "Colombia Potencia Mundial de la Vida"), **art. 95, "Censo Económico Nacional"** | Ordena al DANE caracterizar y actualizar la información de las unidades económicas de industria, comercio, servicios, construcción y transporte ubicadas en el territorio nacional en **2024**, incluida la Economía Popular. Prevé un **conteo intercensal 5 años después** y el uso de registros administrativos | https://leyonline.co/laws/ley-2294-de-2023/articulo-95-censo-economico-nacional ; https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=209510 |
| Ley 2294 de 2023, **art. 90** | Crea el SIEP, que usa como insumo, entre otros, el Censo Económico | https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-MemoriaJustificativa-2024.pdf |
| **Ley 2335 de 2023** (Ley del Sistema Estadístico Nacional) | El art. 27 asigna al DANE los censos económicos, según estudios previos de contratación. El art. 37 cubre la confidencialidad. Según el "Marco Normativo" del CENU, prevé **censos económicos cada 10 años y conteos intercensales cada 5 años**. **Número exacto del artículo de periodicidad: NO CONFIRMADO** | https://censoeconomiconacionalurbano.dane.gov.co/images/Autodiligenciamiento-web/Marco-Normativo_Censo-Economico-nacional-Urbano_2024.pdf ; columna de Urdinola en La República: https://www.larepublica.co/analisis/piedad-urdinola-3874408/un-mejor-espejo-de-colombia-4437808 |
| **CONPES 3956** (Política de formalización empresarial) | El DANE enmarca el CENU en este documento, que busca fomentar la formalidad empresarial mejorando la información disponible para políticas públicas. **Asignación presupuestal específica dentro del CONPES: NO CONFIRMADO** | Marco Normativo CENU (URL de arriba) |
| **Proyecto de Decreto CENU 2024** y su Memoria Justificativa | Proyecto normativo del DANE con base en los arts. 90 y 95. En una búsqueda aparece como resolución de **gobernanza** del CENU. **Número del decreto o resolución finalmente expedido: NO CONFIRMADO** | https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-2024.pdf ; https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-MemoriaJustificativa-2024.pdf |
| Ley 1955 de 2019 (PND 2018-2022) | **NO CONFIRMADO** que tenga un artículo sobre el censo económico | — |

### 1.3 Presupuesto
- **$335.000 millones** (Piedad Urdinola, oct-2025, en un foro) [PRENSA, La República]: https://www.larepublica.co/economia/el-nuevo-censo-economico-del-dane-se-conocera-el-proximo-11-de-noviembre-4259631
- **$336.328 millones** (El Tiempo, entrevista de julio de 2026): https://www.eltiempo.com/economia/sectores/luego-de-34-anos-colombia-vuelve-a-conocer-su-economia-urbana-piedad-urdinola-directora-del-dane-3570729
- **Antecedente presupuestal:** en la planeación anterior, cuando el censo se proyectaba para 2020-2021, se anunciaron **$293.800 millones**: $10.000 M para 2020, $272.000 M para 2021 y $11.550 M para 2022 [PRENSA, Valora Analitik]: https://www.valoraanalitik.com/colombia-tendra-nuevo-censo-economico-se-invertiran-293-mil-millones/

### 1.4 Cronograma
| Hito | Fecha | Fuente |
|---|---|---|
| Comunicado de anuncio del CENU | Dic-2023 (anunciaba inicio en junio de 2024) | https://www.dane.gov.co/files/investigaciones/censo-economico/cp-CENU.pdf |
| **Fase 1: autodiligenciamiento web.** Correos masivos a cerca de 50.000 empresas, empezando por transporte. Plazo para medianas y grandes: 30-sep-2024 | **4-jun-2024** | El Tiempo: https://www.eltiempo.com/economia/sectores/tres-decadas-despues-el-dane-comenzara-el-martes-4-de-junio-el-censo-economico-nacional-3348691 ; https://www.eltiempo.com/economia/sectores/el-censo-economico-empezara-con-el-envio-masivo-de-correos-electronicos-a-alrededor-de-50-000-empresas-3349299 ; El Colombiano: https://www.elcolombiano.com/negocios/censo-economico-nacional-urbano-2024-colombia-conocer-economia-a-fondo-BI24684621 |
| **Fase 2: recuento.** Unos 388 recuentistas y 99 supervisores con dispositivos móviles; arrancó en Bogotá y 10 municipios de Cundinamarca y se extendió a 133 centros operativos | Jul-2024 | Presidencia: https://www.presidencia.gov.co/prensa/Paginas/DANE-comenzo-segunda-fase-del-Censo-Economico-Nacional-desde-pequenos-nego-240702.aspx ; DANE: https://www.dane.gov.co/index.php/actualidad-dane/5786-con-el-recuento-empieza-la-segunda-fase-del-censo-economico-nacional-urbano |
| **Fase 3: barrido** (censistas casa a casa y en calle) | Prevista para el 4-ago-2024. Arranque formal reportado el **11-sep-2024 en Cartagena** (mercado de Bazurto). La diferencia de fechas no está resuelta | El Universal: https://www.eluniversal.com.co/economica/2024/09/11/en-un-negocio-de-bazurto-en-cartagena-empezo-la-fase-de-barrido-del-censo-economico/ ; Portafolio: https://www.portafolio.co/economia/censo-economico-arranco-la-implementacion-de-su-primera-etapa-605869 |
| Denuncias de retrasos y fallas logísticas | Jun-2024 (Cambio) y 2025 (Portafolio) | https://cambiocolombia.com/pais/articulo/2024/6/el-dane-le-lleva-la-contraria-petro-el-despelote-en-el-censo-economico-que-revela-aparentes ; https://www.portafolio.co/economia/gobierno/el-censo-economico-nacional-urbano-avanza-con-demoras-en-su-ejecucion-625116 |
| "Fase final" de recolección: más de 2,3 millones de unidades registradas a finales de enero de 2025 | Feb-2025 | https://censoeconomiconacionalurbano.dane.gov.co/images/2025/comunicadosDePrensa/com-Censo-Fase-Final-feb2025.pdf |
| **Resultados preliminares (1.ª entrega)** | **11-nov-2025** | https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano ; boletín: https://stg.censoeconomiconacionalurbano.dane.gov.co/images/2025/comunicadosDePrensa/20251111_Boletin-de-Prensa_Resultados-Censo-Economico.pdf |
| 2.ª entrega | **NO CONFIRMADO** (fecha y contenido) | — |
| **3.ª entrega** (formalización: RUT y registro mercantil; datos sociodemográficos de propietarios) | El DANE anunció su inicio el **4-may-2026**. Comunicado del **25-may-2026** | https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf ; listado DANE: https://www.dane.gov.co/index.php/sala-de-prensa/caja-de-herramientas/comunicados-de-prensa-y-presentaciones |
| Foro EL TIEMPO-DANE "Datos para decidir: los nuevos hallazgos del CENU" | **9-jul-2026**. Algunas notas fechan la presentación sobre mujeres propietarias el 14-jul-2026 | https://www.eltiempo.com/mas-contenido/los-nuevos-hallazgos-del-censo-economico-en-el-centro-del-proximo-foro-de-el-tiempo-y-el-dane-3569455 ; https://www.portafolio.co/economia/regiones/datos-para-decidir-los-nuevos-hallazgos-del-censo-economico-nacional-urbano-497856 |
| **Microdatos anonimizados** | Fechas en conflicto: "may-jun 2026" según una página del sitio de difusión; "finales de julio o comienzos de agosto" según Portafolio; "antes de la llegada del próximo gobierno" (7-ago-2026) según Urdinola. **Publicación efectiva en ANDA (microdatos.dane.gov.co): NO CONFIRMADO** a oct-2026 | https://www.portafolio.co/economia/regiones/en-colombia-hay-mas-de-dos-millones-de-unidades-economicas-segun-el-nuevo-censo-economico-nacional-urbano-del-dane-497881 ; https://www.eltiempo.com/economia/sectores/luego-de-34-anos-colombia-vuelve-a-conocer-su-economia-urbana-piedad-urdinola-directora-del-dane-3570729 |
| Difusión progresiva (análisis temáticos, sectoriales y regionales) | Durante todo 2026 | Comunicado DANE 5878 (URL de arriba) |

### 1.5 Cobertura geográfica
- **Cabeceras municipales y centros poblados** de los **1.102 municipios**, más **San Andrés y Providencia** y **18 áreas no municipalizadas** [OFICIAL, comunicado 5878; Ficha FME-001].
- Recorrido de **más de 500.000 manzanas**, con **más de 8.000 censistas** y una cobertura promedio **mayor al 98,2 %** [OFICIAL, comunicado 5878; PRENSA, Semana].

### 1.6 Unidad de observación y tipología
- **Unidad económica visible** en zona urbana.
- **Tipo de emplazamiento:** establecimiento **fijo**, **semifijo**, **vivienda con actividad económica visible** y **puesto móvil** [OFICIAL, Ficha FME-001 v2; resumen CENU de Cámara Directa]: https://www.camaradirecta.com/imagenes/vdo_conexion/cone_beba87be34b7796e18c5667fd5e8aebc4a61ed84.pdf
- **Tipo de unidad:** empresa, micronegocio, unidad institucional o vendedor de calle (resumen CENU, misma URL).
- **Definición de semifijo:** "Unidad Económica que cuenta con instalaciones delimitadas por construcciones simples adheridas al piso" [OFICIAL, Manual CNT-CENU-MDI-007]: https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/empresa/20240913_Manual-Diligenciamiento_PMG.pdf
- **Vendedor de calle:** persona que "se dedica voluntariamente al comercio de bienes o servicios en el espacio público, como medio básico de subsistencia" (fragmento de un documento del DANE).
- Glosario oficial: https://censoeconomiconacionalurbano.dane.gov.co/tienes-preguntas/conceptos-y-definiciones

### 1.7 Metodología
- **Censo "híbrido"**, el primero del país de este tipo. Combina trabajo de campo (recuento y barrido con dispositivos móviles), **registros administrativos** y **formularios web** que diligencian las propias empresas. También admite **cargue masivo de archivos .xlsx** [OFICIAL, ficha técnica 2025]: https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf ; [PRENSA, El Tiempo 3570729].
- **Georreferenciación** de unidades al interior de las manzanas. Ya se aplicó en el conteo de 2021, cuyo objetivo era "enumerar y georreferenciar" establecimientos, puestos móviles y viviendas con actividad económica: https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/FASE-III-documento-metodologico-preliminar-censo-economico-2021.pdf
- **DMC (Dispositivo Móvil de Captura):** la prensa reporta el uso de dispositivos móviles en el recuento (Presidencia). El término exacto "DMC" para el CENU: **NO CONFIRMADO** en fuente leída.
- **Enfoque étnico-racial:** El Tiempo afirma que fue "el segundo [censo económico] en el mundo con este enfoque": https://www.eltiempo.com/mas-contenido/luego-de-34-anos-el-pais-volvio-a-tener-un-censo-economico-de-su-economia-urbana-3511490
- Un fragmento de la ficha metodológica menciona un umbral de marco censal ("establecimientos con 5 o más personas ocupadas o valor de producción superior a un umbral"). **Contexto exacto: NO CONFIRMADO.**

### 1.8 Cuestionarios y variables
**Seis cuestionarios** [OFICIAL, manual PMG]: (1) Básico a establecimientos; (2) Vendedores de calle; (3) Pequeña, mediana y gran empresa (PMG, autodiligenciado vía web); (4) Especializado de construcción; (5) Especializado de transporte; (6) No confirmado. Posiblemente es el cuestionario web de Servicios de Administración Pública (SAF/SAFP).

- **Cuestionario PMG:** 6 módulos. Los módulos 1 a 4 son a nivel empresa, el 5 a nivel establecimiento y el 6 recoge los datos del informante. Según un fragmento de prensa, la versión de servicios tiene 208 preguntas y la de transporte 298 [OFICIAL manual / PRENSA El Colombiano].
  - Manual PMG (13-sep-2024): https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/empresa/20240913_Manual-Diligenciamiento_PMG.pdf
  - Manual PMG-Empresa final (22-oct-2024): https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/empresa/20241022_Manual-diligenciamiento_PMG-Empresa_final.pdf
- **Cuestionario básico a establecimientos (2024):** https://censoeconomiconacionalurbano.dane.gov.co/images/visitas-negocios/20240917_Cuestionario_Basico-establecimientos.pdf
  - Variables confirmadas en fragmentos: número de personas que trabajan (personal ocupado); registro en cámara de comercio (registro mercantil); RUT; entidades ante las que se registró la unidad; ingresos y costos (pagos, licencias, certificados); fuente principal de ingresos; actividad económica (clasificación).
  - Variables reportadas en resultados: **sexo, edad y nivel educativo del propietario**, **medios de pago**, **ingresos 2023** y **puestos de trabajo**.
  - **"Tiempo de funcionamiento"** y **"lleva contabilidad"** dentro del cuestionario básico: **NO CONFIRMADO**. La fecha de inicio de operaciones y los meses operados aparecen en el cuestionario web de administración pública.
- **Cuestionario vendedores de calle:** se reportan 88 preguntas (nota de prensa de 2024; **NO CONFIRMADO** en documento oficial). Lo diligencia el censista.
- **Cuestionario web Servicios de Administración Pública:** https://www.dane.gov.co/files/operaciones/CENU/CUESTIONARIOSAFPVERSINFINAL3.pdf y https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/safp/CE_Cuestionarioweb_8_SAF.pdf
- **Clasificaciones:** **CIIU Rev. 4 A.C.**; su principal ventaja es la comparabilidad internacional [OFICIAL, documento metodológico]. Por el carácter territorial del censo se presume el uso de **DIVIPOLA** y del marco geoestadístico, pero **NO CONFIRMADO** textualmente.
- **Confidencialidad:** art. 37 de la Ley 2335 de 2023 (reserva estadística).

---

## 2. Antecedentes inmediatos

### 2.1 Censo Económico de 1990
- Planeación hasta julio de 1989, preempadronamiento hasta enero de 1990, empadronamiento entre febrero y junio de 1990 y cierre en diciembre de 1990: https://biblioteca.dane.gov.co/media/libros/LD_10328_1990_EJ_5.PDF
- Resultados: alrededor de **1 millón de unidades económicas** y **3,9 millones de empleos**, con el comercio en el **56,2 %** [PRENSA citando al DANE]: https://www.eltiempo.com/economia/sectores/dane-lanza-el-censo-economico-nacional-urbano-de-colombia-834683

### 2.2 Conteo de Unidades Económicas 2021 (precenso)
- Se hizo en el **primer semestre de 2021** en los **1.102 municipios** [CEPAL, presentación del DANE]: https://cepal.org/sites/default/files/presentations/dane-censos-economicos-experiencia-colombia.pdf
- **Total: 2.548.896 unidades económicas** [OFICIAL, Nota estadística feb-2022]: https://www.dane.gov.co/files/investigaciones/notas-estadisticas/feb-2022-censo-economico.pdf
  - Bogotá: 451.093 (17,7 %). Antioquia: 296.942 (11,6 %). Valle del Cauca: 253.601 (9,9 %). Santander: 148.009 (5,8 %). Cundinamarca: 135.583 (5,3 %).
  - Por condición: fijas 83,1 %, viviendas con actividad económica 9,4 % (240.186 unidades), puestos móviles 4,1 % y semifijas 3,4 % [PRENSA, El Colombiano]: https://www.elcolombiano.com/negocios/empresas/cuantas-unidades-economicas-hay-en-colombia-OA15733904
  - Una cifra preliminar anterior de 2,58 millones superaba en 37,11 % las 1,88 millones esperadas [PRENSA, El Tiempo]: https://www.eltiempo.com/economia/sectores/dane-censo-economico-en-colombia-2021-598985
- **Geovisor oficial del conteo:** https://geoportal.dane.gov.co/geovisores/economia/resultados-conteo/
- Otros documentos de diseño: marco censal (ene-2021): https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/censo-economico-marco-censal.pdf ; documento metodológico preliminar Fase III: https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/FASE-III-documento-metodologico-preliminar-censo-economico-2021.pdf
- **Comparación metodológica:** el conteo de 2021 (2,55 M) y el CENU (2,0 M) **no son directamente comparables**. El CENU cuenta "unidades económicas visibles" con criterios de campo distintos. Esta es una interpretación propia; la conciliación oficial está **NO CONFIRMADA**.

### 2.3 Censo Económico Experimental (pilotos)
- **Funza, Ricaurte y Nariño** (Cundinamarca), durante **2021 y 2022**. Sirvió para pilotear metodologías de campo e instrumentos de recolección [OFICIAL, Ficha FME-001].
- En sept-2021 el entonces director del DANE anunció: "Nos vamos a concentrar en tres municipios, Ricaurte, Nariño y Funza…" [PRENSA, Infobae]: https://www.infobae.com/america/colombia/2021/09/22/dane-revelo-que-en-el-pais-hay-254-millones-de-negocios-formales-e-informales/
- Según la CEPAL, hubo pruebas de campo (ago-sep), un censo experimental (oct-dic) y pilotos temáticos como transporte.
- Cuestionarios del "Censo Experimental de Colombia 2020":
  - Básico: https://www.dane.gov.co/files/investigaciones/censo-economico/info-metodologica/CE-cuestionario-basico-establecimientos.pdf
  - Puestos móviles: https://www.dane.gov.co/files/investigaciones/censo-economico/info-metodologica/CE-cuestionario-puestos-moviles.pdf
  - Básico preliminar: https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/CuestionarioBasicoPreliminarEstablecimientos_CE.pdf
- **Resultados publicados de los pilotos: NO CONFIRMADO.** No se encontró un informe público con cifras de los tres municipios.
- Página histórica: https://www.dane.gov.co/index.php/categoria-economicas/5691-censo-economico-de-colombia-historico

---

## 3. Resultados publicados a octubre de 2026 (todos preliminares)

### 3.1 Primera entrega (11-nov-2025)
Fuente principal: comunicado DANE 5878 y boletín 20251111 (URLs en §1.4).
- **2.005.613 unidades económicas visibles** en zonas urbanas.
- **Por sector:**

  | Sector | Participación | Unidades |
  |---|---|---|
  | Comercio | 53,1 % | 1.066.668 según Valora. Otras cifras citadas: 1.064.505 y 1.062.288 (Portafolio, versión de julio de 2026) |
  | Servicios | 32,3 % | — |
  | Industria | 5,2 % | — |

  Fuente: https://www.valoraanalitik.com/censo-economico-del-dane-identifico-mas-de-dos-millones-de-empresas-y-negocios-en-colombia/
- **Por departamento:** Bogotá 360.565 (18 %), Antioquia 250.574 (12,5 %) y Valle 193.974 (9,7 %) [Valora/Yahoo]. En la versión de julio de 2026: Bogotá 359.990, Antioquia 250.406 y Valle 194.034 [PRENSA].
- **Por ciudad:** Bogotá 360.568, Medellín 118.679 (Valora: 118.678), Cali 99.208 y Bucaramanga 52.065. Barranquilla figura en el top 5 sin cifra confirmada [PRENSA, Semana / La República]: https://www.semana.com/economia/macroeconomia/articulo/primeros-resultados-del-censo-economico-urbano-del-dane-ranking-de-ciudades-con-mas-negocios-en-colombia/202550/
- Los 30 municipios con más unidades concentran el **57,2 %** del total.
- **Vendedores de calle: 219.042 unidades**, cerca de 1 de cada 10 y presentes en unos 990 municipios. Bogotá tiene 42.097, Antioquia 21.617, Valle 19.326, Medellín 13.692 y Cali 12.213. La mayoría son estacionarios, no ambulantes [PRENSA]: https://www.larepublica.co/economia/hay-mas-de-219-000-colombianos-que-tienen-unidades-productivas-de-venta-de-calle-4346821 ; https://www.portafolio.co/economia/crecimiento/uno-de-cada-10-negocios-en-colombia-hace-parte-de-las-ventas-ambulantes-482970
- **Ingresos 2023:** alrededor de **$2.421 billones** (redondeado a $2.400 billones) [PRENSA, Valora / Portafolio].

### 3.2 Tercera entrega (mayo de 2026): formalización y propietarios
- **RUT:** de **1.547.275** unidades (subconjunto con información, distinto del total de 2,0 M), el **49,16 %** tiene RUT (760.680), el **37,32 %** no lo tiene (577.485) y el **13,51 %** no dio información válida [PRENSA, El Heraldo, 26-may-2026]: https://www.elheraldo.co/economia/2026/05/26/solo-la-mitad-de-los-negocios-en-colombia-cuenta-con-rut-segun-el-dane/ . El Tiempo reporta 760.327 unidades (49,2 %).
- **Registro mercantil:** promedio nacional **47,5 %**, según una fuente local de Ibagué (**NO CONFIRMADO** en fuente oficial). San Andrés lidera con 70,28 % de RUT y 74,82 % de registro mercantil. Bogotá tiene 158.647 unidades con registro mercantil. Sobre Bolívar: https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/
- **Propietarios:** el **59,4 %** de las unidades tiene información sociodemográfica (sexo, edad, educación). **Mujeres: 613.953; hombres: 576.983**, una diferencia de 36.970. Las mujeres representan alrededor del 51,5 % de las unidades con dato. En Bogotá hay 90.628 unidades con propietaria mujer [PRENSA, La República]: https://www.larepublica.co/economia/dane-reporto-mas-de-1-1-millones-de-unidades-economicas-con-datos-sociodemograficos-4384649 ; El Tiempo: https://www.eltiempo.com/amp/economia/sectores/en-colombia-hay-mas-mujeres-propietarias-de-negocios-urbanos-que-hombres-3553039

### 3.3 Foro de julio de 2026 (El Tiempo-DANE)
- Totales revisados: **2.005.622** (El Tiempo) y **2.005.248** (entrevista a Urdinola). Hay pequeñas revisiones entre versiones.
- **Puestos de trabajo: más de 9,5 millones** [El Tiempo 3570240]. Otra fuente menciona "6,1 millones de personas ocupadas" (**NO CONFIRMADO**; posible diferencia entre puestos de trabajo y personas ocupadas, o entre subconjuntos).
- Se reportan nuevos temas: **medios de pago**, informalidad medida "por primera vez" y características de los propietarios. **Cifras de medios de pago: NO CONFIRMADO.**

### 3.4 Visores y tableros
- **Sitio de difusión:** https://difusioncensoeconomiconacionalurbano.dane.gov.co/
- **Resultados preliminares:** https://censoeconomiconacionalurbano.dane.gov.co/resultados/
- La prensa (Portafolio, BusinessCol, La FM) menciona un **visor interactivo** con el total nacional y más de 1.100 municipios. **URL exacta del visor: NO CONFIRMADO.** Probablemente está dentro del sitio de difusión.
- Tablero de terceros (Observatorio Fiscal de Armenia): https://observatorioarmenia.org/site/observatorio-fiscal-radiografia-de-la-economia-urbana-colombiana/

### 3.5 Inconsistencias que conviene conocer en la Datatón
1. El total varía entre 2.005.248, 2.005.613 y 2.005.622 según la versión. Una página del sitio de difusión mostraría "1.230 M" (**NO CONFIRMADO**; posiblemente un subconjunto).
2. Las tasas de RUT y registro mercantil se calculan sobre unos **1,55 M** de unidades con información, no sobre los 2,0 M.
3. Los datos sociodemográficos cubren el **59,4 %** de las unidades.
4. El comercio aparece como 1.062.288, 1.064.505 o 1.066.668 según la fuente.

---

## 4. Datatón CENU 2026 (sábado 24 de octubre de 2026, Universidad de La Salle, Bogotá)

**Resultado de la investigación: NO CONFIRMADO en fuentes públicas indexadas.**
- Hice más de 10 búsquedas específicas: "Datatón CENU", "datatón DANE 2026", "Universidad de La Salle datatón 2026", "lasalle.edu.co datatón DANE", "datathon DANE universidades microdatos censo económico" y variantes con hackatón y maratón de datos. Ninguna devolvió la convocatoria, las bases, los retos, los premios, el jurado ni los criterios de evaluación.
- Por lo tanto **convocatoria, bases, requisitos, retos, categorías, criterios del jurado, premios y datos entregados quedan todos como NO CONFIRMADO**. Hay que obtenerlos directamente de los organizadores o de los canales de inscripción.
- Contexto verificable sobre La Salle: la universidad lanzó un **pregrado virtual en Ciencia de Datos** (2024): https://lasalle.edu.co/es/noticias/la-universidad-de-la-salle-presenta-su-nuevo-programa-de-ciencia-de-datos . También ofrece una Especialización en Análisis Estadístico para Ciencia de Datos: https://lasalle.edu.co/es/especializacion/especializacion-en-analisis-estadistico-para-ciencia-de-datos . Un profesor del programa trabajó en proyectos de datos ligados a las encuestas de industria, comercio y servicios del DANE: https://lasalle.edu.co/es/noticias/lanzamiento-del-programa-de-ciencia-de-datos
- **Hipótesis razonable (no verificada):** como los microdatos anonimizados del CENU estaban previstos para mediados de 2026, la datatón probablemente use microdatos anonimizados o agregados municipales y sectoriales del CENU, además de capas geográficas del DANE. **NO CONFIRMADO.**

### 4.1 Antecedentes de datatones y concursos relacionados con el DANE

| Evento | Detalle | Fuente |
|---|---|---|
| **UN Datathon 2024** (Medellín, 8-11 nov-2024, durante el Foro Mundial de Datos de la ONU) | Coorganizado por la ONU (UN-CEBD/UNSD), el **DANE**, Ruta N y la Alcaldía de Medellín. Tema: **"Soluciones para el turismo sostenible en áreas urbanas a partir de los datos"**. Más de 100 equipos inscritos. Premios: ganador general, mejor equipo joven (menores de 32 años) y mejor equipo estudiantil. **1.º: INEGI-LCiD México. Mejor equipo estudiantil y mejor joven: TuringBox (Universidad Nacional de Colombia).** El equipo **DANE Geoinformación** aparece en el podio; el puesto exacto (2.º o 3.º) está **NO CONFIRMADO**. También figuran Sisifos (U. de Antioquia) y Datavengers (U. Cooperativa) entre los equipos jóvenes | https://unstats.un.org/bigdata/events/2024/un-datathon ; https://unstats.un.org/bigdata/events/2024/un-datathon/winners.cshtml ; https://foromundialdedatos.dane.gov.co/es/ultimas-noticias/ya-llega-la-un-datathon-2024 ; comunicado: https://unstats.un.org/bigdata/events/2024/un-datathon/files/Comunicado%20UN%20Datathon%20WDF_final.pdf ; CEPAL: https://www.cepal.org/en/notes/un-datathon-2024-solutions-sustainable-tourism-urban-areas-based-data |
| **Datos a la U 2024** (MinTIC, datos.gov.co) | 16 equipos finalistas y 50 estudiantes en la premiación (283 equipos inscritos según datos.gov.co). **Ganador: U. Tecnológica de Pereira**, con la "Herramienta colaborativa de IA para la reforma agraria basada en datos". El premio fue un viaje a ConDatos (Brasil); el 2.º y 3.º lugar recibieron herramientas tecnológicas | https://mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/398866:Con-exito-cerro-el-concurso-Datos-a-la-U-Conoce-a-los-ganadores ; https://herramientas.datos.gov.co/noticias/datos-la-u-edicion-2024-una-historia-para-contar |
| Data Challenge 2024 Uninorte (dengue) | No es del DANE | https://www.uninorte.edu.co/en/web/grupo-prensa/w/estos-son-los-ganadores-del-data-challenge-2024 |
| "Datatón DANE" propia o "Datajam" del DANE | **NO CONFIRMADO.** No se encontraron ediciones previas organizadas solo por el DANE | — |

**Patrón de propuestas ganadoras (inferido de los casos verificados):**
- Usan datos oficiales georreferenciados en soluciones aplicadas a una política pública concreta (turismo urbano sostenible, reforma agraria).
- Incluyen un componente de IA o herramientas colaborativas.
- Llevan la solución a un prototipo usable (tablero o herramienta).

### 4.2 Recursos de datos del DANE posiblemente útiles
- **ANDA (microdatos):** https://microdatos.dane.gov.co/ . Hay que verificar si ya existe el catálogo del CENU 2024 (**NO CONFIRMADO**).
- Centro de Datos Geoestadísticos (CDGE): https://cdge.dane.gov.co/
- Geovisor del conteo 2021: https://geoportal.dane.gov.co/geovisores/economia/resultados-conteo/
- El DANE publicó para comentarios un proyecto de resolución sobre acceso a microdatos no públicos con fines de investigación. Propone renombrar la sala de procesamiento especializado (SPEE) como "Centro de Datos Estadístico" [PRENSA, Semana 2026]: https://www.semana.com/economia/macroeconomia/articulo/dane-propone-nuevas-reglas-para-el-acceso-a-microdatos-estadisticos-con-fines-de-investigacion/202620/

---

## 5. Enlaces oficiales del DANE (URLs exactas vistas en el buscador; no se abrieron por el bloqueo de red)

**Portales y páginas**
- Página temática del CENU: https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/censo-economico-de-colombia/censo-economico-nacional-urbano
- Categoría del CENU: https://www.dane.gov.co/index.php/categoria-economicas/5399-censo-economico-nacional-urbano
- Censo Económico de Colombia: https://www.dane.gov.co/index.php/categoria-economicas/5397-censo-economico-de-colombia
- Histórico: https://www.dane.gov.co/index.php/categoria-economicas/5691-censo-economico-de-colombia-historico
- Micrositio operativo: https://censoeconomiconacionalurbano.dane.gov.co/
- Resultados preliminares: https://censoeconomiconacionalurbano.dane.gov.co/resultados/
- Micrositio de difusión: https://difusioncensoeconomiconacionalurbano.dane.gov.co/
- Conceptos y definiciones: https://censoeconomiconacionalurbano.dane.gov.co/tienes-preguntas/conceptos-y-definiciones
- CENU en los medios: https://censoeconomiconacionalurbano.dane.gov.co/contamos-con-su-voz/cenu-en-los-medios

**Noticias y comunicados**
- Lanzamiento del CENU 2024: https://www.dane.gov.co/index.php/el-dane-le-presento-al-pais-el-censo-economico-nacional-urbano-2024
- Inicio del recuento (fase 2): https://www.dane.gov.co/index.php/actualidad-dane/5786-con-el-recuento-empieza-la-segunda-fase-del-censo-economico-nacional-urbano
- Resultados preliminares: https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano
- Comunicado de anuncio (2023): https://www.dane.gov.co/files/investigaciones/censo-economico/cp-CENU.pdf
- Comunicado de fase final (feb-2025): https://censoeconomiconacionalurbano.dane.gov.co/images/2025/comunicadosDePrensa/com-Censo-Fase-Final-feb2025.pdf
- Boletín de resultados (11-nov-2025): https://stg.censoeconomiconacionalurbano.dane.gov.co/images/2025/comunicadosDePrensa/20251111_Boletin-de-Prensa_Resultados-Censo-Economico.pdf (dominio `stg.`; la ruta equivalente en producción está **NO CONFIRMADA**)
- Comunicado de la tercera entrega (25-may-2026): https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf

**Metodología**
- Documento metodológico V1: https://www.dane.gov.co/files/operaciones/CENU/DSO-CENU-MET-001.pdf
- Documento metodológico (nov-2025): https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/documento-metodologico-cenu-20251110.pdf
- Ficha metodológica v1 (ago-2024): https://censoeconomiconacionalurbano.dane.gov.co/images/2024/agosto/Ficha-Metodologica_CENU_FME-001_v1_2024_08_21.pdf
- Ficha técnica (versión clásica, 2025): https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf (también en https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf)
- Marco normativo: https://censoeconomiconacionalurbano.dane.gov.co/images/Autodiligenciamiento-web/Marco-Normativo_Censo-Economico-nacional-Urbano_2024.pdf
- Kit de comunicación: https://censoeconomiconacionalurbano.dane.gov.co/images/contamos-con-su-voz/Kit-Comunicacion_CENU-2024.pdf

**Cuestionarios y manuales**
- Cuestionario básico a establecimientos (2024): https://censoeconomiconacionalurbano.dane.gov.co/images/visitas-negocios/20240917_Cuestionario_Basico-establecimientos.pdf
- Manual PMG: https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/empresa/20240913_Manual-Diligenciamiento_PMG.pdf
- Manual PMG-Empresa final: https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/empresa/20241022_Manual-diligenciamiento_PMG-Empresa_final.pdf
- Cuestionario web SAF: https://censoeconomiconacionalurbano.dane.gov.co/images/galerias/safp/CE_Cuestionarioweb_8_SAF.pdf
- Cuestionario web SAFP: https://www.dane.gov.co/files/operaciones/CENU/CUESTIONARIOSAFPVERSINFINAL3.pdf

**Normatividad**
- Proyecto de decreto CENU: https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-2024.pdf
- Memoria justificativa: https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/anex-ProyectoDecretoCENU-MemoriaJustificativa-2024.pdf

**Antecedentes (2020-2022)**
- Nota estadística del conteo 2021: https://www.dane.gov.co/files/investigaciones/notas-estadisticas/feb-2022-censo-economico.pdf
- Presentación del DANE en la CEPAL: https://cepal.org/sites/default/files/presentations/dane-censos-economicos-experiencia-colombia.pdf
- Marco censal: https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/censo-economico-marco-censal.pdf
- Metodológico preliminar Fase III: https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/FASE-III-documento-metodologico-preliminar-censo-economico-2021.pdf

---

## 6. Pendientes y NO CONFIRMADOS (prioridad para el equipo)
1. Bases, retos, criterios, premios y datos de la **Datatón CENU 2026**. Pedirlos a los organizadores (DANE / La Salle).
2. Si los **microdatos del CENU** ya están publicados en ANDA, con qué nivel de anonimización y con qué variables.
3. URL exacta del **visor** de resultados municipales.
4. Fecha y contenido de la **2.ª entrega**. Cifras de **medios de pago**, **contabilidad**, **tiempo de funcionamiento** y **personal ocupado por sector**.
5. Número del decreto o resolución expedido para el CENU y artículo exacto de la Ley 2335 sobre la periodicidad decenal.
6. Resultados de los pilotos de Funza, Ricaurte y Nariño.
7. Puesto exacto del equipo DANE Geoinformación en la UN Datathon 2024.
