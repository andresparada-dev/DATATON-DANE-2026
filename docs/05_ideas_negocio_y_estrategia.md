# 05 · Ideas de negocio, productos de datos y estrategia ganadora — Datatón CENU (DANE)

> Documento de trabajo para un equipo que compite en una datatón de 2 horas (7:50–9:50) con pitch de 5 minutos, usando datos del **Censo Económico Nacional Urbano (CENU)** del DANE.
> Fecha de elaboración: 21-oct-2026. Regla del documento: **toda cifra lleva fuente (URL)**. Donde no se encontró cifra oficial, se dice explícitamente y se marca como "a calcular con el CENU" o "verificar".
> Nota de investigación: los portales `dane.gov.co` y `censoeconomiconacionalurbano.dane.gov.co` no fueron accesibles directamente desde el entorno de investigación (bloqueo de red); las cifras del CENU se tomaron de comunicados citados por prensa económica y de los enlaces oficiales indexados. **Antes del pitch, verificar cada cifra en el visor/boletín oficial.**

---

## Índice

0. [Resumen ejecutivo (para leer en 2 minutos)](#0-resumen-ejecutivo)
1. [Qué es el CENU y qué cifras clave ya existen](#1-qué-es-el-cenu-y-cifras-clave)
2. [Casos internacionales: DENUE (México), Censos Económicos 2024, CENEC (Perú), CNBV](#2-casos-internacionales)
3. [Contexto colombiano por vertical (tiendas TAT, inclusión financiera, formalización, economía popular, género, cuidado, espacio público)](#3-contexto-colombiano-por-vertical)
4. [Mapa de políticas y actores que se benefician](#4-mapa-de-políticas-y-actores)
5. [Métricas e indicadores derivables del censo (con fórmulas y código)](#5-métricas-e-indicadores-con-fórmulas)
6. [18 ideas de negocio / productos de datos / casos de política](#6-ideas-desarrolladas)
7. [Matriz impacto vs factibilidad y Top 3 recomendadas](#7-matriz-impacto-vs-factibilidad-y-top-3)
8. [Estrategia para el día: cronograma 7:50–9:50, roles, checklist](#8-estrategia-para-el-día)
9. [Plantilla de pitch de 5 minutos (con tiempos por diapositiva)](#9-plantilla-de-pitch-de-5-minutos)
10. [Preguntas típicas del jurado y respuestas](#10-preguntas-típicas-del-jurado-y-respuestas)
11. [Snippets de código listos para copiar](#11-snippets-de-código-listos)
12. [Fuentes](#12-fuentes)

---

## 0. Resumen ejecutivo

- **El activo único del CENU** es que, por primera vez en 34 años, Colombia tiene un conteo **georreferenciado de todas las unidades económicas urbanas visibles**, incluyendo la economía popular (viviendas con actividad económica, puestos semifijos y móviles) que no aparece en registros administrativos como Cámaras de Comercio o DIAN. Cifra base: **2.005.613 unidades** en 1.102 municipios ([DANE](https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano)).
- **La brecha que el CENU revela** es la de formalidad: solo **49,16 % tiene RUT** y **47,48 %** reporta registro ante Cámaras/otras entidades ([comunicado DANE 25-may-2026](https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf); [El Universal](https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/)). Y **hay más mujeres propietarias (613.953) que hombres (576.983)** entre quienes respondieron el módulo sociodemográfico ([Forbes Colombia](https://forbes.co/forbes-women/las-mujeres-estan-al-frente-de-mas-de-la-mitad-de-los-negocios-urbanos-de-colombia)).
- **Top 3 recomendadas para ganar** (ver §7):
  1. **"Donde Falta, Emprende"** — mapa de *desiertos* de comercio/servicios esenciales por manzana o celda + recomendación de qué negocio abrir dónde (sirve a emprendedores, alcaldías y financiadores). Factibilidad alta, demo visual muy fuerte.
  2. **"Semáforo de Formalización e Inclusión"** — índice municipal/barrial de brecha de formalidad (RUT/registro) y de acceso financiero, que prioriza dónde enviar brigadas de formalización, Régimen Simple y crédito CREO/FNG. Impacto en política muy alto y alineado con el CONPES de Economía Popular.
  3. **"Ellas Mueven la Economía Popular"** — radiografía territorial de la brecha de género (sectores, formalidad, antigüedad, tamaño) para focalizar programas de crédito y cuidado (Manzanas del Cuidado). Diferenciador narrativo potente con dato oficial nuevo.
- **Plan B (si los datos llegan sucios o tarde):** "Ficha Territorial CENU automática" — un one-pager por municipio generado en Python (densidad, LQ, HHI, formalidad, género). Siempre se puede terminar en 2 horas.
- **Regla de oro del pitch:** 1 usuario concreto + 1 dato que duela + 1 mapa que se entienda en 5 segundos + 1 decisión de política que cambia mañana. Más demo que diapositivas.
- **Riesgo legal que el jurado preguntará:** la **reserva estadística** (art. 5 Ley 79/1993 y art. 37 Ley 2335/2023) prohíbe usar datos individuales del censo para fiscalización o decisiones administrativas sobre una persona ([Ley 79 de 1993](https://www.dane.gov.co/files/noticias/Ley79_1993.pdf); [DANE, respuesta PQR](https://www.dane.gov.co/files/pqr/Respuesta-20241510152151.pdf)). Todas las ideas deben operar con **agregados territoriales**, nunca con "la lista de negocios a fiscalizar".

---

## 1. Qué es el CENU y cifras clave

> Aclaración de nombre: el operativo es el **CENU 2024** (recolección 2.º semestre 2024 – inicios 2025); sus resultados se publican por entregas entre nov-2025 y 2026. En este documento "CENU 2026" = los datos del CENU disponibles en 2026. El próximo censo económico urbano está previsto para 2034 ([La República](https://www.larepublica.co/especiales/empresario-del-ano-2025/piedad-urdinola-en-su-intervencion-en-el-empresario-del-ano-lr-4347556)).

### 1.1 Cobertura y operativo

| Dato | Valor | Fuente |
|---|---|---|
| Unidades económicas visibles urbanas | **2.005.613** | [DANE – resultados preliminares](https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano) |
| Territorio | Áreas urbanas de 1.102 municipios + San Andrés y Providencia + 18 áreas no municipalizadas | ídem |
| Operativo | >8.000 censistas, >500.000 manzanas, cobertura promedio >98,2 %; primer censo "híbrido" (papel + digital) | [Forbes Colombia](https://forbes.co/2025/11/24/economia-y-finanzas/piedad-urdinola-directora-del-dane-perfila-la-colombia-urbana-mas-servicios-mas-calle-y-menos-industria); [Portafolio](https://www.portafolio.co/economia/regiones/en-colombia-hay-mas-de-dos-millones-de-unidades-economicas-segun-el-nuevo-censo-economico-nacional-urbano-del-dane-497881) |
| Ingresos reportados (año ref. 2023) | ~$2.400 billones (según la directora del DANE) | [La República](https://www.larepublica.co/economia/dane-revelara-datos-del-censo-economico-urbano-la-primera-medicion-en-34-anos-4434383) |
| Visor | "Visor interactivo": cada punto del mapa = una unidad observada | [Instructivo visor DANE](https://www.dane.gov.co/files/operaciones/CENU/instructivo_Visor-interactivo.pdf) |
| Documentación técnica | Ficha metodológica (v2, nov-2025) y documento metodológico | [Ficha](https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf); [Doc. metodológico](https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/documento-metodologico-cenu-20251110.pdf) |

### 1.2 Estructura sectorial y territorial

| Dato | Valor | Fuente |
|---|---|---|
| Comercio | 53,1 % (≈1.064.505–1.066.668 unidades; diferencia por versión de base) | [Valora Analitik](https://www.valoraanalitik.com/resultados-del-censo-economico-del-dane-2026/); [Forbes](https://forbes.co/2025/11/11/economia-y-finanzas/comercio-y-servicios-dominan-el-mapa-economico-urbano-de-colombia-segun-el-censo-del-dane) |
| Servicios | 32,3 % (648.375) | ídem |
| Industria | 5,2 % (105.148) | ídem |
| Transporte | 1,1 % | [Valora Analitik](https://www.valoraanalitik.com/censo-economico-del-dane-identifico-mas-de-dos-millones-de-empresas-y-negocios-en-colombia/) |
| Sin CIIU asignado | 7,4 % | [Valora Analitik](https://www.valoraanalitik.com/resultados-del-censo-economico-del-dane-2026/) |
| Bogotá | 360.565 (~18 %) | [Forbes](https://forbes.co/2025/11/24/economia-y-finanzas/piedad-urdinola-directora-del-dane-perfila-la-colombia-urbana-mas-servicios-mas-calle-y-menos-industria) |
| Antioquia / Valle | 250.574 (12,5 %) / 193.974 (9,7 %) | ídem |
| Medellín / Cali | 118.678 / 99.208 | [Valora Analitik](https://www.valoraanalitik.com/censo-economico-del-dane-identifico-mas-de-dos-millones-de-empresas-y-negocios-en-colombia/) |
| Venta en calle | **219.042** (~11 %, "uno de cada diez") — Bogotá 42.097, Antioquia 21.617, Valle 19.326 | [Portafolio](https://www.portafolio.co/economia/crecimiento/uno-de-cada-10-negocios-en-colombia-hace-parte-de-las-ventas-ambulantes-482970); [La República](https://www.larepublica.co/economia/los-vendedores-de-calle-son-11-de-los-negocios-urbanos-4268116) |

> ⚠️ No se encontró en fuentes verificables un desglose oficial reconciliado por **emplazamiento** (fijo / vivienda / semifijo / móvil). Calcularlo con la base del CENU el día de la datatón.

### 1.3 Formalidad y propietarios (entregas 2026)

| Dato | Valor | Fuente |
|---|---|---|
| Unidades con RUT | **49,16 %** (37,3 % sin RUT; 13,5 % sin información) | [Comunicado DANE 25-may-2026](https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf); [El Universal](https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/) |
| Registradas ante Cámaras de Comercio y otras entidades | >734.000 (47,48 %) — *verificar la base del porcentaje* | ídem |
| Bolívar con Registro Mercantil | 23,88 % | [El Universal](https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/) |
| Uso de saberes ancestrales | 11.776 unidades (1,11 %) | [Comunicado DANE](https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf) |
| Propietarias mujeres vs hombres | **613.953 vs 576.983** (diferencia 3,1 %) sobre 1.190.936 unidades que respondieron el módulo (59,4 % del total) | [Forbes Colombia](https://forbes.co/forbes-women/las-mujeres-estan-al-frente-de-mas-de-la-mitad-de-los-negocios-urbanos-de-colombia); [DANE cp Tercera entrega](https://www.dane.gov.co/files/prensa/comunicados/cp-TerceraEntregaCENU.pdf) |
| Edad de propietarios | Mayor concentración entre 35 y 59 años | [Portafolio](https://www.portafolio.co/negocios/empresas/colombia-es-un-pais-de-empresas-que-apenas-estan-naciendo-donde-la-universidad-no-es-regla-para-emprender-498739) |

### 1.4 Variables típicas con las que trabajar (confirmar con el diccionario que entregue la organización)

Identificador anonimizado · coordenadas / manzana (MGN) · municipio / localidad / comuna · **emplazamiento** (establecimiento fijo, vivienda con actividad económica, puesto semifijo, puesto móvil) · **CIIU Rev. 4 A.C.** (sección, división, clase) · **personal ocupado** (total, por sexo, remunerado/no) · **RUT, registro mercantil, contabilidad** · **tiempo de funcionamiento** · sexo/edad/educación/autorreconocimiento del propietario (módulo sociodemográfico) · uso de saberes ancestrales · ingresos (para el subconjunto con cuestionario de empresa).

**Datos complementarios útiles** (descargar ANTES del evento): proyecciones de población DANE por municipio y CNPV 2018 por manzana; MGN (Marco Geoestadístico Nacional) de manzanas/secciones; puntos de acceso financiero (Banca de las Oportunidades/SFC); EMICRON; estratificación; red de transporte (GTFS/TransMilenio); POT/usos del suelo; mapas de amenaza (inundación/remoción); equipamientos (Manzanas del Cuidado, colegios, hospitales); registros de Cámaras de Comercio (agregados por CIIU/municipio).

---

## 2. Casos internacionales

### 2.1 México — INEGI DENUE (Directorio Estadístico Nacional de Unidades Económicas)

- **Qué es:** directorio georreferenciado derivado de los Censos Económicos y actualizaciones, con **>5 millones de establecimientos**; cada registro trae nombre, razón social, clase SCIAN, **estrato de personal ocupado**, dirección, teléfono, web y **latitud/longitud** ([API DENUE](https://en.www.inegi.org.mx/servicios/api_denue.html)). En nov-2020 tenía 5.546.698 negocios y cuenta con app móvil ([boletín INEGI 2020](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2020/OtrTemEcon/DENUE2020.pdf)). Boletines recientes: [DENUE 2025](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/denue/denue2025_05.pdf), [DENUE 2026](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/denue/DENUE2026_05.pdf).
- **API:** búsqueda por palabra clave o **por coordenada + radio (máx. 5.000 m)**, con token gratuito ([API DENUE](https://en.www.inegi.org.mx/servicios/api_denue.html)). Este es exactamente el patrón "¿qué hay a mi alrededor?" que habilita *site selection*.
- **Usos documentados por INEGI:** estudios de mercado y análisis de competencia; búsqueda de **clientes potenciales** (ej. una panadería que localiza cafeterías cercanas); identificación de **proveedores nacionales** y cadenas de suministro; detección de tendencias (ej. crecimiento de negocios de motocicletas asociado a entregas de e-commerce en Tonalá, Jalisco) ([fuente INEGI vía búsqueda API/DENUE](https://en.www.inegi.org.mx/servicios/api_denue.html); [boletín DENUE 2026](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/denue/DENUE2026_05.pdf)).
- **Uso académico/analítico:** segmentación geográfica con CRISP-DM sobre DENUE ([Revista de Ingeniería UNAM 2020](https://www.revistaingenieria.unam.mx/numeros/2020/v21n1-08.pdf)); librería R `inegiR` para consumir la API ([manual inegiR](https://eflores89.r-universe.dev/inegiR/doc/manual.html)).
- **Lección para Colombia:** el valor no está solo en el conteo, sino en **(i) API abierta con consulta por radio, (ii) actualización periódica y (iii) estrato de tamaño por establecimiento**. Una propuesta de datatón que diga "esto es el DENUE colombiano para X usuario" es inmediatamente entendible por un jurado.
- *Nota honesta:* no se encontraron casos documentados y verificables de **startups específicas** construidas sobre DENUE; no se citan nombres para no inventar.

### 2.2 México — Censos Económicos 2024 (resultados oportunos)

- ~**5,45 millones de unidades económicas**; **95,5 % micro** (≤10 personas); grandes (≥251) 0,2 % ([INEGI CE 2024 RO](https://inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_RO_Nal.pdf)). Tabulados interactivos (SAIC) y mapa de datos municipal ([SNIEG](https://www.snieg.mx/Documentos/Economico/sesiones/doc_22024/3_avances_censos_econ_2024.pdf)).
- Lección: el producto estadístico se vuelve "producto de datos" cuando hay **tabulados por área + mapa + API**.

### 2.3 México — CNBV: geografía de la inclusión financiera

- Medición por **radio**: ~21 millones de personas (≈19 %) sin sucursal, corresponsal o cajero a **2 km** ([IDC Online, sobre CNBV](https://idconline.mx/corporativo/2020/01/06/19-de-los-mexicanos-no-tiene-un-banco-cerca)).
- A 2023-T2, 84,2 % de municipios con al menos un punto de acceso; 38 % de los municipios rurales sin cobertura ([BBVA Research](https://www.bbvaresearch.com/publicaciones/mexico-en-2023-2t-99-de-adultos-en-municipios-con-punto-de-acceso-creditocaptacion/)).
- Lección: la métrica de **"distancia al punto de acceso más cercano"** es directamente replicable en Colombia cruzando CENU (unidades de la clase CIIU de bancos/corresponsales o la base de puntos de acceso de la SFC) con la localización de las unidades de la economía popular → **"desiertos financieros para negocios"**, no solo para personas.

### 2.4 Perú — INEI CENEC (V Censo Nacional Económico 2022)

- Primera fase (Censo de Establecimientos): **2.367.085 locales**, de los cuales **1.897.539 (80,2 %) operativos** y 469.546 cerrados/alquilados/en venta/desocupados; el censo de 2008 registró 940.336 ([Gestión](https://gestion.pe/economia/hay-23-millones-de-locales-para-negocio-en-peru-cuantos-se-alquilan-noticia/)).
- Fase 2: encuesta a grandes, medianas y pequeñas empresas (jun–dic 2022); resultados definitivos con agregados (producción, consumo intermedio, valor agregado) ([INEI, presentación CEPAL](https://cepal.org/sites/default/files/presentations/inei-censos-economicos-quinto-censo-nacional-peru.pdf); [INEI publicaciones](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1924/Libro21.pdf)).
- Lección: **contar también locales cerrados/desocupados** genera un indicador de **vacancia comercial** muy útil para inmobiliarias y renovación urbana. Si el CENU trae estado del local, es una idea extra (ver idea 17).

### 2.5 Bogotá — "ciudad de 15 minutos"

- Un estudio difundido por La Silla Vacía halló que tiendas de alimentos, comercios locales, restaurantes, farmacias y colegios están a <15 minutos a pie para **casi el 80 %** de la población, pero con **desigualdades socioeconómicas** significativas ([La Silla Vacía](https://www.lasillavacia.com/?p=250624); [Streetsblog](https://sf.streetsblog.org/2024/03/18/want-a-better-15-minute-city-ask-residents-what-they-really-want)).
- Lección: el CENU permite **recalcular esta métrica con el universo completo de negocios** (incluida la economía popular), algo que fuentes como OpenStreetMap o Google Places subrepresentan en barrios populares.

---

## 3. Contexto colombiano por vertical

### 3.1 Tiendas de barrio / canal tradicional / TAT ("tienda a tienda")

| Dato | Valor | Fuente |
|---|---|---|
| Tiendas de barrio (NielsenIQ) | 453.750 (13,1 % de 3.458.544 establecimientos tradicionales en LatAm) | [Pulzo / Mall y Retail](https://www.pulzo.com/economia/cuantas-tiendas-barrio-hay-colombia-alentador-dato-sus-duenos-PP5289158A) |
| Peso en ventas de consumo masivo | ~37 % (NielsenIQ); ~48 % formatos tradicionales (Fenalco) | [Pulzo](https://www.pulzo.com/economia/cuantas-tiendas-barrio-hay-colombia-alentador-dato-sus-duenos-PP5289158A); [El Colombiano](https://www.elcolombiano.com/negocios/dia-del-tendero-en-colombia-NL28890397) |
| Tiendas de barrio (Fenalco) | ~450.000, con ~1,1 millones de empleos directos | [Comunicado Fenalco 2024 (Ámbito Jurídico)](https://www.ambitojuridico.com/sites/default/files/2024-08/COMUNICADO-Ventasdelas-2024.pdf) |
| Ventas 1S-2024 | Ver nota | [Portafolio](https://www.portafolio.co/negocios/comercio/cuanto-crecieron-las-ventas-de-las-tiendas-de-barrio-de-colombia-en-el-primer-semestre-de-2024-609827) |
| Riesgo de cierre | "Unas 11.000 tiendas en peligro de desaparecer" | [Portafolio](https://www.portafolio.co/negocios/unas-11-000-tiendas-estan-en-peligro-de-desaparecer-555185) |
| Competencia de *hard discount* | Desplazamiento hacia D1 y Ara | [Portafolio](https://www.portafolio.co/negocios/empresas/los-colombianos-han-desplazado-las-tiendas-por-d1-y-ara-501143) |
| Startups B2B para tenderos | **Chiper**: Serie A US$12M (2020), Serie B US$53M (2021) con meta de 100.000 tiendas; según su CEO solo **0,1 %** de transacciones en tiendas era electrónica | [Forbes 2020](https://forbes.co/emprendedores/chiper-levanta-us12-millones-digitalizando-las-tiendas-de-barrio); [Forbes 2021](https://forbes.co/2021/11/18/emprendedores/chiper-buscara-atender-100-000-tiendas-de-barrio-tras-recaudar-us53-millones/) |
| Fracasos del sector | **Frubana** cerró en 2025 tras recaudar >US$270M | [El Colombiano](https://www.elcolombiano.com/negocios/historia-detras-cierre-frubana-y-merqueo-colombia-america-latina-LP29733329) |

**Por qué importa para la datatón:** el universo de tiendas lo estiman privados (Nielsen/Fenalco) con cifras que no coinciden; **el CENU puede dar el conteo oficial y georreferenciado por CIIU 4711 (comercio al por menor en establecimientos no especializados con surtido compuesto principalmente por alimentos, bebidas o tabaco)** y similares. Para distribuidores TAT y fintechs B2B, eso es *TAM georreferenciado*. El caso Frubana es útil para el pitch: "la logística de última milla al tendero falla cuando no se conoce la densidad real" (argumento, no cifra).

### 3.2 Inclusión financiera y crédito

| Dato | Valor | Fuente |
|---|---|---|
| Adultos con al menos un producto financiero (2024) | **96,3 %** | [Superfinanciera](https://www.superfinanciera.gov.co/publicaciones/10115642/para-2024-el-963-de-los-colombianos-adultos-tenia-al-menos-un-producto-de-deposito-o-credito/); [RIF 2024 BdO](https://www.bancadelasoportunidades.gov.co/sites/default/files/2025-06/BDO_RIF%202024_20062025.pdf) |
| Acceso a crédito del sistema financiero | **35,5 %** (50,5 % incluyendo sector real) | [Portafolio](https://www.portafolio.co/economia/finanzas/en-2024-el-96-3-de-adultos-tenia-un-producto-financiero-631786) |
| Motivación del programa CREO | Solo ~30 % de micronegocios con financiación formal y 1 de cada 4 que pidió crédito acudió al "gota a gota" (EMICRON) | [Forbes 2023](https://forbes.co/2023/03/28/economia-y-finanzas/gobierno-promovera-acceso-al-credito-para-frenar-los-gota-a-gota) |
| CREO (Banca de las Oportunidades) | 15.779 beneficiarios y $28.649 millones desembolsados a 31-ene-2024; Caribe la región más beneficiada | [Portafolio](https://www.portafolio.co/mis-finanzas/creditos/programa-creo-iniciativa-para-combatir-gota-a-gota-ha-desembolsado-mas-de-28-000-millones-de-pesos-601038) |
| Fondo Nacional de Garantías | ~$15,1 billones respaldados y >610.000 garantías a agosto de 2025 | [La República](https://www.larepublica.co/finanzas/el-fondo-nacional-de-garantias-respaldo-15-1-billones-en-creditos-con-corte-a-agosto-4217873) |
| FNG y microempresarios | Coberturas de hasta 90 %; cartera de microcrédito +11 % al cierre de 2025; productos específicos para economía popular | [La República](https://www.larepublica.co/finanzas/fondo-nacional-de-garantias-asegura-que-perfil-de-riesgo-de-microempresarios-cayo-50-4437280) |
| Bogotá (SDDE) | Microcréditos sin interés de $50.000 a $500.000 (2024) para emprendedores formales e informales | [Pulzo](https://www.pulzo.com/economia/prestamos-bogota-intereses-con-secretaria-desarrollo-economico-PP3966348) |
| Puntos de acceso (histórico) | Jun-2018: 7.797 oficinas y 565.043 puntos de acceso; 835 de 1.102 municipios con oficina | [BdO Cobertura 2018](https://www.bancadelasoportunidades.gov.co/sites/default/files/2019-02/Cobertura%20primer%20semestre%202018.pdf) |

**Lectura:** el problema ya no es la tenencia de cuenta sino el **crédito productivo** y su **focalización territorial**. El CENU ofrece el "denominador" que no tenían CREO/FNG: dónde están físicamente las unidades de la economía popular y qué tan lejos están de un punto de acceso.

### 3.3 Formalización

| Dato | Valor | Fuente |
|---|---|---|
| RUT en unidades CENU | 49,16 % | ver §1.3 |
| Régimen Simple de Tributación | ~157.000 inscritos en 2024, ~133.000 activos | [Actualícese](https://actualicese.com/contribuyentes-en-el-regimen-simple-de-tributacion/) |
| Empresas creadas 1S-2025 (RUES) | 173.907 (+1,9 %); 74 % personas naturales | [Confecámaras](https://confecamaras.org.co/wp-content/uploads/2025/08/2025-1-dinamica-de-creacion-de-empresas.pdf) |
| Bogotá-Región empresas activas (ene–nov 2025) | 496.686 | [Portafolio / CCB](https://www.portafolio.co/negocios/empresas/la-creacion-de-empresas-aumento-6-en-bogota-y-cundinamarca-hasta-noviembre-segun-la-camara-de-comercio-485224) |
| Micronegocios (EMICRON) | >5,2 millones; >1,6 millones operan desde la vivienda (+9,8 % 2023→2024) | [Forbes Colombia, sep-2026](https://forbes.co/2026/09/29/negocios/el-30-de-los-micronegocios-en-colombia-opera-desde-una-vivienda-dane/) |
| Micronegocios en Bogotá | 510.090 (2023) → 589.110 (2024) | [Alcaldía de Bogotá](https://bogota.gov.co/en/node/269302) |
| Vendedores ambulantes (EMICRON 2024) | 507.266 micronegocios (+5,3 %) | [Boletín DANE EMICRON Vendedores Ambulantes 2024](https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRONVendedoresAmbulantes-2024.pdf) |

> Nota: EMICRON (encuesta, incluye rural y trabajo por cuenta propia no visible) y CENU (censo de unidades **visibles urbanas**) **no son comparables 1:1**; esa diferencia es en sí un hallazgo ("economía invisible") pero debe explicarse con cuidado en el pitch.

### 3.4 Economía popular (PND 2022–2026 y CONPES)

- **Definición PND:** oficios y ocupaciones mercantiles y no mercantiles realizados por unidades de **baja escala** (personales, familiares, micronegocios o microempresas) en cualquier sector (Transformación 7 de las Bases del PND) ([Bloomberg Línea](https://www.bloomberglinea.com/latinoamerica/colombia/plan-de-desarrollo-medicion-de-la-economia-popular-que-plantea-petro-ya-existe/)).
- **Art. 90, Ley 2294 de 2023:** el DANE debe diseñar e implementar un **Sistema de Información de la Economía Popular (SIEP)** a partir de registros administrativos, operaciones estadísticas y fuentes alternativas, compartible con entidades para **micro-focalización** de políticas ([DANE – proyecto de resolución SIEP](https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/doc-SG-ProyectoSIEP-2023.pdf)).
- **Meta PND:** aumentar 6 % los ingresos de los micronegocios de la economía popular ([Bloomberg Línea](https://www.bloomberglinea.com/latinoamerica/colombia/como-va-la-medicion-y-caracterizacion-de-la-economia-popular-gobierno-responde/)).
- **DANE, Nota Estadística N.º 1 de 2026 "Economía Popular mercantil en datos"** ([PDF DANE](https://www.dane.gov.co/files/investigaciones/notas-estadisticas/nota-EconomiaPopular-2026.pdf)).
- **CONPES de Política Nacional de Economía Popular:** formulado con proceso participativo liderado por el DNP ([DNP](https://dnp.gov.co/Prensa_/Noticias/Paginas/dnp-socializa-la-ruta-de-participacion-para-formulacion-conpes-economia-popular.aspx); [Valora Analitik](https://www.valoraanalitik.com/economia-popular-tendra-conpes-dnp/)); según ICEF fue **aprobado en 2026**, con horizonte 2026–2036, 54 acciones estratégicas, dirigido a >12 millones de personas y 5,3 millones de micronegocios ([ICEF](https://www.icef.com.co/component/k2/item/8483-gobierno-nacional-aprueba-el-conpes-de-economia-popular)) — *verificar número y presupuesto en el documento CONPES oficial*.
- **Relación con el CENU:** el CENU es la primera operación que **caracteriza explícitamente unidades visibles de la economía popular** (viviendas con actividad económica, puestos semifijos y móviles) ([Confecámaras, documento economía popular](https://confecamaras.org.co/wp-content/uploads/2024/09/economia-popular-sep-3-1.pdf)). En el pitch: **"el CENU es el marco muestral y el mapa base del SIEP"**.

### 3.5 Género, cuidado y emprendimiento

- Más propietarias que propietarios entre unidades con módulo sociodemográfico (613.953 vs 576.983) ([Forbes Colombia](https://forbes.co/forbes-women/las-mujeres-estan-al-frente-de-mas-de-la-mitad-de-los-negocios-urbanos-de-colombia)).
- iNNpulsa: brecha de **12 p.p.** a favor de hombres en la probabilidad de tener oferta innovadora; las diferencias de desempeño no se explican solo por el sexo del propietario ([iNNpulsa – brechas en innovación](https://innpulsacolombia.com/wp-content/uploads/2024/11/BRECHAS-DE-GENERO-EN-LA-INNOVACION.pdf); [iNNpulsa – brechas en desempeño](https://innpulsacolombia.com/wp-content/uploads/2024/11/BRECHAS-DE-GENERO-EN-EL-DESEMPENO-EMPRESARIAL.pdf)).
- Bogotá: **27 Manzanas del Cuidado** al cierre de 2025, meta 31 en el cuatrienio; >297.000 personas atendidas en 2025 ([Alcaldía de Bogotá](https://bogota.gov.co/mi-ciudad/mujer/bogota-fortalecio-su-sistema-distrital-de-cuidado-durante-2025)).
- Hipótesis a testear con CENU (no son cifras): las mujeres concentran unidades en vivienda y en sectores de menor escala (alimentos, belleza, confección); la co-localización vivienda-negocio es una estrategia de conciliación con el trabajo de cuidado → la oferta de cuidado cercana debería aumentar horas/ingresos.

### 3.6 Espacio público y venta en calle

- 219.042 unidades de venta en calle (CENU) y diferencia semifijo (puesto fijo en un lugar) vs ambulante (se desplaza) según la directora del DANE ([Portafolio](https://www.portafolio.co/economia/crecimiento/uno-de-cada-10-negocios-en-colombia-hace-parte-de-las-ventas-ambulantes-482970)).
- Bogotá: fondos rotatorios de crédito con IPES para vendedores informales; programas locales "Impulso Local" y "El Taller de las Microempresas" (planes locales 2025–2028) ([Alcaldía de Bogotá](https://bogota.gov.co/mi-ciudad/desarrollo-economico/bogota-fortalecio-100000-micronegocios-en-menos-de-cuatro-anos); [Secretaría de Gobierno](https://gobiernobogota.gov.co/sites/default/files/2026-04/DTS-2826-007-23-01-2026_0.pdf)).

### 3.7 Turismo

- El DANE tiene un boletín CENU de **turismo** ([bol-CENU-Turismo-2023](https://www.dane.gov.co/files/operaciones/CENU/bol-CENU-Turismo-2023.pdf)) — revisar alcance. Con CIIU 55 (alojamiento), 56 (expendio de alimentos y bebidas) y 79 (agencias de viaje) se mide la oferta turística georreferenciada por municipio.

---

## 4. Mapa de políticas y actores

| Actor | Qué decide / necesita | Qué le da el CENU | Idea(s) asociada(s) |
|---|---|---|---|
| **DNP / Consejo Nacional de Economía Popular / CONPES EP** | Focalizar 54 acciones en territorio; línea base y seguimiento | Línea base georreferenciada de unidades populares por municipio/manzana | 4, 7, 18 |
| **DANE (SIEP)** | Sistema de información de economía popular (art. 90 Ley 2294) | Marco censal para el SIEP | 7, 18 |
| **MinCIT / iNNpulsa / CEmprende** | Dónde poner centros CEmprende, programas de fortalecimiento, reindustrialización | Densidad, especialización (LQ), clústeres | 1, 12, 16 |
| **Banca de las Oportunidades (CREO), Banco Agrario, FNG, Bancóldex** | Dónde colocar crédito y garantías, diseño de productos | Desiertos financieros; riesgo-entorno; antigüedad | 3, 4, 5 |
| **DIAN (Régimen Simple)** | Estrategia de formalización *amigable* (pedagogía, no fiscalización individual) | Brecha de RUT agregada por sector/territorio | 4 |
| **Cámaras de Comercio / Confecámaras** | Campañas de matrícula mercantil y servicios empresariales | Brecha registro mercantil por zona; mercado potencial de afiliados | 4, 16 |
| **Alcaldías (Planeación, Hacienda, Desarrollo Económico; en Bogotá: SDDE, IPES, SDMujer)** | POT, usos del suelo, espacio público, ICA, cuidado, plazas de mercado | Usos reales del suelo, venta en calle, desiertos de servicios | 2, 8, 9, 10, 11, 14, 15 |
| **Empresas de consumo masivo / distribuidores TAT / fintech B2B** | Expansión de rutas, cobertura, *share of shelf* | TAM georreferenciado de tiendas | 6, 5 |
| **Aseguradoras / microseguros** | Exposición de negocios a riesgo | Unidades por zona de amenaza | 14 |
| **Emprendedores / inmobiliarias / franquicias** | Dónde abrir | Saturación vs demanda | 1, 17 |
| **Secretarías de movilidad** | Zonas de cargue y descargue, rutas | Densidad de personal ocupado y tipo de actividad | 15 |

---

## 5. Métricas e indicadores con fórmulas

Notación: *i* = sector (CIIU), *j* = territorio (municipio, localidad, manzana, celda H3), *E* = número de unidades (o personal ocupado), *P* = población.

### 5.1 Densidad empresarial
$$D_j = \frac{E_j}{P_j}\times 1000$$
Unidades por 1.000 habitantes. Variante por superficie: $E_j / \text{km}^2_j$. **Interpretación:** densidad alta con baja diversidad = posible saturación; densidad baja en zona residencial poblada = posible desierto. *Población:* proyecciones DANE municipales o CNPV 2018 por manzana.

### 5.2 Cociente de localización (LQ) — especialización
$$LQ_{ij} = \frac{E_{ij}/E_j}{E_i/E}$$
LQ > 1: el territorio *j* está especializado en *i* relativo al país (o a la ciudad). Usar umbral práctico LQ ≥ 1,25 con un mínimo de unidades (p.ej. ≥ 30) para evitar ruido. Referencias de uso municipal: [Scielo – Región y Sociedad](https://www.scielo.org.mx/img/revistas/regsoc/v16n31/html/a1an1.html); [CEPAL](https://repositorio.cepal.org/bitstreams/655c13be-c321-4767-80bc-24cd44e97399/download).

### 5.3 Índice Herfindahl-Hirschman (HHI) — concentración / diversificación sectorial
$$HHI_j = \sum_{i=1}^{n} s_{ij}^2,\qquad s_{ij}=\frac{E_{ij}}{E_j}$$
Rango [1/n, 1]. Normalizado: $HHI^*_j = \frac{HHI_j - 1/n}{1 - 1/n}$. Diversificación = $1 - HHI_j$. Alternativa: entropía de Shannon $H_j = -\sum_i s_{ij}\ln s_{ij}$. Uso en ciudades: [CREEBBA Bahía Blanca](https://creebba.org.ar/iae/iae125/Caracteristicas_estructurales_de_la_economia_local_IAE_125.pdf); [PUCE Ecuador](https://repositorio.puce.edu.ec/server/api/core/bitstreams/bfcd9864-b368-44d2-a351-162f28ad0ddb/content).
*Uso adicional (competencia de mercado):* HHI de cuota de personal ocupado entre unidades de un mismo CIIU en un radio → mide si un mercado local está dominado por pocos actores.

### 5.4 Índice de formalidad (y brecha)
$$F^{RUT}_j = \frac{\#\{u\in j: RUT=1\}}{\#\{u\in j: RUT\ \text{informado}\}}$$
Análogo para registro mercantil ($F^{RM}$) y contabilidad. **Índice compuesto** (0–1): $F_j = \frac{1}{3}(F^{RUT}_j + F^{RM}_j + F^{CONT}_j)$. **Brecha:** $B_j = F_{\text{ref}} - F_j$ (ref = promedio nacional o meta). **Potencial de formalización** (número absoluto a priorizar): $PF_j = E_j\,(1 - F_j)$ → ordena territorios por *cuántas* unidades podrían formalizarse, no solo por porcentaje. Excluir "sin información" del denominador y reportarlo aparte.

### 5.5 Supervivencia / antigüedad (con advertencia metodológica)
Con un censo transversal **no se observa la mortalidad**; solo la distribución de antigüedad de las **sobrevivientes**. Indicadores defendibles:
- Proporción de unidades jóvenes: $J_j = \frac{\#\{u: t_u < 2\ \text{años}\}}{E_j}$.
- Proporción consolidada: $C_j = \frac{\#\{u: t_u \ge 5\}}{E_j}$.
- **Pseudo-supervivencia** (supuesto de flujo de entrada estable): $\hat S(k)=\frac{N(t\ge k)}{N(t\ge 0)}$ por cohortes; *solo como proxy*. Para supervivencia real cruzar con cohortes de Confecámaras (empresas formales).
- Antigüedad mediana por sector y por sexo del propietario.

### 5.6 Clústeres espaciales
- **DBSCAN** (puntos): parámetros `eps` (radio, p.ej. 150 m en métrica haversine) y `min_samples` (p.ej. 15). Punto *núcleo* si $|N_\varepsilon(p)| \ge \text{minPts}$; clúster = componentes conectados de núcleos. Útil para detectar ejes comerciales y aglomeraciones de venta en calle.
- **I de Moran global** (autocorrelación espacial de una variable agregada $x$ por celda):
$$I = \frac{n}{W}\,\frac{\sum_i\sum_j w_{ij}(x_i-\bar x)(x_j-\bar x)}{\sum_i (x_i-\bar x)^2},\quad W=\sum_i\sum_j w_{ij}$$
I > 0 y significativo (permutaciones) → valores similares se agrupan.
- **LISA (Moran local)**: $I_i = \frac{(x_i-\bar x)}{m_2}\sum_j w_{ij}(x_j-\bar x)$, $m_2=\frac{\sum_i (x_i-\bar x)^2}{n}$ → clasifica alto-alto, bajo-bajo, alto-bajo, bajo-alto.
- **Getis-Ord Gi\*** (hot spots):
$$G_i^* = \frac{\sum_j w_{ij}x_j - \bar X\sum_j w_{ij}}{S\sqrt{\frac{n\sum_j w_{ij}^2-(\sum_j w_{ij})^2}{n-1}}},\quad S=\sqrt{\frac{\sum_j x_j^2}{n}-\bar X^2}$$
Es un z-score: > 1,96 hot spot (95 %), < −1,96 cold spot ([Esri – Hot Spot Analysis](https://doc.esri.com/en/arcgis-pro/3.7/tool-reference/spatial-statistics/hot-spot-analysis.html); Getis & Ord, 1992, *Geographical Analysis* 24(3)). En Python: `esda.G_Local(..., star=True)` y `esda.Moran` (PySAL).

### 5.7 Accesibilidad a servicios
- **Distancia al más cercano:** $d_u = \min_{s\in S} \text{haversine}(u, s)$, con $S$ = unidades de un tipo (farmacia CIIU 4773, tienda 4711/4721–4729, ferretería 4752, corresponsal/banco 6412…). Reportar % de población (o de manzanas) con $d > 500$ m / 1 km.
- **Cobertura en buffer:** $A_j = \#\{s\in S: d(j,s)\le r\}$.
- **2SFCA (Two-Step Floating Catchment Area)** — oferta vs demanda:
  Paso 1: $R_s = \frac{O_s}{\sum_{k: d_{ks}\le d_0} P_k}$ (oferta $O_s$, p.ej. personal ocupado de la unidad); Paso 2: $A_k = \sum_{s: d_{ks}\le d_0} R_s$.

### 5.8 "Desiertos" de comercio / servicios / finanzas
Definición operativa propuesta (parametrizable): una manzana/celda *k* es **desierto de servicio S** si (a) tiene población residente $P_k \ge P_{min}$ (p.ej. 100 hab.) y (b) $d_k(S) > r$ (p.ej. 500 m caminando para tienda/farmacia; 1–2 km para punto financiero). **Índice de desierto** municipal: $DS = \frac{\sum_{k\in\text{desierto}} P_k}{\sum_k P_k}$. Para negocios: % de unidades de la economía popular a > 1 km de un punto de acceso financiero (paralelo a la métrica de CNBV en México).

### 5.9 Saturación competitiva (para *site selection*)
$$Sat_{i,k} = \frac{\#\{u\in CIIU_i: d(u,k)\le r\}}{P_k(r)/1000}\Big/\ \text{mediana}_{\text{ciudad}}(\cdot)$$
Sat > 1 = más competencia por habitante que la mediana; Sat < 1 = oportunidad (si hay demanda).

### 5.10 Brecha de género
- Participación femenina: $M_j = \frac{\#\{u: \text{propietaria}=M\}}{\#\{u: \text{sexo informado}\}}$.
- Brecha en formalidad: $\Delta F = F^{H} - F^{M}$; en tamaño: $\Delta PO = \overline{PO}^H - \overline{PO}^M$; en antigüedad: medianas.
- **Índice de disimilitud de Duncan** (segregación sectorial): $DI = \frac12\sum_i \left|\frac{M_i}{M} - \frac{H_i}{H}\right|$ (0 = misma distribución sectorial; 1 = segregación total).
- Brecha ajustada: regresión logística $\Pr(RUT=1) = \Lambda(\beta_0 + \beta_1 \text{Mujer} + \gamma\,\text{CIIU} + \delta\,\text{emplazamiento} + \theta\,\text{municipio})$ → la brecha que queda tras controlar sector y lugar.

### 5.11 Otros útiles
- **Tamaño medio**: $\overline{PO}_j = PO_j/E_j$. **% micro** (≤ 10 PO).
- **Índice de economía popular** (propuesto): $EP_j = \frac{\#\{u: \text{emplazamiento}\in\{\text{vivienda, semifijo, móvil}\}\ \lor\ PO_u\le 2\}}{E_j}$ — documentar el criterio.
- **Coeficiente de especialización de Krugman** entre dos territorios: $K_{jk} = \sum_i |s_{ij} - s_{ik}|$.
- **Mezcla de usos (entropía de uso del suelo)** por celda, útil para POT: $H_k/\ln(n)$.

---

## 6. Ideas desarrolladas

Formato por idea: **Problema · Usuario/cliente · Datos CENU · Datos complementarios · Solución · Métricas · Modelo de negocio/sostenibilidad · Impacto social · MVP en 2 horas · Complejidad (1–5)**.

---

### Idea 1 — "Donde Falta, Emprende" (desiertos de servicios esenciales + oportunidad de negocio) ⭐ TOP 1

- **Problema:** en barrios populares faltan servicios cotidianos (farmacia, droguería, tienda de alimentos, papelería, ferretería, cuidado infantil) mientras otras zonas están saturadas del mismo tipo de negocio. Emprendedores abren "donde ven" y no "donde falta", y la alcaldía no sabe dónde promover qué.
- **Usuario/cliente:** (a) emprendedor/a de economía popular y programas que lo acompañan (CEmprende, SDDE, CREO); (b) Secretarías de Planeación (POT, ciudad de 15 minutos); (c) cadenas/franquicias y distribuidores.
- **Datos CENU:** coordenadas, CIIU, emplazamiento, personal ocupado.
- **Complementarios:** población por manzana (CNPV 2018/proyecciones), MGN, estrato (opcional).
- **Solución:** grilla H3 (res. 9 ≈ 0,1 km²) o manzana → para cada servicio esencial calcula distancia al más cercano y saturación (§5.7–5.9). Produce (1) **mapa de desiertos**, (2) **ranking "oportunidad = demanda alta × oferta baja"** por tipo de negocio, (3) ficha "Si vas a abrir una droguería, estas 10 zonas tienen ≥ X habitantes sin una a 500 m".
- **Métricas:** % población en desierto por servicio; Sat por CIIU; # oportunidades identificadas; Índice de desierto municipal.
- **Modelo de negocio:** gratuito para emprendedores/alcaldías (financiado por convenio con alcaldías, Cámaras, banca de desarrollo); **premium B2B** para franquicias, inmobiliarias y distribuidores (API "consulta por radio" estilo DENUE); licenciamiento a gremios.
- **Impacto social:** reduce tiempos de desplazamiento por bienes básicos; aumenta probabilidad de supervivencia de nuevos negocios al evitar saturación; insumo directo para el POT y la "ciudad de 15 minutos" ([La Silla Vacía](https://www.lasillavacia.com/?p=250624)).
- **MVP 2h:** 1 ciudad (p.ej. Bogotá o la ciudad del dataset), 4 servicios, mapa folium/kepler + tabla top-10 oportunidades + 1 indicador nacional. **Muy viable.**
- **Complejidad:** 2/5.

---

### Idea 2 — "Ciudad de 15 Minutos Real" (accesibilidad con economía popular incluida)

- **Problema:** las métricas de proximidad se calculan con OSM/Google, que subrepresentan negocios informales; se sobrestiman los desiertos en barrios populares y se subestiman las brechas de calidad.
- **Usuario:** Secretaría de Planeación, Secretaría de Movilidad, academia, organismos multilaterales.
- **Datos CENU:** puntos por CIIU, emplazamiento (para separar formal-fijo vs popular).
- **Complementarios:** red peatonal (OSM con `osmnx`) o distancias euclidianas, población por manzana, equipamientos públicos.
- **Solución:** índice de proximidad por manzana (n.º de categorías esenciales a ≤ 1.000 m / 15 min a pie) con y sin economía popular → "cuánto de la ciudad de 15 minutos la sostiene la economía popular".
- **Métricas:** % población con ≥ 8 de 10 categorías a 15 min; contribución de la economía popular (Δ índice).
- **Modelo:** consultoría/plataforma para planeación urbana; publicación académica; convenio con BID/CAF.
- **Impacto:** argumento con evidencia para **regular y no erradicar** la economía popular que da proximidad.
- **MVP 2h:** euclidiano (sin red) en una ciudad; mapa comparativo "con vs sin popular". **Viable.**
- **Complejidad:** 3/5.

---

### Idea 3 — "Desiertos Financieros para Negocios"

- **Problema:** la inclusión financiera se mide por personas (96,3 % con producto: [SFC](https://www.superfinanciera.gov.co/publicaciones/10115642/para-2024-el-963-de-los-colombianos-adultos-tenia-al-menos-un-producto-de-deposito-o-credito/)), pero el crédito productivo es bajo (35,5 %) y no se sabe **dónde** están los negocios sin acceso físico/digital.
- **Usuario:** Banca de las Oportunidades, Banco Agrario (CREO), bancos y cooperativas, fintech, redes de corresponsales.
- **Datos CENU:** ubicación y tipo de unidades; CIIU 64xx (servicios financieros) y corresponsales si están clasificados; formalidad (RUT).
- **Complementarios:** puntos de acceso de la SFC/BdO (oficinas, corresponsales, cajeros) por coordenada o municipio ([BdO cobertura](https://www.bancadelasoportunidades.gov.co/sites/default/files/2019-02/Cobertura%20primer%20semestre%202018.pdf)); RIF por municipio.
- **Solución:** distancia de cada unidad de economía popular al punto de acceso más cercano; índice municipal "% de unidades a > 1 km"; mapa de **dónde instalar corresponsales** (maximización de cobertura: elegir *k* tiendas existentes que, convertidas en corresponsales, cubren más unidades — algoritmo greedy de *maximal covering*).
- **Métricas:** % unidades sin acceso a 1 km; unidades cubiertas por corresponsal adicional; ranking municipal.
- **Modelo:** SaaS para redes de corresponsales y bancos (expansión); convenio BdO.
- **Impacto:** acerca crédito formal y desplaza el "gota a gota" (1 de cada 4 micronegocios que pidió crédito acudió a él, según [Forbes 2023](https://forbes.co/2023/03/28/economia-y-finanzas/gobierno-promovera-acceso-al-credito-para-frenar-los-gota-a-gota)).
- **MVP 2h:** si no hay base de puntos de acceso, usar las propias unidades del CENU con CIIU financiero como proxy + greedy de 20 nuevas ubicaciones. **Viable.**
- **Complejidad:** 3/5.

---

### Idea 4 — "Semáforo de Formalización e Inclusión" ⭐ TOP 2

- **Problema:** solo 49,16 % de las unidades tiene RUT; los programas de formalización (Régimen Simple: ~133.000 activos según [Actualícese](https://actualicese.com/contribuyentes-en-el-regimen-simple-de-tributacion/); matrícula mercantil; CREO; FNG) se despliegan sin una priorización territorial basada en el universo real.
- **Usuario:** DNP/CONPES EP, MinCIT, DIAN (área de pedagogía/cultura tributaria), Confecámaras y Cámaras, alcaldías.
- **Datos CENU:** RUT, registro mercantil, contabilidad, emplazamiento, CIIU, PO, antigüedad, sexo.
- **Complementarios:** población; puntos de acceso financiero; presencia de oficinas de Cámara/DIAN (opcional).
- **Solución:** índice compuesto por municipio y por localidad/comuna (§5.4) + **potencial de formalización** (número absoluto) + segmentación de "listos para formalizarse" (≥ 3 años, ≥ 2 PO, fijo, sin RUT) vs "subsistencia" (móvil, 1 PO) → **ruta diferenciada**: a los primeros, Régimen Simple + matrícula + crédito FNG; a los segundos, inclusión financiera básica + protección social, no tributación. Semáforo rojo/amarillo/verde.
- **Métricas:** $F_j$, $PF_j$, % "listos para formalizarse", brecha vs promedio nacional, brecha por sexo.
- **Modelo:** producto público (tablero para DNP/SIEP); servicio de analítica para Cámaras (planear campañas de matrícula); cofinanciación por cooperación internacional.
- **Impacto:** formalizar a quien le conviene (y no forzar a quien es de subsistencia) mejora ingresos y acceso a crédito; aporta a la meta PND de +6 % ingresos de micronegocios EP.
- **Ética/legal:** solo agregados; nunca listas individuales (reserva estadística, [Ley 79/1993](https://www.dane.gov.co/files/noticias/Ley79_1993.pdf)).
- **MVP 2h:** groupby municipio + mapa coroplético + tabla de segmentos + 3 recomendaciones. **Muy viable.**
- **Complejidad:** 2/5.

---

### Idea 5 — "Score de Entorno" (variables territoriales para scoring alternativo de microcrédito)

- **Problema:** los micronegocios no tienen historial crediticio; las fintech y microfinancieras necesitan señales alternativas.
- **Usuario:** microfinancieras, cooperativas, fintech B2B (tipo plataformas para tenderos), FNG (diseño de garantías).
- **Datos CENU:** agregados de entorno por celda: densidad, diversidad (1−HHI), antigüedad mediana, % consolidados, saturación del CIIU, % formalidad.
- **Complementarios:** estrato, criminalidad, flujo peatonal/transporte; idealmente datos de desempeño de cartera del aliado (para entrenar).
- **Solución:** API que, dada una coordenada + CIIU, devuelve un vector de "salud del entorno" y un **puntaje de entorno** (0–100) para complementar el scoring individual. No sustituye datos del deudor; reduce asimetría de información.
- **Métricas:** AUC incremental del modelo del aliado (piloto), cobertura de solicitantes.
- **Modelo:** pago por consulta (API) o licencia anual.
- **Impacto:** más aprobaciones responsables para micronegocios en zonas "sanas" que hoy se rechazan por falta de información.
- **Riesgo:** sesgo territorial (*redlining*) → usar solo como variable positiva/complementaria y auditar equidad.
- **MVP 2h:** función Python `score_entorno(lat, lon, ciiu)` + mapa de puntajes; sin validación con cartera (decirlo). **Viable.**
- **Complejidad:** 3/5.

---

### Idea 6 — "TAT Radar" (potencial y ruteo tienda a tienda)

- **Problema:** distribuidores de consumo masivo (canal con ~37–48 % de las ventas, [Pulzo](https://www.pulzo.com/economia/cuantas-tiendas-barrio-hay-colombia-alentador-dato-sus-duenos-PP5289158A); [El Colombiano](https://www.elcolombiano.com/negocios/dia-del-tendero-en-colombia-NL28890397)) no tienen un universo oficial de tiendas; estimaciones privadas difieren.
- **Usuario:** fabricantes, distribuidores, fintech/B2B de abastecimiento, gremios (Fenalco).
- **Datos CENU:** CIIU 4711/4719/472x, emplazamiento (incluye tiendas en vivienda), PO, coordenadas.
- **Complementarios:** población por manzana, estrato, malla vial.
- **Solución:** (1) conteo oficial de tiendas por municipio y comparación con Nielsen/Fenalco; (2) DBSCAN para "micro-territorios" de visita; (3) zonificación de rutas balanceadas (k-means con restricción de tamaño ≈ n.º de tiendas por vendedor/día) y orden de visita (heurística vecino más cercano / OR-Tools).
- **Métricas:** tiendas/1.000 hab.; tiendas por ruta; km estimados por ruta; cobertura.
- **Modelo:** licencia de datos/servicio a fabricantes y distribuidores; versión gratuita agregada para gremios.
- **Impacto:** abastecimiento más barato al tendero → precios competitivos frente al *hard discount*.
- **MVP 2h:** una ciudad, conteo + DBSCAN + 10 rutas en mapa. **Viable.**
- **Complejidad:** 3/5.

---

### Idea 7 — "Observatorio Territorial de la Economía Popular" (SIEP-ready)

- **Problema:** el CONPES EP y el SIEP (art. 90 Ley 2294) requieren línea base y seguimiento territorial; hoy no hay un tablero único.
- **Usuario:** DNP, DANE, gobernaciones/alcaldías, Consejo Nacional de Economía Popular, academia.
- **Datos CENU:** emplazamiento, PO, formalidad, CIIU, sexo, antigüedad.
- **Complementarios:** EMICRON (ingresos), población, NBI/IPM municipal.
- **Solución:** tablero (Looker Studio/Power BI/Streamlit) con **Índice de Economía Popular** (§5.11), perfil por municipio y tipologías (k-means sobre indicadores) → "municipios de economía popular de calle", "de vivienda", "de comercio fijo informal", etc., cada uno con un paquete de política recomendado.
- **Métricas:** EP_j, tipología, brechas.
- **Modelo:** bien público; financiable por DNP/cooperación (BID, CAF, PNUD).
- **Impacto:** focalización de 54 acciones del CONPES en donde están las unidades.
- **MVP 2h:** índice + clustering de municipios + 1 mapa + 4 perfiles. **Viable.**
- **Complejidad:** 2/5.

---

### Idea 8 — "Ellas Mueven la Economía Popular" (brecha de género territorial) ⭐ TOP 3

- **Problema:** las mujeres son mayoría entre propietarios que respondieron (613.953 vs 576.983, [Forbes](https://forbes.co/forbes-women/las-mujeres-estan-al-frente-de-mas-de-la-mitad-de-los-negocios-urbanos-de-colombia)), pero probablemente con negocios más pequeños, más en vivienda y menos formales (hipótesis a verificar). Los programas no se diseñan con esa radiografía.
- **Usuario:** Consejería/Ministerio de Igualdad, secretarías de la mujer (en Bogotá, SDMujer y Sistema Distrital de Cuidado), FNG/Bancóldex (líneas con enfoque de género), iNNpulsa.
- **Datos CENU:** sexo/edad/educación del propietario, CIIU, emplazamiento, PO, RUT, antigüedad, coordenadas.
- **Complementarios:** Manzanas del Cuidado (27 en Bogotá a 2025, [Alcaldía](https://bogota.gov.co/mi-ciudad/mujer/bogota-fortalecio-su-sistema-distrital-de-cuidado-durante-2025)), oferta de cuidado (CIIU 88xx), población.
- **Solución:** (1) brechas $\Delta F$, $\Delta PO$, antigüedad, Duncan DI por municipio; (2) brecha ajustada (logit); (3) mapa de hot spots (Gi\*) de negocios de mujeres en vivienda **vs** distancia a servicios de cuidado → dónde una Manzana del Cuidado o un jardín tendría mayor efecto en el emprendimiento femenino.
- **Métricas:** M_j, ΔF, ΔPO, DI, % negocios de mujeres a > 1 km de servicio de cuidado.
- **Modelo:** insumo de política pública; producto financiero con enfoque de género (cartera rosa) para bancos.
- **Impacto:** liberar tiempo de cuidado → más horas productivas; crédito para crecer negocios femeninos.
- **MVP 2h:** tabla de brechas nacional + top municipios + 1 mapa Gi\* en una ciudad + recomendación de 3 ubicaciones para servicios de cuidado. **Viable si el módulo sociodemográfico viene en la base.**
- **Complejidad:** 3/5.

---

### Idea 9 — "Cuidado Cerca" (oferta de servicios de cuidado vs demanda)

- **Problema:** la economía del cuidado es a la vez sector económico (guarderías, cuidado de adultos mayores) y barrera para el emprendimiento femenino.
- **Usuario:** Sistema Nacional/Distrital de Cuidado, ICBF, alcaldías, emprendedoras del sector cuidado.
- **Datos CENU:** CIIU 87 y 88 (asistencia social con/sin alojamiento), 8510 (preescolar), ubicación, sexo propietario.
- **Complementarios:** población 0–5 y 60+ por manzana (CNPV), Manzanas del Cuidado.
- **Solución:** 2SFCA de cuidado (§5.7) → zonas de déficit; oportunidades de emprendimiento en cuidado (economía del cuidado como fuente de empleo).
- **Métricas:** cupos estimados/población objetivo (si PO como proxy de capacidad), déficit por manzana.
- **Modelo:** público; microfranquicias sociales de cuidado.
- **Impacto:** empleo femenino + reducción de carga de cuidado.
- **MVP 2h:** mapa de déficit en una ciudad. **Viable** (población por edad requiere CNPV preparado).
- **Complejidad:** 3/5.

---

### Idea 10 — "Calle Ordenada" (gestión inteligente del espacio público y venta en calle)

- **Problema:** 219.042 unidades de venta en calle ([Portafolio](https://www.portafolio.co/economia/crecimiento/uno-de-cada-10-negocios-en-colombia-hace-parte-de-las-ventas-ambulantes-482970)); la política oscila entre desalojo y tolerancia sin datos de dónde y cuántos.
- **Usuario:** IPES (Bogotá) y entidades equivalentes, secretarías de gobierno, alcaldías locales.
- **Datos CENU:** emplazamiento semifijo/móvil, CIIU (alimentos, confección, etc.), coordenadas, sexo, antigüedad.
- **Complementarios:** estaciones de transporte masivo, colegios, hospitales, plazas de mercado, andenes (ancho), POT.
- **Solución:** hot spots (Gi\*) de venta en calle + co-localización con generadores de flujo → propuesta de **Zonas de Aprovechamiento Económico Regulado** (ubicación y tamaño sugerido), priorizando por antigüedad (vendedores con años en el sitio) y por perfil.
- **Métricas:** densidad de puestos por 100 m de corredor, # vendedores reubicables en zonas propuestas.
- **Modelo:** público; concesión de mobiliario/kioscos (ingresos para el distrito).
- **Impacto:** convivencia en espacio público, ingresos estables para vendedores, menos conflicto.
- **MVP 2h:** mapa de hot spots + 5 zonas propuestas. **Viable.**
- **Complejidad:** 2/5.

---

### Idea 11 — "ICA Justo" (brecha fiscal municipal agregada y simplificación tributaria)

- **Problema:** municipios con baja base de ICA no saben cuál es su universo potencial de contribuyentes por sector.
- **Usuario:** secretarías de Hacienda municipales, Federación Colombiana de Municipios.
- **Datos CENU:** agregados por municipio/CIIU de unidades con RUT y tamaño.
- **Complementarios:** número de contribuyentes ICA por municipio/CIIU (de la alcaldía; agregado), tarifas.
- **Solución:** comparación **agregada** universo CENU vs registro ICA → brecha por sector; propuesta de **régimen simplificado/ventanilla única** para sectores con mayor brecha y menor escala (integración con Régimen Simple, que incorpora el ICA consolidado).
- **Métricas:** cobertura ICA = contribuyentes/unidades con RUT por sector.
- **Modelo:** consultoría a municipios.
- **Impacto:** finanzas municipales más sostenibles con un enfoque de facilitación.
- **⚠️ Legal:** **prohibido** cruzar datos individuales del CENU con fines fiscales ([Ley 79/1993 art. 5](https://www.dane.gov.co/files/noticias/Ley79_1993.pdf); Ley 2335/2023 art. 37 según [DANE](https://www.dane.gov.co/files/pqr/Respuesta-20241510152151.pdf)). Solo agregados. Si el jurado percibe "fiscalización", resta puntos.
- **MVP 2h:** difícil sin datos ICA; se puede simular con una sola ciudad que publique datos agregados. **Poco viable en 2h.**
- **Complejidad:** 4/5.

---

### Idea 12 — "Mapa de Vocaciones Productivas" (clústeres y especialización)

- **Problema:** la política de desarrollo productivo/reindustrialización y las Comisiones Regionales de Competitividad necesitan identificar aglomeraciones reales (incluyendo micro y popular).
- **Usuario:** MinCIT, iNNpulsa, Bancóldex, gobernaciones, Cámaras (iniciativas clúster).
- **Datos CENU:** CIIU a 4 dígitos, PO, coordenadas.
- **Complementarios:** comercio exterior por municipio (opcional), matriz insumo-producto DANE.
- **Solución:** LQ por municipio/comuna + DBSCAN/Gi\* por CIIU → "fichas de vocación" (p.ej., confección en X, metalmecánica en Y); recomendación de instrumentos (líneas Bancóldex, programas de encadenamiento).
- **Métricas:** LQ, # unidades y PO en clúster, HHI.
- **Modelo:** público + consultoría a gremios.
- **Impacto:** inversión focalizada en aglomeraciones existentes.
- **MVP 2h:** LQ top-3 por municipio + mapa nacional + 1 clúster urbano. **Muy viable.**
- **Complejidad:** 2/5.

---

### Idea 13 — "Compra Local" (matchmaking proveedor–cliente B2B por proximidad)

- **Problema:** micro y pequeñas empresas compran a intermediarios lejanos; hay proveedores cerca que no se conocen (INEGI ilustra el caso panadería→cafeterías con DENUE).
- **Usuario:** micro/pequeñas empresas, Cámaras de Comercio, compras públicas locales (PAE, mercados campesinos), iNNpulsa (encadenamientos).
- **Datos CENU:** CIIU, PO, coordenadas (sin datos de contacto individuales salvo los públicos de registro).
- **Complementarios:** matriz insumo-producto DANE (relaciones CIIU→CIIU); RUES (contacto público de empresas registradas).
- **Solución:** para cada CIIU comprador, lista de CIIU proveedores (MIP) y densidad de proveedores a ≤ 2 km; "índice de autosuficiencia local de insumos" por localidad.
- **Métricas:** % de insumos con proveedor local disponible.
- **Modelo:** marketplace B2B/servicio de Cámaras.
- **Impacto:** encadenamientos y reducción de costos logísticos.
- **MVP 2h:** 3 cadenas ejemplo (panadería, restaurante, confección) en una ciudad. **Medio.**
- **Complejidad:** 3/5.

---

### Idea 14 — "Negocios en Riesgo" (exposición a amenazas naturales y microseguros)

- **Problema:** inundaciones y remociones afectan a micronegocios sin seguro; no se sabe cuántos están expuestos.
- **Usuario:** UNGRD, alcaldías (gestión del riesgo), aseguradoras (microseguros/paramétricos), Fasecolda.
- **Datos CENU:** ubicación, CIIU, PO, formalidad.
- **Complementarios:** mapas de amenaza del POT/IDEAM/SGC, eventos históricos.
- **Solución:** overlay espacial → # unidades y PO expuestos por nivel de amenaza; producto de microseguro paramétrico sugerido para zonas de amenaza alta.
- **Métricas:** unidades expuestas, PO expuesto, % informal expuesto.
- **Modelo:** B2B para aseguradoras; público para planes de contingencia.
- **Impacto:** resiliencia económica y continuidad de negocio.
- **MVP 2h:** requiere tener el shapefile de amenaza listo; **medio**.
- **Complejidad:** 3/5.

---

### Idea 15 — "Cargue Inteligente" (movilidad y logística urbana)

- **Problema:** zonas de cargue/descargue y rutas de transporte público no consideran la densidad real de actividad económica y empleo.
- **Usuario:** secretarías de movilidad, operadores logísticos, TransMilenio/SITP.
- **Datos CENU:** PO por unidad (generador de viajes de empleo), CIIU (comercio que requiere abastecimiento), coordenadas.
- **Complementarios:** GTFS, malla vial, zonas de cargue existentes.
- **Solución:** mapa de "demanda de cargue" (comercio al por mayor/menor ponderado por PO) vs oferta de bahías; accesibilidad de empleos a paradas (PO a ≤ 500 m de estación).
- **Métricas:** PO por estación, déficit de bahías.
- **Modelo:** consultoría a movilidad/logística.
- **Impacto:** menos congestión y costos logísticos.
- **MVP 2h:** medio (GTFS prep).
- **Complejidad:** 3/5.

---

### Idea 16 — "Destino en Datos" (oferta turística georreferenciada)

- **Problema:** destinos turísticos no conocen su oferta real (incluida la informal: alojamiento en vivienda, comida en calle).
- **Usuario:** MinCIT (Viceministerio de Turismo), FONTUR, alcaldías de destinos, gremios (Cotelco, Acodres).
- **Datos CENU:** CIIU 55, 56, 79, 9xxx recreativo, emplazamiento, formalidad (RNT no está en CENU; usar RUT/registro).
- **Complementarios:** RNT (Registro Nacional de Turismo), flujos turísticos, [boletín CENU Turismo](https://www.dane.gov.co/files/operaciones/CENU/bol-CENU-Turismo-2023.pdf).
- **Solución:** LQ turístico municipal, % informalidad turística, mapa de hot spots; brecha CENU vs RNT (agregada).
- **Métricas:** unidades turísticas/1.000 hab., LQ, % sin registro.
- **Modelo:** público/gremial.
- **Impacto:** formalización y calidad turística.
- **MVP 2h:** muy viable a nivel municipal.
- **Complejidad:** 2/5.

---

### Idea 17 — "Pulso de Antigüedad" (vulnerabilidad empresarial y acompañamiento temprano)

- **Problema:** muchos negocios mueren en los primeros años; los programas de acompañamiento no saben dónde están los negocios jóvenes.
- **Usuario:** CEmprende, SDDE, Cámaras (servicios a nuevos inscritos), microfinancieras.
- **Datos CENU:** tiempo de funcionamiento, CIIU, PO, formalidad, sexo.
- **Complementarios:** cohortes de Confecámaras (empresas formales) para validar.
- **Solución:** "pirámide de antigüedad" por territorio y sector (§5.5), zonas con alta proporción de negocios < 2 años y sectores saturados → focalización de mentoría/crédito de consolidación.
- **Métricas:** J_j, C_j, antigüedad mediana, pseudo-supervivencia (con advertencia).
- **Modelo:** público; datos para microfinancieras.
- **Impacto:** mayor supervivencia de negocios jóvenes.
- **MVP 2h:** muy viable (groupby + gráficos).
- **Complejidad:** 2/5.

---

### Idea 18 — "Ficha Territorial CENU automática" (Plan B garantizado)

- **Problema:** 1.102 alcaldías necesitan un diagnóstico económico rápido para planes de desarrollo, POT y CONPES EP; la mayoría no tiene analistas.
- **Usuario:** alcaldías pequeñas e intermedias, concejos, gobernaciones, Federación de Municipios.
- **Datos CENU:** todas las variables agregadas.
- **Complementarios:** población.
- **Solución:** script que genera un **one-pager por municipio** (HTML/PDF): densidad, top-5 sectores, LQ, HHI, formalidad, género, economía popular, comparación con pares (mismo rango de población) + 3 recomendaciones automáticas por reglas. Opcional: resumen en lenguaje natural con un LLM.
- **Métricas:** todas las de §5.
- **Modelo:** bien público; servicio de actualización para gobernaciones.
- **Impacto:** democratiza el uso del censo.
- **MVP 2h:** **altísima viabilidad**; demostrable con 3 municipios contrastantes.
- **Complejidad:** 1/5.

---

## 7. Matriz impacto vs factibilidad y Top 3

Escala 1–5. **Impacto** = magnitud y alcance del beneficio social/política + alineación con agenda vigente (CONPES EP, PND). **Factibilidad 2h** = probabilidad de demo funcional y convincente en 2 horas con un equipo de 3–5. **Wow** = potencia visual/narrativa para el jurado. Puntaje = 0,4·Impacto + 0,4·Factibilidad + 0,2·Wow.

| # | Idea | Impacto | Factib. 2h | Wow | Complejidad | Puntaje |
|---|---|:-:|:-:|:-:|:-:|:-:|
| 1 | Donde Falta, Emprende | 5 | 5 | 5 | 2 | **5,0** |
| 4 | Semáforo de Formalización e Inclusión | 5 | 5 | 4 | 2 | **4,8** |
| 8 | Ellas Mueven la Economía Popular | 5 | 4 | 5 | 3 | **4,6** |
| 7 | Observatorio Territorial EP | 5 | 4 | 4 | 2 | 4,4 |
| 3 | Desiertos Financieros para Negocios | 5 | 4 | 4 | 3 | 4,4 |
| 18 | Ficha Territorial automática | 4 | 5 | 3 | 1 | 4,2 |
| 12 | Mapa de Vocaciones Productivas | 4 | 5 | 3 | 2 | 4,2 |
| 10 | Calle Ordenada | 4 | 4 | 5 | 2 | 4,2 |
| 6 | TAT Radar | 4 | 4 | 4 | 3 | 4,0 |
| 17 | Pulso de Antigüedad | 3 | 5 | 3 | 2 | 3,8 |
| 2 | Ciudad de 15 Minutos Real | 4 | 3 | 5 | 3 | 3,8 |
| 16 | Destino en Datos | 3 | 5 | 3 | 2 | 3,8 |
| 9 | Cuidado Cerca | 4 | 3 | 4 | 3 | 3,6 |
| 5 | Score de Entorno | 4 | 3 | 4 | 3 | 3,6 |
| 14 | Negocios en Riesgo | 4 | 3 | 4 | 3 | 3,6 |
| 13 | Compra Local | 3 | 3 | 3 | 3 | 3,0 |
| 15 | Cargue Inteligente | 3 | 2 | 3 | 3 | 2,6 |
| 11 | ICA Justo | 3 | 2 | 2 | 4 | 2,4 |

### Cuadrantes (vista rápida)

```
            FACTIBILIDAD EN 2 HORAS  →
            baja (≤3)                         alta (≥4)
IMPACTO  ┌───────────────────────────────┬───────────────────────────────────┐
alto     │ APOSTAR SOLO SI HAY DATOS     │ ★ HACER YA (zona ganadora)        │
(≥4)     │ PREPARADOS:                   │ 1 Donde Falta, Emprende           │
         │ 2 Ciudad 15 min · 5 Score     │ 4 Semáforo Formalización          │
         │ 9 Cuidado Cerca · 14 Riesgo   │ 8 Ellas Mueven la EP              │
         │                               │ 7 Observatorio EP · 3 Desiertos F.│
         │                               │ 12 Vocaciones · 10 Calle Ordenada │
         │                               │ 6 TAT Radar · 18 Ficha (Plan B)   │
─────────┼───────────────────────────────┼───────────────────────────────────┤
medio/   │ EVITAR EN LA DATATÓN          │ "RELLENO" / MÓDULOS DE APOYO      │
bajo     │ 11 ICA Justo · 15 Cargue      │ 17 Pulso de Antigüedad            │
(≤3)     │ 13 Compra Local               │ 16 Destino en Datos               │
         └───────────────────────────────┴───────────────────────────────────┘
```

### Top 3 recomendadas y cómo combinarlas

1. **"Donde Falta, Emprende"** — la más completa para una datatón: usa la **georreferenciación** (el diferencial del CENU), tiene usuario claro (emprendedor + alcaldía), demo visual inmediata (mapa de desiertos), modelo de negocio dual (público gratuito + API B2B estilo DENUE) y conecta con ciudad de 15 minutos/POT.
2. **"Semáforo de Formalización e Inclusión"** — la de **mayor alineación con política pública vigente** (CONPES EP, SIEP, Régimen Simple, CREO/FNG). El dato 49,16 % con RUT es un gancho fuerte; la segmentación "listos para formalizar vs subsistencia" muestra madurez de política (no "formalizar a todos").
3. **"Ellas Mueven la Economía Popular"** — diferenciador narrativo con un dato oficial **nuevo** (más propietarias que propietarios) y conexión con el sistema de cuidado; alto "wow" si se muestra un mapa de hot spots de negocios de mujeres en vivienda vs servicios de cuidado.

**Recomendación estratégica:** construir **una sola plataforma** con nombre propio (p.ej., **"CENU Lab: Oportunidad Territorial"**) cuyo núcleo sea la Idea 1, y con **dos capas** que se activan en la demo: *Formalización* (Idea 4) y *Género* (Idea 8). Así el jurado ve una solución coherente con 3 casos de uso, no tres proyectos a medias. Si el tiempo se acaba, se presenta solo la capa núcleo + 1 capa. **Plan B**: Idea 18 (fichas automáticas) usando el mismo código de indicadores.

---

## 8. Estrategia para el día

### 8.1 Criterios típicos de evaluación (y cómo puntuar alto en cada uno)

Patrones observados en datatones de gobierno y hackatones:
- **La Paz 2025:** identificación del problema con uso riguroso de datos abiertos; coherencia lógica y factibilidad de la propuesta de política; correspondencia entre exposición oral y propuesta escrita ([Guía Datatón La Paz 2025](https://sitservicios.lapaz.bo/dataton2025/pdf/guia_y_lineamientos_basicos_del_concurso.pdf)).
- **Datatón UP (Perú) 2024:** concordancia con la temática e impacto en la comunidad; características técnicas: n.º de variables usadas, uso de datos externos, técnicas de procesamiento ([Bases Datatón 2024](https://dataton.up.edu.pe/uploads/base/Bases-del-concurso-DATATON-2024.pdf)).
- **Concurso de datos abiertos Colombia 2026:** innovación y creatividad; uso estratégico de datos abiertos; rigor analítico; tecnologías emergentes e IA; impacto y escalabilidad ([DPL News](https://dplnews.com/?p=331547)).
- **UN Datathon 2024 (co-organizado con DANE):** bases combinadas, visualizaciones, dashboard y video ([UNSD](https://unstats.un.org/bigdata/events/2024/un-datathon/files/Comunicado%20UN%20Datathon%20WDF_final.pdf)).
- **Rúbricas de hackatón:** ejemplo con 40 % técnica, 30 % idea, 20 % diseño, 10 % "wow" ([Global Travel Hackathon](https://github.com/Global-Travel-Hackathon/Evaluation-Criteria)); recomendación de tener **demo/enlace** porque muchos jurados no son técnicos ([TRON DAO forum](https://forum.trondao.org/t/tron-grand-hackathon-improving-your-devpost-judge-score/9393)); "un proyecto simple que funciona le gana a uno ambicioso que no" ([Reskilll](https://blogs.reskilll.com/what-hackathon-judges-look-for-complete-judging-criteria-breakdown-2026/)).

| Criterio típico | Qué busca el jurado | Cómo ganar el punto |
|---|---|---|
| **Impacto / relevancia** | Problema real, usuario concreto, escala | Nombrar el usuario y la decisión que cambia; cuantificar con el CENU ("X unidades / Y personas en desierto") |
| **Uso de datos** | Aprovechar el CENU a fondo + cruces | Usar **geo + CIIU + formalidad + género**; al menos 1 dato externo (población); explicar limpieza |
| **Rigor analítico** | Indicadores bien definidos, supuestos explícitos | Fórmulas en 1 diapositiva técnica; advertencias (transversal, preliminar, reserva) |
| **Innovación** | Algo que no existía | "Primer mapa oficial de desiertos con economía popular incluida" |
| **Viabilidad / sostenibilidad** | ¿Quién lo opera y paga? | Socio institucional + modelo dual (público + B2B) + costo bajo |
| **Escalabilidad** | ¿Sirve en otros municipios? | Mostrar que el código corre para 1.102 municipios (selector) |
| **Presentación** | Claridad, tiempo, demo | Historia de 1 persona; demo en vivo de 90 s; terminar a tiempo |

**Acción #1 al llegar:** pedir/leer la rúbrica oficial y ajustar el pitch a sus pesos.

### 8.2 Roles (equipo de 4; adaptable)

| Rol | Responsabilidad | Herramientas | Entregable a las 9:30 |
|---|---|---|---|
| **R1 – Líder de producto y pitch** (storyteller) | Problema, usuario, narrativa, diapositivas, control del tiempo, ensayo | Google Slides/Canva, cronómetro | Deck de 7 diapositivas + guion |
| **R2 – Ingeniero/a de datos** | Carga, limpieza, diccionario, joins con población/MGN, tabla maestra | Colab/pandas, DuckDB | `master.parquet` + tabla de indicadores por municipio |
| **R3 – Analista geoespacial** | Indicadores espaciales: desiertos, DBSCAN/Gi\*, mapas | geopandas, h3, scikit-learn, esda, folium/kepler.gl, QGIS | 2–3 mapas exportados (HTML + PNG) |
| **R4 – Visualización / dashboard** | Tablero y gráficos, capturas para el deck, demo | Looker Studio / Power BI / Tableau Public / Streamlit | Tablero publicado (link) + 4 gráficos |

Con 3 personas: R1 asume diapositivas + dashboard ligero; con 5: un R5 "validador/abogado del diablo" que verifica cifras, prepara Q&A y la diapositiva de ética/limitaciones.

### 8.3 Checklist PREVIO al evento (hacer el día anterior)

- [ ] Leer bases, rúbrica, formato de entrega (¿notebook? ¿link? ¿video?) y si el pitch está **dentro** o **después** de las 2 horas.
- [ ] Colab/notebook plantilla con celdas: carga → limpieza → indicadores (§11) → mapas → export. Probar `pip install geopandas h3 esda libpysal folium` (o `pip install -r requirements.txt`; el repo ya trae el MVP de la Idea 1 en `scripts/donde_falta.py` y la ficha automática en `scripts/analisis_rapido.py`).
- [ ] Descargar y dejar en Drive/local: proyecciones de población municipal DANE; MGN municipios y (si se puede) manzanas de la ciudad objetivo; CNPV 2018 por manzana (población); diccionario CIIU Rev. 4 A.C.; puntos de acceso financiero (si existen).
- [ ] Lista de **códigos CIIU** por categoría de servicio esencial (tienda 4711/4721–4729, droguería 4773, ferretería 4752, papelería 4761, panadería 1081/4724, peluquería 9602, restaurante 5611/5613, cuidado 87xx/88xx, preescolar 8510, financieros 64xx/6612).
- [ ] Plantilla de deck (7 diapositivas, §9) con marcadores "[MAPA AQUÍ]" "[DATO AQUÍ]".
- [ ] Plantilla de tablero vacío (Looker Studio conectado a Google Sheets) para pegar resultados.
- [ ] Cifras de contexto verificadas (§1, §3) en una "hoja de datos" con URL.
- [ ] Batería cargada, cargadores, hotspot de respaldo, mapas pre-exportados como PNG por si falla internet.
- [ ] Decidir de antemano ciudad piloto (Bogotá por tamaño o la ciudad sede) y la idea (Top 1 con capas).

### 8.4 Cronograma minuto a minuto (7:50 – 9:50)

> Supuesto: las 2 horas son de construcción y la entrega cierra a las 9:50; el pitch ocurre después. Si el pitch está dentro de la ventana, recortar el bloque de construcción en 10 minutos y adelantar el ensayo.

| Hora | Min | Qué pasa | Quién | Salida/criterio de "listo" |
|---|---|---|---|---|
| **7:50–7:55** | 5 | Leer reto, rúbrica y diccionario de datos. Confirmar formato de entrega. | Todos | Rúbrica anotada en el deck |
| **7:55–8:00** | 5 | Carga del dataset; `shape`, `dtypes`, nulos, valores de emplazamiento/CIIU/RUT/sexo. | R2 (R3 apoya) | Perfil rápido del dataset |
| **8:00–8:07** | 7 | **Decisión Go/No-Go de la idea** (Top 1 + capas) según variables disponibles; ciudad piloto; 1 frase de problema; usuario; métrica norte. *Timebox estricto.* | R1 decide con todos | Frase: "Ayudamos a [usuario] a [decisión] usando [CENU]" |
| **8:07–8:25** | 18 | Limpieza + tabla maestra (CIIU a 2/4 dígitos, categoría de servicio, flags de formalidad, EP). Join con población municipal. | R2 | `master.parquet`, `muni_indicadores.csv` v0 |
| 8:07–8:25 | 18 | Preparar grilla H3/manzanas de la ciudad piloto y población; función de distancia al más cercano (BallTree haversine). | R3 | `celdas.parquet` con población |
| 8:07–8:25 | 18 | Esqueleto del deck: portada, problema, usuario, slide de datos/método; buscar cifra gancho. | R1 | 4 diapositivas en borrador |
| 8:07–8:25 | 18 | Montar tablero vacío; gráficos nacionales con datos v0 (sectores, formalidad por depto). | R4 | Tablero con 2 gráficos |
| **8:25–8:30** | 5 | **Checkpoint 1** (de pie, 5 min): ¿hay datos limpios? ¿qué falta? recortar alcance si es necesario. | Todos | Lista de recortes |
| **8:30–8:55** | 25 | Indicadores núcleo: densidad, LQ, HHI, formalidad, potencial de formalización, índice EP, brecha de género por municipio. | R2 | `muni_indicadores.csv` v1 |
| 8:30–8:55 | 25 | Desiertos por servicio (4 servicios) + ranking de oportunidades; Gi\* o DBSCAN para la capa de género o venta en calle. | R3 | Mapa núcleo (HTML+PNG) + top-10 oportunidades |
| 8:30–8:55 | 25 | Tablero: filtros por municipio/servicio; KPI tiles. | R4 | Tablero navegable |
| 8:30–8:55 | 25 | Diapositivas de solución, modelo de negocio, impacto; redactar guion v1. | R1 | Deck 6/7 |
| **8:55–9:00** | 5 | **Checkpoint 2**: elegir **3 hallazgos** (1 nacional, 1 territorial, 1 de capa) y el "momento wow" del demo. | Todos | 3 hallazgos con cifra exacta |
| **9:00–9:20** | 20 | Pulir: capa 2 (formalización o género) si hay tiempo; si no, robustecer núcleo. Exportar imágenes en alta. | R2, R3 | Mapas finales; tabla final |
| 9:00–9:20 | 20 | Integrar capturas, cifras finales y fuentes en el deck; diapositiva de limitaciones/ética. | R1 + R4 | Deck 7/7 completo |
| **9:20–9:22** | 2 | **Congelar código** ("code freeze"): no más features. | R1 anuncia | — |
| **9:22–9:35** | 13 | **Ensayo 1** cronometrado (5 min) + 3 min de feedback + **Ensayo 2** (5 min). Practicar transición a la demo. | R1 presenta; todos critican | Pitch ≤ 4:50 |
| **9:35–9:42** | 7 | Preparar Q&A (§10): asignar quién responde qué; tarjeta con cifras clave. | R5/R1 | Hoja de respuestas |
| **9:42–9:48** | 6 | **Entrega**: subir notebook (limpio, con README de 10 líneas), link del tablero, PDF del deck. Verificar que los links abren en modo incógnito. | R2 + R4 | Confirmación de envío |
| **9:48–9:50** | 2 | Respirar. Dejar abiertas pestañas de demo (tablero, mapa HTML, PNG de respaldo). | Todos | Todo listo |

**Reglas del día:**
1. **Timebox** sin negociación; si algo no sale en 10 minutos, plan B (PNG estático, número agregado, menos capas).
2. **Una sola fuente de verdad** de cifras: celda final del notebook que imprime los números del pitch.
3. **Nada de modelos complejos** que no se puedan explicar en 1 frase.
4. Cada mapa con **título que dice la conclusión** ("El 23 % de la población de X vive a > 500 m de una droguería"), no "Mapa de droguerías".
5. Guardar cada 15 min; versión del notebook en Drive/GitHub.

### 8.5 Herramientas rápidas (qué usar para qué)

| Necesidad | Rápido y seguro | Alternativa |
|---|---|---|
| Limpieza / indicadores | Python + pandas en **Google Colab**; DuckDB para archivos grandes | Excel/Power Query |
| Geo-análisis | geopandas + scikit-learn (BallTree, DBSCAN) + h3; PySAL `esda` para Moran/Gi\* | **QGIS** (Hot Spot plugin, buffers) |
| Mapas para demo | **kepler.gl** (arrastrar CSV con lat/lon: hexágonos y heatmap en 1 minuto) o folium (HTML) | Tableau Public / Power BI mapa |
| Tablero | **Looker Studio** (Google Sheets) o **Power BI**; Streamlit si hay alguien fuerte en Python | Tableau Public |
| Deck | Google Slides/Canva con plantilla preparada | — |
| Respaldo | PNG de cada mapa y gráfica dentro del deck | — |

---

## 9. Plantilla de pitch de 5 minutos

**Estructura: 7 diapositivas, 5:00 exactos (objetivo 4:45).** La demo es el centro.

| # | Tiempo | Diapositiva | Contenido | Frase guía (ejemplo para Top 1) |
|---|---|---|---|---|
| 1 | 0:00–0:25 (25 s) | **Gancho** | Un dato del CENU + una persona | "María quiere abrir una droguería en su barrio. Hoy decide por intuición. El CENU contó 2.005.613 negocios urbanos, por primera vez en 34 años, y nos dice exactamente dónde falta lo esencial." |
| 2 | 0:25–1:00 (35 s) | **Problema y usuario** | Quién sufre, cuánto, por qué ahora; 2 cifras con fuente | "Solo 49 % de las unidades tiene RUT; la economía popular es invisible para los registros. Alcaldías, CREO y emprendedores deciden sin mapa." |
| 3 | 1:00–1:20 (20 s) | **Solución en una frase** | Nombre + propuesta de valor + 3 capas | "CENU Lab: el mapa de oportunidades territoriales: dónde falta qué negocio, dónde formalizar y a quién llegar primero." |
| 4 | 1:20–2:50 (90 s) | **DEMO en vivo** | Mapa de desiertos → clic en zona → top oportunidades → activar capa formalización/género | "Aquí, en [localidad], 18.000 personas viven a más de 500 m de una droguería [cifra del notebook]; abrir aquí tiene la menor saturación de la ciudad…" |
| 5 | 2:50–3:35 (45 s) | **Hallazgos e impacto** | 3 hallazgos con números; quién decide qué distinto mañana | "1) X % de la población en desierto de servicios; 2) N municipios con potencial de formalización > Y; 3) brecha de formalidad de Z p.p. entre propietarias y propietarios." |
| 6 | 3:35–4:20 (45 s) | **Cómo se sostiene y escala** | Modelo dual (público gratis + API B2B), socio institucional (DNP/SIEP, BdO, Cámaras), costo, escalabilidad a 1.102 municipios, hoja de ruta 30-60-90 | "El código corre para todos los municipios; la versión pública alimenta el SIEP; la API por radio se licencia a franquicias y distribuidores." |
| 7 | 4:20–4:50 (30 s) | **Rigor, ética y cierre** | Supuestos/limitaciones (preliminar, transversal), reserva estadística (solo agregados), **llamado a la acción** | "Trabajamos solo con agregados, respetando la reserva estadística. Pedimos al DANE abrir esta capa en su visor: que María, y 2 millones de negocios, decidan con datos." |
| — | 4:50–5:00 | Margen | — | — |

**Consejos de pitch:**
- 1 idea por diapositiva; ≤ 15 palabras de texto; cifras grandes; fuente pequeña al pie.
- Presentan **máximo 2 personas** (1 narra, 1 maneja la demo) para evitar transiciones lentas.
- La demo debe tener **ruta guionizada** (3 clics) y un **PNG de respaldo** en la diapositiva 4.
- Repetir el nombre del producto 3 veces (inicio, demo, cierre).
- Terminar con **qué se pide** (piloto con una alcaldía, apertura de una capa en el visor, convenio de datos).
- Hablar del **usuario**, no del algoritmo; el algoritmo va en una diapositiva de respaldo (anexo) para Q&A.

**Diapositivas de anexo (no se presentan; se usan en Q&A):** A1 fórmulas de indicadores (§5); A2 diccionario/limpieza; A3 validación (comparación con Nielsen/Fenalco/EMICRON); A4 costos y hoja de ruta; A5 riesgos y mitigación.

---

## 10. Preguntas típicas del jurado y respuestas

| # | Pregunta | Respuesta modelo (adaptar con cifras propias) |
|---|---|---|
| 1 | **¿Por qué el CENU y no RUES/DIAN?** | "Porque los registros solo ven lo formal: el propio CENU muestra que cerca de la mitad de las unidades no tiene RUT ([DANE](https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf)). El CENU es el único universo georreferenciado que incluye vivienda, semifijos y móviles." |
| 2 | **¿Cómo manejan la reserva estadística / privacidad?** | "Trabajamos con agregados por celda/manzana/municipio con umbral mínimo de unidades (p.ej. ≥ 5) y nunca listamos negocios individuales. La ley prohíbe usar datos individuales para fiscalización o decisiones administrativas ([Ley 79/1993](https://www.dane.gov.co/files/noticias/Ley79_1993.pdf); Ley 2335/2023)." |
| 3 | **Los datos son preliminares y de 2024; ¿no quedan desactualizados?** | "Sí, por eso el producto está diseñado para actualizarse con registros administrativos (RUES, RST, puntos de acceso) y con la ruta del SIEP; el censo es el marco de referencia. El próximo censo económico está previsto para 2034, así que este es el mapa base de la década." |
| 4 | **¿Quién paga esto? ¿Cómo se sostiene?** | "Modelo dual: capa pública financiada por convenio (DNP/SIEP, alcaldías, Banca de las Oportunidades) y API B2B por consulta para franquicias, distribuidores TAT y financieras — el mismo patrón de la API DENUE en México ([INEGI](https://en.www.inegi.org.mx/servicios/api_denue.html))." |
| 5 | **¿Cómo validan que un "desierto" es real y no un error de cobertura?** | "Cobertura del censo > 98 % ([Forbes](https://forbes.co/2025/11/24/economia-y-finanzas/piedad-urdinola-directora-del-dane-perfila-la-colombia-urbana-mas-servicios-mas-calle-y-menos-industria)); además exigimos población mínima en la celda y contrastamos con OSM/registros. Es una herramienta de priorización que se valida en campo, no un veredicto." |
| 6 | **¿Por qué 500 m / 1 km?** | "Son parámetros ajustables; usamos estándares de caminabilidad de ciudad de 15 minutos. Mostramos sensibilidad: el ranking de top zonas es estable entre 400 y 800 m [si lo verificaron]." |
| 7 | **¿No están sobresimplificando la informalidad?** | "Precisamente segmentamos: 'listos para formalizarse' vs 'subsistencia'. Para los segundos la ruta es inclusión financiera y protección, no impuestos. Esto sigue la lógica de la economía popular del PND, que no la reduce a informalidad ([DNP](https://colaboracion.dnp.gov.co/CDT/Desarrollo%20Empresarial/Encuentros%20territoriales_Economia%20Popular.pdf))." |
| 8 | **¿Cuál es el impacto medible?** | "KPI norte: % de población en desierto de servicios esenciales y n.º de unidades formalizadas/financiadas en zonas priorizadas. Un piloto con una alcaldía permite medir antes/después con grupo de comparación." |
| 9 | **¿Qué tan escalable es?** | "El notebook corre por municipio con un parámetro; ya lo probamos en [N] municipios. Requiere solo CENU + población, ambos nacionales." |
| 10 | **¿Riesgo de que se use para discriminar territorios (redlining)?** | "El score de entorno solo suma información positiva y se audita por estrato/sexo; la decisión de crédito sigue siendo individual. Para política pública, la priorización favorece a las zonas con déficit." |
| 11 | **¿Qué hicieron en estas 2 horas vs qué es visión?** | "Hecho: limpieza, indicadores para todos los municipios, mapa de desiertos de [ciudad], tablero. Visión: API, actualización con registros, piloto." (Ser explícitos genera confianza.) |
| 12 | **¿Por qué ustedes / por qué ahora?** | "El CONPES de Economía Popular se está implementando 2026–2036 ([ICEF](https://www.icef.com.co/component/k2/item/8483-gobierno-nacional-aprueba-el-conpes-de-economia-popular)) y el SIEP necesita un mapa base. El CENU acaba de publicarse; es el momento de convertirlo en decisiones." |
| 13 | **¿Cómo se compara con Nielsen/Fenalco para tiendas?** | "Nielsen reporta 453.750 tiendas y Fenalco ~450.000 ([Pulzo](https://www.pulzo.com/economia/cuantas-tiendas-barrio-hay-colombia-alentador-dato-sus-duenos-PP5289158A); [Fenalco](https://www.ambitojuridico.com/sites/default/files/2024-08/COMUNICADO-Ventasdelas-2024.pdf)); el CENU da [N] en CIIU 4711 urbano. Las diferencias se explican por definiciones y cobertura rural." |
| 14 | **¿Qué limitaciones tiene su análisis?** | "Censo transversal (no mide mortalidad), resultados preliminares, módulo sociodemográfico con respuesta del 59,4 %, distancias euclidianas (no red vial). Todas están en el anexo y no cambian las conclusiones de priorización." |

---

## 11. Snippets de código listos

> Ajustar nombres de columnas al diccionario real. Son celdas de notebook (Colab/Jupyter); nombres como `rut`, `sexo_prop`, `emplazamiento`, `personal_ocupado` son supuestos.

```python
# --- 0. Setup ---
import pandas as pd, numpy as np
from sklearn.neighbors import BallTree
from sklearn.cluster import DBSCAN

df = pd.read_csv("cenu.csv", dtype={"ciiu": str, "cod_mpio": str})
df["ciiu4"] = df["ciiu"].str.zfill(4).str[:4]
df["ciiu2"] = df["ciiu4"].str[:2]
pob = pd.read_csv("poblacion_mpio.csv", dtype={"cod_mpio": str})  # cod_mpio, pob

# --- 1. Densidad ---
m = df.groupby("cod_mpio").size().rename("E").reset_index().merge(pob, on="cod_mpio")
m["densidad_1000"] = m["E"] / m["pob"] * 1000

# --- 2. LQ por municipio y división CIIU ---
t = df.groupby(["cod_mpio", "ciiu2"]).size().rename("Eij").reset_index()
t["Ej"] = t.groupby("cod_mpio")["Eij"].transform("sum")
Ei = t.groupby("ciiu2")["Eij"].sum(); E = t["Eij"].sum()
t["LQ"] = (t["Eij"] / t["Ej"]) / (t["ciiu2"].map(Ei) / E)
top_lq = t[t["Eij"] >= 30].sort_values("LQ", ascending=False).groupby("cod_mpio").head(3)

# --- 3. HHI y diversificación ---
t["s"] = t["Eij"] / t["Ej"]
hhi = t.groupby("cod_mpio")["s"].apply(lambda s: (s**2).sum()).rename("HHI")
n = t["ciiu2"].nunique()
m = m.merge(hhi, on="cod_mpio")
m["HHI_norm"] = (m["HHI"] - 1/n) / (1 - 1/n)

# --- 4. Formalidad y potencial ---
f = (df[df["rut"].isin([0, 1])].groupby("cod_mpio")["rut"].mean().rename("F_rut"))
m = m.merge(f, on="cod_mpio", how="left")
m["potencial_formalizacion"] = m["E"] * (1 - m["F_rut"])

# --- 5. Brecha de género ---
g = (df[df["sexo_prop"].isin(["M", "H"])]
       .groupby(["cod_mpio", "sexo_prop"])
       .agg(n=("rut", "size"), F=("rut", "mean"), PO=("personal_ocupado", "mean"))
       .unstack())
# Duncan DI por municipio
def duncan(sub):
    c = sub.pivot_table(index="ciiu2", columns="sexo_prop", aggfunc="size", fill_value=0)
    return 0.5 * (c["M"]/c["M"].sum() - c["H"]/c["H"].sum()).abs().sum()
di = df[df["sexo_prop"].isin(["M","H"])].groupby("cod_mpio").apply(duncan).rename("Duncan_DI")

# --- 6. Distancia al servicio más cercano (desiertos) ---
R = 6_371_000
def nearest_dist(origins, targets):
    tree = BallTree(np.radians(targets[["lat","lon"]].values), metric="haversine")
    d, _ = tree.query(np.radians(origins[["lat","lon"]].values), k=1)
    return d[:, 0] * R
servicio = df[df["ciiu4"] == "4773"]                     # droguerías
celdas = pd.read_parquet("celdas.parquet")              # lat, lon, pob (centroides)
celdas["d_drog"] = nearest_dist(celdas, servicio)
celdas["desierto_drog"] = (celdas["d_drog"] > 500) & (celdas["pob"] >= 100)
indice_desierto = celdas.loc[celdas.desierto_drog, "pob"].sum() / celdas["pob"].sum()

# --- 7. DBSCAN (clústeres de venta en calle) ---
calle = df[df["emplazamiento"].isin(["semifijo", "movil"])]
db = DBSCAN(eps=150/R, min_samples=15, metric="haversine",
            algorithm="ball_tree").fit(np.radians(calle[["lat","lon"]]))
calle = calle.assign(cluster=db.labels_)

# --- 8. Getis-Ord Gi* sobre celdas (requiere geopandas, libpysal, esda) ---
# import geopandas as gpd, libpysal, esda
# gdf = gpd.GeoDataFrame(celdas, geometry=gpd.points_from_xy(celdas.lon, celdas.lat), crs=4326).to_crs(9377)
# w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=500, binary=True)
# gi = esda.G_Local(gdf["n_mujeres_vivienda"], w, star=True, permutations=999)
# gdf["Gi_z"], gdf["Gi_p"] = gi.Zs, gi.p_sim
```

**kepler.gl en 1 minuto:** exportar `df[["lat","lon","ciiu2","emplazamiento","sexo_prop"]].to_csv("puntos.csv")` → arrastrar a kepler.gl → capa *Hexbin* coloreada por conteo → filtro por emplazamiento → exportar imagen/HTML. Para Colombia usar CRS **MAGNA-SIRGAS / Origen-Nacional (EPSG:9377)** al calcular distancias en metros con geopandas.

---

## 12. Fuentes

**CENU (DANE) y prensa sobre resultados**
- DANE – resultados preliminares CENU: https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano
- DANE – Comunicado tercera entrega (25-may-2026): https://censoeconomiconacionalurbano.dane.gov.co/images/2026/ComunicadosPrensa/25052026_Comunicado-TerceraEntrega-CensoEconomico.pdf
- DANE – cp Tercera entrega CENU: https://www.dane.gov.co/files/prensa/comunicados/cp-TerceraEntregaCENU.pdf
- DANE – Boletín de prensa resultados (11-nov-2025): https://stg.censoeconomiconacionalurbano.dane.gov.co/images/2025/comunicadosDePrensa/20251111_Boletin-de-Prensa_Resultados-Censo-Economico.pdf
- DANE – Ficha metodológica CENU (v2): https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf
- DANE – Documento metodológico CENU: https://censoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/documento-metodologico-cenu-20251110.pdf
- DANE – Instructivo visor interactivo: https://www.dane.gov.co/files/operaciones/CENU/instructivo_Visor-interactivo.pdf
- DANE – Boletín CENU Turismo: https://www.dane.gov.co/files/operaciones/CENU/bol-CENU-Turismo-2023.pdf
- Valora Analitik – resultados 2026: https://www.valoraanalitik.com/resultados-del-censo-economico-del-dane-2026/
- Valora Analitik – más de dos millones: https://www.valoraanalitik.com/censo-economico-del-dane-identifico-mas-de-dos-millones-de-empresas-y-negocios-en-colombia/
- Forbes Colombia – Urdinola, "más servicios, más calle": https://forbes.co/2025/11/24/economia-y-finanzas/piedad-urdinola-directora-del-dane-perfila-la-colombia-urbana-mas-servicios-mas-calle-y-menos-industria
- Forbes Colombia – comercio y servicios dominan: https://forbes.co/2025/11/11/economia-y-finanzas/comercio-y-servicios-dominan-el-mapa-economico-urbano-de-colombia-segun-el-censo-del-dane
- Forbes Colombia – mujeres al frente de más de la mitad: https://forbes.co/forbes-women/las-mujeres-estan-al-frente-de-mas-de-la-mitad-de-los-negocios-urbanos-de-colombia
- Portafolio – más de dos millones de unidades: https://www.portafolio.co/economia/regiones/en-colombia-hay-mas-de-dos-millones-de-unidades-economicas-segun-el-nuevo-censo-economico-nacional-urbano-del-dane-497881
- Portafolio – uno de cada 10 negocios es venta ambulante: https://www.portafolio.co/economia/crecimiento/uno-de-cada-10-negocios-en-colombia-hace-parte-de-las-ventas-ambulantes-482970
- Portafolio – empresas que apenas están naciendo: https://www.portafolio.co/negocios/empresas/colombia-es-un-pais-de-empresas-que-apenas-estan-naciendo-donde-la-universidad-no-es-regla-para-emprender-498739
- La República – vendedores de calle 11 %: https://www.larepublica.co/economia/los-vendedores-de-calle-son-11-de-los-negocios-urbanos-4268116
- La República – primera medición en 34 años: https://www.larepublica.co/economia/dane-revelara-datos-del-censo-economico-urbano-la-primera-medicion-en-34-anos-4434383
- La República – Urdinola (próximo censo 2034): https://www.larepublica.co/especiales/empresario-del-ano-2025/piedad-urdinola-en-su-intervencion-en-el-empresario-del-ano-lr-4347556
- El Universal – Bolívar registro mercantil y RUT: https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/

**Economía popular, micronegocios y formalización**
- DANE – Nota Estadística Economía Popular 2026: https://www.dane.gov.co/files/investigaciones/notas-estadisticas/nota-EconomiaPopular-2026.pdf
- DANE – Proyecto SIEP: https://www.dane.gov.co/files/proyectos-de-resoluciones-y-decretos/doc-SG-ProyectoSIEP-2023.pdf
- Bloomberg Línea – medición de economía popular: https://www.bloomberglinea.com/latinoamerica/colombia/plan-de-desarrollo-medicion-de-la-economia-popular-que-plantea-petro-ya-existe/
- Bloomberg Línea – avances: https://www.bloomberglinea.com/latinoamerica/colombia/como-va-la-medicion-y-caracterizacion-de-la-economia-popular-gobierno-responde/
- DNP – ruta CONPES EP: https://dnp.gov.co/Prensa_/Noticias/Paginas/dnp-socializa-la-ruta-de-participacion-para-formulacion-conpes-economia-popular.aspx
- DNP – Encuentros territoriales EP: https://colaboracion.dnp.gov.co/CDT/Desarrollo%20Empresarial/Encuentros%20territoriales_Economia%20Popular.pdf
- ICEF – aprobación CONPES EP: https://www.icef.com.co/component/k2/item/8483-gobierno-nacional-aprueba-el-conpes-de-economia-popular
- Confecámaras – economía popular: https://confecamaras.org.co/wp-content/uploads/2024/09/economia-popular-sep-3-1.pdf
- Confecámaras – dinámica de creación de empresas 2025-1: https://confecamaras.org.co/wp-content/uploads/2025/08/2025-1-dinamica-de-creacion-de-empresas.pdf
- DANE – EMICRON 2024: https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2024.pdf
- DANE – EMICRON Vendedores ambulantes 2024: https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRONVendedoresAmbulantes-2024.pdf
- Forbes Colombia – 30 % de micronegocios opera desde vivienda: https://forbes.co/2026/09/29/negocios/el-30-de-los-micronegocios-en-colombia-opera-desde-una-vivienda-dane/
- Alcaldía de Bogotá – micronegocios 2024: https://bogota.gov.co/en/node/269302
- Actualícese – Régimen Simple: https://actualicese.com/contribuyentes-en-el-regimen-simple-de-tributacion/
- Portafolio – empresas activas Bogotá-Región: https://www.portafolio.co/negocios/empresas/la-creacion-de-empresas-aumento-6-en-bogota-y-cundinamarca-hasta-noviembre-segun-la-camara-de-comercio-485224

**Inclusión financiera y crédito**
- Superfinanciera – RIF 2024: https://www.superfinanciera.gov.co/publicaciones/10115642/para-2024-el-963-de-los-colombianos-adultos-tenia-al-menos-un-producto-de-deposito-o-credito/
- Banca de las Oportunidades – RIF 2024 (PDF): https://www.bancadelasoportunidades.gov.co/sites/default/files/2025-06/BDO_RIF%202024_20062025.pdf
- Portafolio – 96,3 % de adultos: https://www.portafolio.co/economia/finanzas/en-2024-el-96-3-de-adultos-tenia-un-producto-financiero-631786
- Portafolio – programa CREO: https://www.portafolio.co/mis-finanzas/creditos/programa-creo-iniciativa-para-combatir-gota-a-gota-ha-desembolsado-mas-de-28-000-millones-de-pesos-601038
- Forbes – crédito contra el gota a gota: https://forbes.co/2023/03/28/economia-y-finanzas/gobierno-promovera-acceso-al-credito-para-frenar-los-gota-a-gota
- La República – FNG $15,1 billones: https://www.larepublica.co/finanzas/el-fondo-nacional-de-garantias-respaldo-15-1-billones-en-creditos-con-corte-a-agosto-4217873
- La República – FNG riesgo microempresarios: https://www.larepublica.co/finanzas/fondo-nacional-de-garantias-asegura-que-perfil-de-riesgo-de-microempresarios-cayo-50-4437280
- BdO – Cobertura 1S-2018: https://www.bancadelasoportunidades.gov.co/sites/default/files/2019-02/Cobertura%20primer%20semestre%202018.pdf
- Pulzo – préstamos SDDE Bogotá: https://www.pulzo.com/economia/prestamos-bogota-intereses-con-secretaria-desarrollo-economico-PP3966348
- Alcaldía de Bogotá – 100.000 micronegocios: https://bogota.gov.co/mi-ciudad/desarrollo-economico/bogota-fortalecio-100000-micronegocios-en-menos-de-cuatro-anos

**Tiendas de barrio / TAT**
- Pulzo – cuántas tiendas de barrio hay: https://www.pulzo.com/economia/cuantas-tiendas-barrio-hay-colombia-alentador-dato-sus-duenos-PP5289158A
- Fenalco (vía Ámbito Jurídico) – comunicado 2024: https://www.ambitojuridico.com/sites/default/files/2024-08/COMUNICADO-Ventasdelas-2024.pdf
- El Colombiano – Día del tendero: https://www.elcolombiano.com/negocios/dia-del-tendero-en-colombia-NL28890397
- Portafolio – ventas tiendas 1S-2024: https://www.portafolio.co/negocios/comercio/cuanto-crecieron-las-ventas-de-las-tiendas-de-barrio-de-colombia-en-el-primer-semestre-de-2024-609827
- Portafolio – 11.000 tiendas en peligro: https://www.portafolio.co/negocios/unas-11-000-tiendas-estan-en-peligro-de-desaparecer-555185
- Portafolio – desplazamiento hacia D1 y Ara: https://www.portafolio.co/negocios/empresas/los-colombianos-han-desplazado-las-tiendas-por-d1-y-ara-501143
- Forbes – Chiper Serie A: https://forbes.co/emprendedores/chiper-levanta-us12-millones-digitalizando-las-tiendas-de-barrio
- Forbes – Chiper Serie B: https://forbes.co/2021/11/18/emprendedores/chiper-buscara-atender-100-000-tiendas-de-barrio-tras-recaudar-us53-millones/
- El Colombiano – cierre Frubana: https://www.elcolombiano.com/negocios/historia-detras-cierre-frubana-y-merqueo-colombia-america-latina-LP29733329

**Género y cuidado**
- iNNpulsa – brechas de género en innovación: https://innpulsacolombia.com/wp-content/uploads/2024/11/BRECHAS-DE-GENERO-EN-LA-INNOVACION.pdf
- iNNpulsa – brechas de género en desempeño: https://innpulsacolombia.com/wp-content/uploads/2024/11/BRECHAS-DE-GENERO-EN-EL-DESEMPENO-EMPRESARIAL.pdf
- Alcaldía de Bogotá – Sistema Distrital de Cuidado 2025: https://bogota.gov.co/mi-ciudad/mujer/bogota-fortalecio-su-sistema-distrital-de-cuidado-durante-2025

**Internacional**
- INEGI – API DENUE: https://en.www.inegi.org.mx/servicios/api_denue.html
- INEGI – Boletín DENUE 2020: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2020/OtrTemEcon/DENUE2020.pdf
- INEGI – Boletín DENUE 2026: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/denue/DENUE2026_05.pdf
- INEGI – Censos Económicos 2024 resultados oportunos: https://inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_RO_Nal.pdf
- SNIEG – avances CE 2024: https://www.snieg.mx/Documentos/Economico/sesiones/doc_22024/3_avances_censos_econ_2024.pdf
- Revista Ingeniería UNAM – CRISP-DM sobre DENUE: https://www.revistaingenieria.unam.mx/numeros/2020/v21n1-08.pdf
- inegiR (R): https://eflores89.r-universe.dev/inegiR/doc/manual.html
- IDC Online – geografía inclusión financiera CNBV: https://idconline.mx/corporativo/2020/01/06/19-de-los-mexicanos-no-tiene-un-banco-cerca
- BBVA Research – cobertura puntos de acceso México: https://www.bbvaresearch.com/publicaciones/mexico-en-2023-2t-99-de-adultos-en-municipios-con-punto-de-acceso-creditocaptacion/
- Gestión (Perú) – V CENEC 2,3 millones de locales: https://gestion.pe/economia/hay-23-millones-de-locales-para-negocio-en-peru-cuantos-se-alquilan-noticia/
- INEI / CEPAL – censos económicos Perú: https://cepal.org/sites/default/files/presentations/inei-censos-economicos-quinto-censo-nacional-peru.pdf
- INEI – V CENEC publicaciones: https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1924/Libro21.pdf

**Ciudad / métodos**
- La Silla Vacía – Bogotá ciudad de 15 minutos: https://www.lasillavacia.com/?p=250624
- Streetsblog – modelo 15 minutos Bogotá: https://sf.streetsblog.org/2024/03/18/want-a-better-15-minute-city-ask-residents-what-they-really-want
- Esri – Hot Spot Analysis (Getis-Ord Gi\*): https://doc.esri.com/en/arcgis-pro/3.7/tool-reference/spatial-statistics/hot-spot-analysis.html
- CEPAL – cociente de localización: https://repositorio.cepal.org/bitstreams/655c13be-c321-4767-80bc-24cd44e97399/download
- Scielo – especialización municipal: https://www.scielo.org.mx/img/revistas/regsoc/v16n31/html/a1an1.html
- CREEBBA – estructura económica local (LQ, HHI): https://creebba.org.ar/iae/iae125/Caracteristicas_estructurales_de_la_economia_local_IAE_125.pdf

**Legal**
- Ley 79 de 1993 (reserva estadística): https://www.dane.gov.co/files/noticias/Ley79_1993.pdf
- DANE – respuesta PQR sobre reserva (Ley 2335/2023): https://www.dane.gov.co/files/pqr/Respuesta-20241510152151.pdf

**Datatones y hackatones**
- Guía Datatón La Paz 2025: https://sitservicios.lapaz.bo/dataton2025/pdf/guia_y_lineamientos_basicos_del_concurso.pdf
- Bases Datatón UP 2024: https://dataton.up.edu.pe/uploads/base/Bases-del-concurso-DATATON-2024.pdf
- DPL News – concurso de datos abiertos Colombia: https://dplnews.com/?p=331547
- UN Datathon 2024: https://unstats.un.org/bigdata/events/2024/un-datathon/files/Comunicado%20UN%20Datathon%20WDF_final.pdf
- Global Travel Hackathon – criterios: https://github.com/Global-Travel-Hackathon/Evaluation-Criteria
- TRON DAO – mejorar puntaje de jurado: https://forum.trondao.org/t/tron-grand-hackathon-improving-your-devpost-judge-score/9393
- Reskilll – qué buscan los jurados: https://blogs.reskilll.com/what-hackathon-judges-look-for-complete-judging-criteria-breakdown-2026/
- Eventflare – criterios de evaluación: https://eventflare.io/journal/crafting-effective-hackathon-judging-criteria-a-step-by-step-guide

---

### Vacíos de información (no inventados; verificar el día de la datatón)
- Desglose oficial reconciliado por **emplazamiento** (fijo/vivienda/semifijo/móvil) del CENU.
- Conteo de **tiendas de barrio** (CIIU 4711) según CENU.
- Distribución por **tiempo de funcionamiento** y **personal ocupado** a nivel nacional.
- Total nacional EMICRON 2024 confirmado en boletín (prensa reporta >5,2 millones).
- Número oficial, presupuesto y fecha del **CONPES de Economía Popular** (fuente secundaria: ICEF).
- Base vigente georreferenciada de **puntos de acceso financiero** (SFC/BdO) en datos abiertos.
- Disponibilidad de **microdatos anonimizados** georreferenciados del CENU fuera del entorno de la datatón.
