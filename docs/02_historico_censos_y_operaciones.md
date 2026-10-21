# 02 · Histórico de censos y operaciones estadísticas económicas del DANE (insumo para un Censo Económico urbano)

> Fecha de corte de la investigación: 21-oct-2026.
> **Nota de método (importante):** en este entorno `WebFetch` falló por DNS en todos los dominios (dane.gov.co, microdatos.dane.gov.co, wikipedia, larepublica.co), así que no se pudieron abrir los PDF. Todas las cifras salen de extractos devueltos por el buscador (`WebSearch`) sobre las URL citadas: boletines del DANE, sitios oficiales y prensa económica. Se agotó además el cupo de búsquedas de la sesión (200), por lo que algunos temas quedan como **NO CONFIRMADO**. Antes de usar una cifra en un entregable final, conviene verificarla contra el PDF o el anexo oficial enlazado.
> Convenciones: "(prensa)" indica que la cifra viene de un medio que cita al DANE y no del documento primario. "NO CONFIRMADO" marca lo que no se pudo verificar.

---

## 0. Resumen ejecutivo

| Hito | Año (referencia) | Cobertura | Magnitud principal |
|---|---|---|---|
| Primer Censo Industrial (Contraloría) | 1945 (ref. jun-1944 a jun-1945) | Industria manufacturera, establecimientos con ≥5 ocupados o producción ≥ $6.000 | **7.853 establecimientos** |
| Segundo Censo Industrial | 1953 | Industria | NO CONFIRMADO |
| Primer Censo Nacional de Comercio y Servicios | 1954 | Comercio y servicios | NO CONFIRMADO |
| Censos Económicos (industria, comercio, servicios) | 1970/1971 | Tercer censo industrial y segundo de comercio y servicios | Comercio y servicios 1971: 96.530 minoristas, 7.588 mayoristas, 37.306 de servicios (dato de ficha CENU; alcance por confirmar) |
| **Censo Económico Nacional Multisectorial** | 1990 (campo 1991) | Urbano. Industria, comercio, servicios, construcción y transporte | **1.001.398 unidades económicas**; 967.428 con personal ocupado, que suman **3.932.823 ocupados** |
| Censo General 2005 (módulo de unidades económicas) | 2005 | Inventario (no censo económico) de UE independientes y asociadas a vivienda | Industria: **160.055 establecimientos, 946.701 empleados**. Total nacional NO CONFIRMADO |
| 3er Censo Nacional Agropecuario (CNA) | 2014 | Área rural dispersa | **2.370.099 UPA + 543.064 UPNA = 2.913.163 unidades**; 111,5 M ha |
| CNPV 2018 | 2018 | Población y vivienda; registra "uso de la unidad" | Conteo de unidades económicas NO CONFIRMADO |
| **Censo Económico Nacional Urbano (CENU)** | 2024 (campo sep-2024 a 1er cuatrimestre 2025; ref. ingresos 2023) | Urbano, 1.102 municipios + San Andrés + 18 ANM | **2.005.613 unidades económicas visibles**; comercio 53,1 %; 219.042 de venta en calle; ingresos 2023 ≈ $2.421 billones (prensa) |

El dato más útil para un análisis urbano es que **en 34 años (1990→2024) las unidades económicas urbanas visibles pasaron de ~1,0 M a ~2,0 M**, la industria bajó de 9,5 % a 5,2 % de las unidades (prensa) y Bogotá bajó de ~23 % a 18 % (análisis secundario, NO CONFIRMADO en fuente DANE).

---

## 1. Censos económicos históricos de Colombia

### 1.1 Primer Censo Industrial de Colombia, 1945
- **Ejecutor:** Contraloría General de la República, por medio de la Dirección Nacional de Estadística (antecesora del DANE). La publicación de 1947 tiene varios volúmenes y un resumen general de 545 páginas.
- **Período de referencia:** 1-jun-1944 a 30-jun-1945.
- **Marco:** establecimientos con 5 o más personas ocupadas o con producción anual de al menos $6.000.
- **Resultado:** **7.853 establecimientos** censados.
- **Uso actual:** el Banco de la República lo usa para análisis histórico de producción, empleo y capital (Cuadernos de Historia Económica y Empresarial n.º 39).
- **Fuentes:**
  - DANE, *Metodología general EAM*: https://www.dane.gov.co/files/operaciones/EAM/met-EAM.pdf
  - DANE, *Documento metodológico del Censo Económico* (ago-2021): https://www.dane.gov.co/files/investigaciones/censo-economico/info-metodologica/CE-documento-metodologico-censo-economico.pdf
  - Catálogo AGN: https://biblioteca.archivogeneral.gov.co/pmb/opac_css/index.php?lvl=categ_see&id=8414
  - Google Libros: https://books.google.com.co/books/about/Primer_Censo_Industrial_de_Colombia_1945.html?id=Z07Sr-TYXpYC
  - BanRep CHEE 39: https://www.banrep.gov.co/sites/default/files/publicaciones/archivos/chee_39.pdf
- **Microdatos:** no existen en ANDA.

### 1.2 Segundo Censo Industrial (1953) y Primer Censo Nacional de Comercio y Servicios (1954)
- El DANE se creó en 1953 (Decreto 2666 de 1953, 14-oct-1953, según Wikipedia en inglés, que no se pudo abrir: https://en.wikipedia.org/wiki/National_Administrative_Department_of_Statistics).
- La *Memoria Censos Económicos 1970* del DANE incluye en su índice el "Segundo Censo Industrial 1953", el "Primer Censo Nacional de Comercio y Servicios 1954" y las muestras industriales anuales 1953-1969. Fuente: https://biblioteca.dane.gov.co/biblioteca/books/291/
- **Cifras (número de establecimientos): NO CONFIRMADO.**
- **Aclaración:** la pregunta mencionaba un "Censo Económico Nacional de 1945". En 1945 solo hubo censo **industrial**, no multisectorial. Y el primer censo de comercio fue en **1954**, no en 1953.

### 1.3 Censos Económicos de 1970/1971
- La línea de tiempo del DANE ubica el "Censo de Industria, Comercio y Servicios" en **1970**: https://www.dane.gov.co/files/lineadetiempodane/index.html
- La metodología EAM y la ficha técnica del CENU fechan en **1971** el tercer censo industrial y el segundo de comercio y servicios. Los establecimientos pequeños se trataron con diseño muestral.
- **Cifras:** la ficha técnica del CENU (versión clásica) reporta para el censo de comercio y servicios de 1971 **96.530 establecimientos minoristas, 7.588 mayoristas y 37.306 de servicios**. Del extracto no queda claro si son totales censales o solo el estrato censado exhaustivamente, por lo que se marcan como POR VERIFICAR. Fuente: https://difusioncensoeconomiconacionalurbano.dane.gov.co/images/2025/sobre/documentos/ficha-tecnica_version-clasica.pdf
- **Microdatos:** no existen en ANDA.

### 1.4 Censo Económico Nacional Multisectorial 1990 (campo 1991)
- **Naturaleza:** según el DANE, fue el primer censo económico nacional y multisectorial, levantado en 1991 con año de referencia 1990. Hasta el CENU 2024 fue el referente nacional más reciente.
- **Cobertura:** área urbana de todos los municipios. Sectores: industria, comercio, servicios, construcción y transporte. Excluyó el sector agropecuario y la administración pública. Unidades estadísticas: establecimiento y empresa.
- **Resultados:**
  - **1.001.398 unidades económicas** urbanas.
  - De ellas, **967.428** reportaron personal ocupado, por un total de **3.932.823 personas**.
  - Participación de la industria en las unidades: **9,5 %**, según un análisis de prensa que compara 1990 con 2024.
  - Participación de Bogotá: **23,2 %**, según un análisis del economista Eduardo Freire citado en prensa. **NO CONFIRMADO** en fuente DANE.
- **Fuentes:**
  - Ficha metodológica CENU (FME-001 v1, 21-ago-2024): https://censoeconomiconacionalurbano.dane.gov.co/images/2024/agosto/Ficha-Metodologica_CENU_FME-001_v1_2024_08_21.pdf
  - Documento metodológico preliminar del censo económico (consulta pública, 2019/2021): https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/FASE-III-documento-metodologico-preliminar-censo-economico-2021.pdf
  - Biblioteca DANE, resumen metodológico 1990: https://biblioteca.dane.gov.co/media/libros/LD_9487_1990_EJ_3.PDF
  - Contexto histórico sobre Bogotá en 1990 (IFEA): https://books.openedition.org/ifea/3273?lang=en
- **Microdatos:** no aparecen en ANDA (NO CONFIRMADO). Las publicaciones digitalizadas están en biblioteca.dane.gov.co.

### 1.5 Censo General 2005: módulo de unidades económicas
- **Naturaleza:** el CONPES (finales de 2004) amplió el censo de población a un "Censo General" con temas de población, vivienda, sector económico y agropecuario. El propio DANE aclara que hizo un **inventario de unidades económicas, no un censo económico**. Su fin era ajustar los marcos de las encuestas sectoriales. El módulo tenía unas 15 preguntas y clasificaba con CIIU Rev. 3 A.C.
- **Cobertura:** unidades económicas independientes y unidades asociadas a vivienda (industria, comercio, servicios y actividad agropecuaria asociada al hogar), en zonas urbanas y rurales.
- **Resultados confirmados:**
  - Industria: **160.055 establecimientos manufactureros con 946.701 empleados**. Fuente: https://www.dane.gov.co/files/operaciones/EAM/met-EAM.pdf y https://www.dane.gov.co/files/investigaciones/censo-economico/info-metodologica/CE-documento-metodologico-sector-industria.pdf
  - El módulo encontró **más unidades que las encuestas anuales** (EAM 2006, EAC 2006, EAS 2005-2006) en los tres sectores. La diferencia se concentra en unidades de menos de 10 empleados. Fuente: síntesis DANE, https://www.dane.gov.co/files/censos/sintesis_corregido.pdf, y el informe de 2008, https://www.dane.gov.co/files/censos/informe_final_19_08_08.pdf
  - En 2021 el DANE señaló que ese inventario "no es completo para analizar la dinámica empresarial actual". Fuente: Plan General del Censo Económico, https://www.dane.gov.co/files/investigaciones/censo-economico/documento-conceptual/documentos/censo-economico-plan-general.pdf
  - **Perfiles municipales** (Boletín 13/09/2010), que dan la distribución de establecimientos por sector:
    - Cesar: industria 7,1 %, comercio 51,1 %, servicios 33,1 %, otras 8,7 %. https://www.dane.gov.co/files/censo2005/PERFIL_PDF_CG2005/20000T7T000.PDF
    - El Copey: 9,6 / 51,4 / 34,3 / 4,8 %. https://www.dane.gov.co/files/censo2005/PERFIL_PDF_CG2005/20238T7T000.PDF
    - Gama (Cundinamarca): 0,0 / 58,4 / 37,7 / 3,9 %. https://www.dane.gov.co/files/censo2005/PERFIL_PDF_CG2005/25299T7T000.PDF
    - Barranco de Loba: 4,1 / 67,4 / 11,6 / 16,9 %. https://www.dane.gov.co/files/censo2005/PERFIL_PDF_CG2005/13074T7T000.PDF
- **Total nacional de unidades económicas y su distribución industria/comercio/servicios: NO CONFIRMADO.** Está en la síntesis y en los cuadros nacionales del CG2005.
- **Microdatos:** ANDA, catálogo 421, *Colombia – Censo General 2005*: https://microdatos.dane.gov.co/index.php/catalog/421 (incluye, por ejemplo, la variable E16_CIIURV3: https://microdatos.dane.gov.co/index.php/catalog/421/variable/F10/V469?name=E16_CIIURV3).

### 1.6 3er Censo Nacional Agropecuario (CNA) 2014
- **Campo:** noviembre 2013 a noviembre 2014. Cubre el área rural dispersa.
- **Resultados:**
  - Unidades de producción: **2.913.163**, de las cuales **2.370.099 son UPA** (Unidades de Producción Agropecuaria) y **543.064 son UPNA** (Unidades de Producción No Agropecuaria).
  - Área rural dispersa censada: **111,5 millones de hectáreas**. De ella, 38,6 % es de uso agropecuario y 2,2 % de uso no agropecuario. Otro boletín da 56,9 % de bosques naturales (62,8 M ha) y 38,3 % agropecuario (42,3 M ha).
  - Dentro del área agropecuaria: 19,8 % de uso agrícola (8,4 M ha) y 79,9 % pecuario o pastos (33,8 M ha).
  - Inventario bovino: 21,4 millones de cabezas (cifra preliminar).
  - Productores: unos 2,7 millones, según prensa (Engormix).
- **Interés para un censo urbano:** las 543.064 **UPNA** rurales (industria, comercio y servicios en zona rural dispersa) son el complemento rural natural del CENU.
- **Fuentes:**
  - Boletín 12, UPNA: https://www.dane.gov.co/files/CensoAgropecuario/entrega-definitiva/Boletin-12-UPNA/12-Boletin.pdf
  - Boletín 11: https://www.dane.gov.co/files/CensoAgropecuario/entrega-definitiva/Boletin-11-parques-naturales-nacionales/11-Boletin.pdf
  - Boletín técnico de avance: https://www.dane.gov.co/files/CensoAgropecuario/avanceCNA/Boletin%20tecnico-24Nov.pdf
- **Microdatos:** existen en ANDA (CNA 2014), pero el número de catálogo está NO CONFIRMADO.

### 1.7 Censo Nacional de Población y Vivienda (CNPV) 2018
- **Resultados generales:** 14,2 M hogares particulares y 13,5 M viviendas con personas presentes (3.ª entrega): https://www.dane.gov.co/files/censo2018/informacion-tecnica/cnpv-2018-comunicado-3ra-entrega.pdf
- **Unidades económicas:** el cuestionario de hogares incluye la variable **"Uso de la unidad"** (tema Ubicación). Se cree que distingue vivienda, uso mixto, unidad no residencial y LEA, pero esas categorías y el **número de unidades económicas o mixtas están NO CONFIRMADOS**. El CNPV 2018 no tuvo módulo económico como el de 2005.
- **Microdatos:** ANDA, catálogo 643: https://microdatos.dane.gov.co/catalog/643. Ficha metodológica: https://www.dane.gov.co/files/censo2018/informacion-tecnica/DSO-CNPV-FME-01-v2.pdf
- **Uso en el CENU:** las proyecciones CNPV 2018 sirven para expandir EMICRON y para calcular indicadores por habitante (unidades por cada 1.000 habitantes).

### 1.8 Censo Económico Nacional Urbano (CENU) 2024: la operación vigente
**Diseño y operativo**
- Inicio de campo: **11-sep-2024**. Antes hubo autodiligenciamiento web para grandes y medianas empresas, hasta el 30-sep-2024; se enviaron unos 50.000 correos a empresas, según El Tiempo.
- Personal y cobertura prevista: **más de 8.000 censistas** (el anuncio inicial hablaba de 11.000), con visita a unos **3,5 millones** de establecimientos y vendedores de calle en las zonas urbanas de los **1.102 municipios**.
- Presupuesto 2024: **$302.213 millones**.
- Cierre del operativo: primer cuatrimestre de 2025, según el Informe al Congreso del DANE 2024-2025.
- Preparación: comenzó en 2019, con documento conceptual, consulta pública, marco censal y documentos temáticos (por ejemplo, el de informalidad).
- Fuentes:
  - Comunicado de prensa: https://www.dane.gov.co/files/investigaciones/censo-economico/cp-CENU.pdf
  - Nota DANE de inicio: https://www.dane.gov.co/index.php/en/actualidad-dane/5802-con-el-censo-economico-nacional-urbano-cenu-2024-el-dane-sale-a-las-calles-de-las-zonas-urbanas-de-colombia-a-contar-la-economia-del-pais
  - El Tiempo: https://www.eltiempo.com/economia/sectores/el-censo-economico-empezara-con-el-envio-masivo-de-correos-electronicos-a-alrededor-de-50-000-empresas-3349299
  - Informe al Congreso: https://www.camara.gov.co/wp-content/uploads/2025/11/INF-AL-CONGRESO-DANE-RC-2024-2025.pdf
  - Documento temático de informalidad: https://www.dane.gov.co/files/investigaciones/censo-economico/info-metodologica/CE-documento-metodologico-informalidad.pdf

**Resultados preliminares (varias entregas, 2025-2026)**
- **Total:** **2.005.613 unidades económicas visibles** en zonas urbanas de 1.102 municipios, San Andrés y Providencia y 18 áreas no municipalizadas. La cobertura promedio fue superior al 98,2 %. Algunos medios publican 2.005.622 o 2.005.248. Fuente: https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano
- **Por sector:**
  - Comercio: **53,1 %**, es decir 1.064.505 unidades según El Nuevo Siglo o 1.062.288 según Valora Analitik.
  - Servicios: **32,3 %** (648.375 unidades).
  - Industria: **5,2 %** (105.148 unidades). MinHacienda publica 7,4 % para industria (por verificar).
  - Los tres sectores suman 90,6 %. El 9,4 % restante, unas 187.600 unidades, corresponde a categorías no confirmadas, posiblemente construcción, transporte u otras.
- **Por departamento:**
  - Bogotá: 360.565 (18,0 %).
  - Antioquia: 250.574 (12,5 %).
  - Valle del Cauca: 193.974 (9,7 %).
  - Cundinamarca: 110.694.
  - Santander: 110.548.
  - Atlántico: 83.911.
  - Bolívar: 72.795, o 72.830 en una entrega posterior (7.º lugar).
- **Por ciudad (prensa):** Medellín 118.678 o 118.679; Cali 99.208; Bucaramanga 52.065. Barranquilla está en el top 5, pero su cifra está NO CONFIRMADA.
- **Venta en calle:**
  - **219.042 unidades de venta en calle**, la primera vez que se incluyen.
  - Por departamento: Bogotá 42.097, Antioquia 21.617, Valle 19.326.
  - Por ciudad: Medellín 13.692, Cali 12.213.
  - Unidades semifijas: 43.400, según Portafolio.
- **Ingresos y empleo:**
  - Ingresos 2023: **≈ $2.421 billones**, según Valora Analitik y El Tiempo. Portafolio, citando a la directora, habla de unos $2.400 billones.
  - Puestos de trabajo: **más de 9,5 millones**, según un resumen de prensa de El Tiempo. Cifra NO CONFIRMADA en fuente DANE.
- **Tercera entrega, sociodemográfica (≈ may-2026):**
  - El 59,4 % de las unidades tiene información sobre el propietario (unos 1,19 millones).
  - Propietarias **mujeres: 613.953 (51,6 %)**; propietarios hombres: **576.983 (48,4 %)**. La diferencia es de 36.970 unidades.
- **Cuarta entrega, formalización (≈ 26-may-2026):**
  - Se analizaron 1.547.275 unidades con información válida.
  - **Con RUT: 760.680 (49,16 %)**. Sin RUT: 577.485 (37,32 %). Sin información: 13,51 %. El Tiempo publica 760.327 con RUT (49,2 %).
  - Hay datos de registro mercantil por departamento, por ejemplo para Bolívar (El Universal), pero el total nacional está NO CONFIRMADO.
- **Microdatos:**
  - El sitio de difusión anunciaba los microdatos anonimizados para **mayo-junio de 2026**.
  - Portafolio y BusinessCol (9-jul-2026) hablaban de **finales de julio o inicios de agosto de 2026**, dirigidos a universidades, investigadores y entidades.
  - **A 21-oct-2026 no se pudo confirmar si ya están publicados.**
  - Hay un **Geovisor CENU** en el Geoportal DANE: https://geoportal.dane.gov.co/
  - Sitio de difusión: https://difusioncensoeconomiconacionalurbano.dane.gov.co/
  - Resultados: https://censoeconomiconacionalurbano.dane.gov.co/resultados/
- **Fuentes de prensa:**
  - El Tiempo: https://www.eltiempo.com/economia/sectores/radiografia-de-la-economia-urbana-de-colombia-hay-mas-de-2-millones-de-negocios-y-mas-de-210-000-de-ellos-se-realizan-en-la-calle-3507775
  - El Tiempo: https://www.eltiempo.com/amp/economia/sectores/los-ultimos-datos-del-censo-economico-urbano-del-dane-que-no-se-realizaba-hace-mas-de-34-anos-en-colombia-3570240
  - Portafolio: https://www.portafolio.co/economia/regiones/en-colombia-hay-mas-de-dos-millones-de-unidades-economicas-segun-el-nuevo-censo-economico-nacional-urbano-del-dane-497881
  - Portafolio: https://www.portafolio.co/economia/regiones/ciudades-intermedias-impulsan-el-nuevo-mapa-economico-de-colombia-con-los-servicios-como-protagonistas-499548
  - La República: https://www.larepublica.co/economia/dane-reporto-mas-de-1-1-millones-de-unidades-economicas-con-datos-sociodemograficos-4384649
  - El Universal: https://www.eluniversal.com.co/economica/2026/05/26/censo-economico-del-dane-bolivar-se-rajo-en-registro-mercantil-y-rut/
  - El Universal: https://www.eluniversal.com.co/economica/2025/11/14/estos-son-los-resultados-del-censo-economico-nacional-urbano-en-bolivar/
  - Valora Analitik: https://www.valoraanalitik.com/censo-economico-del-dane-identifico-mas-de-dos-millones-de-empresas-y-negocios-en-colombia/
  - Valora Analitik: https://www.valoraanalitik.com/resultados-del-censo-economico-del-dane-2026/
  - Semana: https://www.semana.com/economia/macroeconomia/articulo/primeros-resultados-del-censo-economico-urbano-del-dane-ranking-de-ciudades-con-mas-negocios-en-colombia/202550/
  - MinHacienda: https://www.enclaveeconomica.gov.co/w/primeros-resultados-del-censo-economico-nacional
  - El Nuevo Siglo: https://www.elnuevosiglo.com.co/economia/bogota-es-la-region-que-concentra-mas-unidades-economicas-en-el-pais
  - BusinessCol: https://www.businesscol.com/dane-revela-mas-de-dos-millones-de-unidades-economicas-urbanas-en-colombia-con-nuevo-censo/

**Comparativo 1990 → 2024 (unidades urbanas)**

| Indicador | 1990 | 2024 (CENU prel.) | Cambio |
|---|---|---|---|
| Unidades económicas urbanas | 1.001.398 | 2.005.613 | ×2,0 (+100,3 %) |
| Ocupados | 3.932.823 | >9,5 M (prensa, NO CONFIRMADO) | ×≈2,4 |
| % industria en unidades | 9,5 % (prensa) | 5,2 % | −4,3 p.p. |
| % Bogotá | 23,2 % (análisis secundario, NO CONFIRMADO) | 18,0 % | −5,2 p.p. |

Advertencia: los dos censos no son plenamente comparables. Difieren en sectores incluidos (1990 incluyó construcción y transporte), en el concepto de "unidad visible" y en el tratamiento de la venta en calle, que se incluye por primera vez en 2024.

---

## 2. Operaciones relacionadas vigentes (2022-2026)

### 2.1 Encuesta de Micronegocios (EMICRON)
- **Definición:** unidad económica con un máximo de 9 personas ocupadas. La encuesta es mixta y modular en dos etapas: la GEIH identifica a los propietarios y luego se les visita.
- **Año 2024, total nacional** (boletín del 30-jul-2025, https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2024.pdf):
  - **5.297.252 micronegocios**, un 2,1 % más que en 2023.
  - **Sin RUT: 77,6 %**. Por zona: cabeceras 70,4 %; centros poblados y rural disperso 94,0 %. Entre 2023 y 2024, los micronegocios con RUT bajaron 4,1 % y los sin RUT subieron 4,1 %.
  - **No registrados en Cámara de Comercio: 89,5 %.**
  - Ventas por actividad: comercio y reparación de vehículos 36,5 % del valor de ventas; agropecuario 14,2 %.
  - Sexo del propietario: mujeres **35,4 %** y hombres 64,6 %. La lectura del extracto fue ambigua, así que se marca POR VERIFICAR.
  - Cobertura: el total "nacional" excluye Amazonas, Arauca, Casanare, Guainía, Guaviare, Putumayo, Vaupés y Vichada.
- **Año 2023:** 5.188.402 propietarios, 64,5 % hombres y 35,5 % mujeres (boletín del 31-may-2024): https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2023.pdf
- **Año 2022** (boletín del 26-abr-2024, https://www.dane.gov.co/files/investigaciones/boletines/ech/micro/bol-micronegocios-2022.pdf):
  - 5.150.956 micronegocios.
  - Por tamaño: 79,3 % ocupa una sola persona, 17,7 % ocupa 2-3 personas y 3,0 % ocupa 4-9 personas.
- **Departamentos 2024** (30-jul-2025, https://www.dane.gov.co/files/operaciones/EMICRON/bol-Departamentos-EMICRON-2024.pdf):
  - **5.262.313 micronegocios** en 24 departamentos y Bogotá.
  - Por departamento: **Antioquia 12,1 %, Bogotá 11,2 %, Valle 8,5 %, Nariño 7,7 %**, Atlántico 5.º (porcentaje NO CONFIRMADO).
  - Por actividad: servicios 43,8 %, comercio 24,1 %, agropecuario 22,2 %, industria 10,0 %.
  - Valor agregado: $87,3 billones (NO CONFIRMADO en el PDF).
- **24 ciudades y áreas metropolitanas, 2025** (IV trimestre 2025, boletín del 13-mar-2026, https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-IVtrim2025.pdf; Valora Analitik):
  - **2.434.942 micronegocios**, con valor agregado de **$51,3 billones** e ingresos nominales de **$106,5 billones**.
  - Propietarios: **hombres 62,5 %, mujeres 37,5 %**.
  - Unidades por ciudad: Bogotá 25,8 %, Medellín AM 17,5 %.
  - Valor agregado por ciudad: Bogotá 31,2 %, Medellín AM 20,5 %, Cali AM 7,9 %, Bucaramanga AM 7,8 %, Barranquilla AM 7,6 %.
  - En 2024, siete ciudades concentraban el 77,5 % de los micronegocios (Bogotá 25,3 %, Medellín 17,5 %).
  - Variación del II trimestre de 2025: número de micronegocios +4,7 %; ingresos −7,8% (Portafolio).
  - Más del 90 % de los micronegocios pertenece a trabajadores por cuenta propia (La República).
- **Boletines temáticos:**
  - Vendedores ambulantes 2024 (28-oct-2025): **507.266 micronegocios**, de los cuales 45,9 % son de comercio, 34,2 % de servicios, 11,6 % de industria y 8,2 % agropecuarios.
  - Construcción 2024 (10-jun-2026): **290.294 micronegocios**, con ventas de $7,8 billones.
  - Panaderías y tiendas de barrio 2023 (10-abr-2025).
- **Microdatos:**
  - EMICRON 2023: https://microdatos.dane.gov.co/index.php/catalog/832
  - EMICRON 2024: https://microdatos.dane.gov.co/index.php/catalog/875
  - EMICRON 2025: https://microdatos.dane.gov.co/index.php/catalog/914
  - datos.gov.co: https://www.datos.gov.co/dataset/Encuesta-de-Micronegocios-EMICRON-2024/7fku-rfe7
- **Economía Popular:** la Nota Estadística n.º 1 de 2026 (experimental) cuenta en promedio **11,8 M ocupados** y unos **4,7 M micronegocios** en la Economía Popular mercantil: https://www.dane.gov.co/files/investigaciones/notas-estadisticas/nota-EconomiaPopular-2026.pdf

> **Lectura cruzada CENU–EMICRON:** el CENU cuenta unos 2,0 M unidades **visibles urbanas**, mientras que EMICRON estima unos 5,3 M micronegocios, rurales incluidos y muchos **dentro de la vivienda o no visibles**. Las dos operaciones son complementarias: la brecha mide la economía "invisible" (en casa, puerta a puerta, rural). Ojo con el sexo del propietario: el CENU da 51,6 % mujeres entre las unidades visibles que respondieron, y EMICRON da 35-37 % mujeres en el total de micronegocios. La diferencia se explica por la población y el método de cada operación.

### 2.2 GEIH: informalidad laboral (definición DANE de ocupación informal)

| Período | Nacional | 13 ciudades AM | 23 ciudades AM | CP y rural disperso | Fuente |
|---|---|---|---|---|---|
| **jun–ago 2026** | **54,8 %** (55,2 % en 2025) | **40,7 %** | **42,0 %** | 83,1 % | bol-GEIHEISS-jun-ago2026 (13-oct-2026) |
| ene–mar 2026 | 55,3 % | – | – | – | bol-GEIHEISS-ene-mar2026 (13-may-2026) |
| enero 2026 | 55,3 % (56,0 %) | 41,0 % (42,1 %) | 42,4 % (43,6 %) | – | pres-GEIH-ene2026 |
| oct–dic 2025 | 55,7 % | 42,3 % | 43,6 % | 83,1 % | bol-GEIHEISS-oct-dic2025 (12-feb-2026) |
| sep–nov 2025 | 55,4 % (55,3 %) | – | – | – | bol-GEIHEISS-sep-nov2025 |
| ene–mar 2025 | – | – | 44,5 % | – | bol-GEIHEISS-ene-mar2025 |

- **Ciudades, jun–ago 2026:**
  - Más altas: Sincelejo 65,4 %, Cúcuta AM 62,4 %, Riohacha 61,6 %.
  - Más bajas: **Bogotá 34,1 %**, Tunja 34,7 %, Manizales AM 35,3 %.
  - Unos 13,2 M ocupados informales (La República).
- **Ciudades, dic 2025–feb 2026:** Sincelejo 68,3 %, Valledupar 63,4 %, Cúcuta 62,8 %; Bogotá 33,8 %, Tunja 35,7 %, Manizales 35,7 %, Medellín AM 38,2 %.
- **Ciudades, jul–sep 2025:** Sincelejo 69,1 %, Montería 66,0 %, Valledupar 65,4 %, Cúcuta 62,8 %; Bogotá 33,0 %, Manizales 36,5 %, Tunja 38,5 %.
- **Por tamaño de empresa, jun–ago 2026:** microempresas **85,1 %**, pequeñas 19,0 %, medianas 5,4 %, grandes 2,5 % (Pymenoticias, citando al DANE).
- Fuentes: https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIHEISS-jun-ago2026.pdf, https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIHEISS-oct-dic2025.pdf, https://www.dane.gov.co/files/operaciones/GEIH/pres-GEIH-ene2026.pdf, https://www.larepublica.co/economia/entre-junio-y-agosto-13-2-millones-de-personas-trabajaron-en-el-mercado-informal-4502039, https://www.businesscol.com/dane-reporta-reduccion-leve-en-informalidad-laboral-durante-junio-agosto-2026/, https://www.pymenoticias.com/post/informalidad-microempresas-dane-boletin-ciudades
- **La serie completa de las 23 ciudades** está en los anexos XLSX de cada boletín GEIHEISS. Aquí no se pudieron descargar.

### 2.3 Encuestas estructurales anuales (año 2024, cifras provisionales)

| Operación | Unidades investigadas | Personal / otros | Publicación | URL |
|---|---|---|---|---|
| EAM 2024 | **6.583 establecimientos** | **730.844 ocupados**: 60,3 % permanentes, 23,5 % temporales directos, 13,4 % por agencias. Mayor peso en confección (8,8 %), otros alimentos (8,4 %) y plástico (8,1 %) | 19-dic-2025 | https://www.dane.gov.co/files/operaciones/EAM/bol-EAM-2024.pdf |
| EAC 2024 | **10.231 empresas** (umbral: ≥10 ocupados o ingresos ≥ $2.520 millones); 19 dominios | El comercio al por mayor tiene el 57,8 % de las ventas | 16-dic-2025 | https://www.dane.gov.co/files/operaciones/EAC/bol-EAC-2024.pdf |
| EAS 2024 | **6.885 empresas** | Anexo departamental, p. ej. alojamiento: Bolívar $1.995 mm y Bogotá $1.849 mm en ingresos | 12-dic-2025 | https://www.dane.gov.co/files/operaciones/EAS/bol-EAS-2024.pdf |

- Producción bruta, valor agregado y totales de ventas e ingresos: **NO CONFIRMADO**, porque no se pudieron abrir los PDF.
- Microdatos EAM en ANDA: https://microdatos.dane.gov.co/index.php/catalog/888

### 2.4 PIB departamental (Cuentas departamentales)
- **2024 provisional** (boletín del 30-may-2025, https://www.dane.gov.co/files/operaciones/PIB/bol-PIBDep-2024pr.pdf):
  - PIB nacional: **$1.706.447 miles de millones** a precios corrientes.
  - Bogotá: $430.151 mm (**25,2 %**).
  - Antioquia: $253.232 mm (**14,8 %**).
  - Valle: $166.349 mm (**9,7 %**).
  - Los tres suman **49,7 %**.
- **2025 preliminar** (boletín del 3-jul-2026, https://www.dane.gov.co/files/operaciones/PIB/bol-PIBDep-2025pr.pdf):
  - Bogotá, Antioquia y Valle suman cerca de la mitad del PIB; con Santander, Cundinamarca y Atlántico, las seis economías llegan al **67,3 %**.
  - Crecimiento real: Bogotá 3,5 %, Risaralda 3,2 %, Antioquia 3,0 %, Tolima 3,0 %, Meta 2,5 %, Santander 2,4 %, Bolívar 2,0 %, Cundinamarca 2,0 %, Chocó 1,5 %.
  - Caídas: Casanare −2,2 %, Arauca −1,9 %, La Guajira −1,6 %, Putumayo −1,3 %, Cesar −1,1 %.
  - Región Pacífica: $252 billones (13,6 %).
  - La lectura del ranking de crecimiento fue confusa en el extracto: POR VERIFICAR.

### 2.5 Directorio Estadístico de Empresas (DEE) y Registro Estadístico de Empresas (REE)
- El DEE incluye empresas activas (nuevas, permanentes y reactivadas), clasificadas con CIIU Rev. 4 A.C. El tamaño se calcula con el Registro Estadístico de Relaciones Laborales (RELAB). Hay publicación "Panorama desde el REE 2022–2024", con boletín, anexos y presentación, desagregada por actividad, tamaño, organización jurídica y sexo del gerente o dueño.
- El geovisor del DEE muestra **solo personas jurídicas**; las personas naturales se excluyen por reserva estadística: https://geoportal.dane.gov.co/geovisores/economia/directorio-estadistico-de-empresas/
- Página oficial: https://www.dane.gov.co/index.php/servicios-al-ciudadano/servicios-informacion/registro-estadistico-de-empresas/directorio-estadistico-de-empresas
- Ficha DEE: https://bibliotecadoctecnica.dane.gov.co/static/documentos/DIG/DEE/DEE_Ficha%20metodol%C3%B3gica.pdf
- Nota de demografía empresarial (jun-2022): https://www.dane.gov.co/files/investigaciones/notas-estadisticas/jun_2022_nota_estadistica_demografia_empresarial.pdf
- **Número total de empresas del DEE/REE por tamaño, sector y departamento (2022-2024): NO CONFIRMADO.** Hay que tomarlo de los anexos del Panorama REE.

### 2.6 RUES / Confecámaras y cámaras locales
- **Creación de empresas, Colombia:**
  - **2024: 297.475 empresas** (−2,8 % frente a 305.997 en 2023), de las cuales 214.953 son personas naturales y 82.522 sociedades. Informe del 30-ene-2025: https://confecamaras.org.co/wp-content/uploads/2025/01/dinamica-creacion-empresas-colombia-2025.pdf
  - Empresas activas 2024: **1.739.405** (+0,3 %), según la Revista C-Level citando a Confecámaras. POR VERIFICAR en el PDF: https://revistaclevel.com/creacion-de-empresas-en-colombia-disminuyo-28-en-2024
  - **I semestre 2025: 173.907 empresas** (+1,9 % frente a 170.741), de las cuales 129.048 son personas naturales (74 %) y 44.859 sociedades. Las pequeñas cayeron 12,6 %, las medianas 15 % y las grandes 62,5 %. Comercio creció 3,3 % y construcción cayó 8,2 %. Fuente: https://confecamaras.org.co/wp-content/uploads/2025/08/dinamica-de-creacion-de-empresas-en-colombia-op2-web.pdf
  - **Año completo 2025: NO CONFIRMADO**, porque no apareció el informe.
- **Bogotá-Región (CCB):**
  - Creación ene–nov 2025: 81.372 empresas (+6 %): https://www.portafolio.co/negocios/empresas/la-creacion-de-empresas-aumento-6-en-bogota-y-cundinamarca-hasta-noviembre-segun-la-camara-de-comercio-485224
  - Empresas activas: 496.686 (ene–nov 2025) o 493.825 al cierre de 2025, con 87,5 % ubicadas en Bogotá: https://www.ccb.org.co/es/informacion-especializada/observatorio/dinamica-empresarial
  - El 52 % de las activas está en 5 localidades del norte y occidente de la ciudad.
- **Medellín:**
  - Empresas activas en la ciudad, cierre 2024: 118.441 (+3,5 %): https://www.medellin.gov.co/es/sala-de-prensa/noticias/medellin-aumento-su-tejido-empresarial-en-3-5-durante-2024/
  - Jurisdicción CCMA 2025: 164.416 unidades productivas (98 % pymes).
- **Censos locales de comercio o informales** (por ejemplo, censos de vendedores informales del IPES o de la SDDE de Bogotá): **NO CONFIRMADO**, porque se agotó el cupo de búsquedas. Como referencia local hay una nota de la SDDE sobre micronegocios en Bogotá (EMICRON): https://observatorio.desarrolloeconomico.gov.co/wp-content/uploads/2025/02/ne_emicron_vfinal-CARACTERIZACION-MICRONEGOCIOS.pdf

### 2.7 Medición de la economía informal / Cuenta satélite
- **Colombia:** no se encontró una cuenta satélite de economía informal del DANE con valor agregado informal como porcentaje del PIB. **NO CONFIRMADO / posiblemente inexistente.** El DANE sí publica la Cuenta Satélite de Economía del Cuidado, la de economía digital (industrias digitales: 3,6 % del PIB en 2023) y la Nota de Economía Popular. El documento temático de informalidad del CENU es la base conceptual más cercana.
- **Referentes:**
  - México (INEGI, MEI 2024): economía informal **25,4 % del PIB en 2024** (24,7 % en 2023). https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/pibmed/MEI2024_CP.pdf
  - Perú (INEI, CSEI 2022-2024): sector informal **19,0 % del PIB en 2024**. En 2021 fue 17,6 %, con 7,815 M unidades productivas informales. https://www.gob.pe/institucion/inei/informes-publicaciones/7564428-produccion-y-empleo-informal-en-el-peru-cuenta-satelite-de-la-economia-informal-2022-2024

---

## 3. Comparativa internacional (productos de datos abiertos inspiradores)

| País | Operación | Cifra clave | Producto abierto destacable |
|---|---|---|---|
| **México (INEGI)** | Censos Económicos 2019 y 2024 (quinquenales) | CE2019: **6.373.169 establecimientos, 36.038.272 ocupados**. CE2024 (resultados oportunos, 23-ene-2025): **~7 M establecimientos, ~37 M ocupados; 95,5 % micro, con el 41,5 % del empleo**. CDMX 2024: 453.823 establecimientos y 4.163.511 ocupados. Definitivos por estado: 24-jul-2025 | **DENUE**, un directorio georreferenciado abierto que se actualiza con el censo: 24.ª edición con **6.097.675 unidades** (datos a mar-2025). **API DENUE** con token: método *Buscar* por palabra clave ("todos"), coordenadas y radio en metros. Hay descarga masiva y un paquete R `inegiR::inegi_denue()` (radio por defecto 250 m) |
| **Perú (INEI)** | IV CENEC 2008 (ref. 2007) y V CENEC 2022 (fase 1, establecimientos: abr–nov 2022; fase 2, encuesta a grandes, medianas y pequeñas: jun–dic 2022) | IV CENEC: ~1 M establecimientos (cifra exacta NO CONFIRMADA). Lima Metropolitana: **342.374 (2008) → 624.027 (2022), +82,3 %**. V CENEC: meta de ~2 M establecimientos | Reportes departamentales del V CENEC; directorio basado en el RUC de SUNAT; cuenta satélite de la economía informal |
| **Ecuador (INEC)** | Censo Nacional Económico 2010 (el anterior es de 1980 y solo cubrió unidades con 10 o más empleados) | **511.130 establecimientos** (INEC, presentación UNSD 2015). La cifra de 500.217 citada en la pregunta no se confirmó | Microdatos en **ANDA INEC** (IHSN 5921); **Registro Estadístico de Empresas (REEM)** anual, 2024 publicado en oct-2025 |
| **Chile (INE / SII / BCCh)** | Sin censo económico reciente. Censos de industria y comercio desde 1928; censo industrial anual con 10 o más trabajadores | Las firmas en registros tributarios del SII pasaron de ~939 mil a ~1,5 M en 15 años (DF) | **Banco Central: Demografía de Empresas** con desglose regional y base descargable completa (datos SII); estadísticas de empresas por tramo de ventas en UF del SII |
| **Brasil (IBGE)** | Sin censo económico. **CEMPRE**: registro central de empresas basado en registros administrativos | 2023 (publicado 13-nov-2025): **~10 M empresas y organizaciones formales activas** (+6,3 %), **66 M ocupados** (52,6 M asalariados). El 70,2 % no tiene asalariados; 93,1 % tiene 0-9 personas; comercio, 28,3 % de las empresas. Excluye a los MEI | Tablas SIDRA, publicación anual por municipio |

Fuentes:
- México:
  - https://inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_RO_Nal.pdf
  - https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_RO_CDMX.pdf
  - https://www.inegi.org.mx/app/mapa/denue/
  - https://www.inegi.org.mx/servicios/api_denue.html
  - https://rdocumentation.org/packages/inegiR/versions/3.0.0/topics/inegi_denue
  - https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_Def_NL.pdf
- Perú:
  - https://gestion.pe/economia/que-zonas-de-lima-y-provincias-concentran-mas-locales-para-negocio-quienes-los-lideran-noticia/
  - https://cepal.org/sites/default/files/presentations/inei-censos-economicos-quinto-censo-nacional-peru.pdf
  - https://infomercado.pe/inei-censara-a-2-millones-de-establecimientos-economicos-entre-abril-y-noviembre/
- Ecuador:
  - https://unstats.un.org/unsd/trade/events/2015/aguascalientes/3.-Panel%20I%20-%20Presentation%201%20-%20INEC%20Ecuador.pdf
  - https://datacatalog.ihsn.org/catalog/5921
  - https://www.ecuadorencifras.gob.ec/documentos/web-inec/Estadisticas_Economicas/Registro_Empresas_Establecimientos/2024/Semestre_II/Principales_Resultados_REEM_2024.pdf
- Chile:
  - https://www.bcentral.cl/contenido/-/detalle/lanzamiento-dae
  - https://www.df.cl/economia-y-politica/df-tax/ecos-de-la-operacion-renta-sube-cantidad-de-empresas-y-ventas-pero-por
  - https://unstats.un.org/Unsd/economic_stat/Economic_Census/PDF/Chile.pdf
- Brasil:
  - https://agenciadenoticias.ibge.gov.br/pt/agencia-noticias/45117-empresas-contrataram-mais-e-registraram-ganho-real-do-salario-medio-em-2023.html
  - https://mercadoeconsumo.com.br/13/11/2025/economia/brasil-tinha-10-milhoes-de-empresas-e-organizacoes-formais-ativas-em-2023/

**Ideas de producto inspiradas en lo anterior (para el CENU/Datatón):**
1. **"DENUE colombiano"**: un directorio abierto y georreferenciado de unidades económicas urbanas con API (búsqueda por radio, CIIU y municipio), derivado del CENU y de su marco. Las unidades de personas naturales tendrían que anonimizarse o agregarse por manzana o hexágono para respetar la reserva estadística (Ley 2335 de 2023).
2. **Densidad económica por 1.000 habitantes**, cruzando el CENU con las proyecciones del CNPV 2018.
3. **Índice de formalización territorial** que combine el % con RUT del CENU, el % de registro mercantil, la informalidad laboral GEIH por ciudad y el % sin RUT de EMICRON.
4. **Brecha visible vs. invisible**: contrastar el CENU (≈2,0 M visibles urbanas) con EMICRON (≈5,3 M micronegocios) por departamento.
5. **Dinámica 1990→2024**: cambio de estructura sectorial y desconcentración territorial (participación de Bogotá y ascenso de ciudades intermedias).

---

## 4. Tablas de cifras clave (también en `data/cifras_oficiales/historico_y_operaciones_relacionadas.csv`)

### 4.1 Unidades económicas: totales y por sector

| Indicador | Valor | Año | Unidad | Fuente |
|---|---|---|---|---|
| Establecimientos industriales (1er Censo Industrial) | 7.853 | 1945 | establecimientos | https://www.dane.gov.co/files/operaciones/EAM/met-EAM.pdf |
| Unidades económicas urbanas (CE 1990) | 1.001.398 | 1990 | UE | https://censoeconomiconacionalurbano.dane.gov.co/images/2024/agosto/Ficha-Metodologica_CENU_FME-001_v1_2024_08_21.pdf |
| Personal ocupado (CE 1990) | 3.932.823 | 1990 | personas | ídem |
| Establecimientos industriales (CG 2005) | 160.055 | 2005 | establecimientos | https://www.dane.gov.co/files/operaciones/EAM/met-EAM.pdf |
| Empleados industria (CG 2005) | 946.701 | 2005 | personas | ídem |
| UPA (CNA 2014) | 2.370.099 | 2014 | UPA | https://www.dane.gov.co/files/CensoAgropecuario/entrega-definitiva/Boletin-12-UPNA/12-Boletin.pdf |
| UPNA (CNA 2014) | 543.064 | 2014 | UPNA | ídem |
| Unidades económicas urbanas visibles (CENU) | 2.005.613 | 2024 | UE | https://www.dane.gov.co/index.php/actualidad-dane/5878-el-dane-presento-los-resultados-preliminares-del-censo-economico-nacional-urbano |
| CENU comercio | 53,1 % (1.064.505) | 2024 | % / UE | ídem; El Nuevo Siglo |
| CENU servicios | 32,3 % (648.375) | 2024 | % / UE | ídem |
| CENU industria | 5,2 % (105.148) | 2024 | % / UE | ídem |
| CENU venta en calle | 219.042 | 2024 | UE | El Tiempo |
| CENU ingresos | ≈2.421 | 2023 | billones COP | Valora Analitik (prensa) |

### 4.2 CENU por departamento y ciudad (preliminar)

| Territorio | UE | % nacional | Venta en calle |
|---|---|---|---|
| Bogotá D.C. | 360.565 | 18,0 % | 42.097 |
| Antioquia | 250.574 | 12,5 % | 21.617 |
| Valle del Cauca | 193.974 | 9,7 % | 19.326 |
| Cundinamarca | 110.694 | ≈5,5 % (calculado) | NO CONFIRMADO |
| Santander | 110.548 | ≈5,5 % (calculado) | NO CONFIRMADO |
| Atlántico | 83.911 | ≈4,2 % (calculado) | NO CONFIRMADO |
| Bolívar | 72.795 / 72.830 | ≈3,6 % (calculado) | NO CONFIRMADO |
| Medellín (ciudad) | 118.678 | – | 13.692 |
| Cali (ciudad) | 99.208 | – | 12.213 |
| Bucaramanga (ciudad) | 52.065 | – | NO CONFIRMADO |

### 4.3 Micronegocios (EMICRON)

| Indicador | Valor | Año | Cobertura |
|---|---|---|---|
| Micronegocios | 5.297.252 | 2024 | Nacional (24 deptos + Bogotá, según el boletín) |
| Micronegocios | 5.188.402 | 2023 | Nacional |
| Micronegocios | 5.150.956 | 2022 | Nacional |
| % sin RUT | 77,6 % | 2024 | Nacional |
| % sin RUT, cabeceras | 70,4 % | 2024 | Cabeceras |
| % sin RUT, CP y rural disperso | 94,0 % | 2024 | CP-RD |
| % sin registro en Cámara de Comercio | 89,5 % | 2024 | Nacional |
| % propietarias mujeres | 35,5 % | 2023 | Nacional |
| % propietarias mujeres | 37,5 % | 2025 | 24 ciudades AM |
| Micronegocios | 2.434.942 | 2025 | 24 ciudades AM |
| Valor agregado | $51,3 billones | 2025 | 24 ciudades AM |
| Ingresos | $106,5 billones | 2025 | 24 ciudades AM |
| Vendedores ambulantes | 507.266 | 2024 | Nacional |
| Antioquia / Bogotá / Valle / Nariño (% micronegocios) | 12,1 / 11,2 / 8,5 / 7,7 % | 2024 | Departamentos |
| Bogotá / Medellín AM (% micronegocios) | 25,8 / 17,5 % | 2025 | 24 ciudades AM |

### 4.4 Informalidad laboral (GEIH), jun–ago 2026

| Dominio | % ocupados informales |
|---|---|
| Total nacional | 54,8 |
| 13 ciudades AM | 40,7 |
| 23 ciudades AM | 42,0 |
| CP y rural disperso | 83,1 |
| Sincelejo | 65,4 |
| Cúcuta AM | 62,4 |
| Riohacha | 61,6 |
| Bogotá D.C. | 34,1 |
| Tunja | 34,7 |
| Manizales AM | 35,3 |
| Microempresas (≤10) | 85,1 |
| Grandes empresas | 2,5 |

### 4.5 PIB departamental 2024 provisional (precios corrientes)

| Departamento | PIB (miles de millones COP) | % |
|---|---|---|
| Nacional | 1.706.447 | 100 |
| Bogotá D.C. | 430.151 | 25,2 |
| Antioquia | 253.232 | 14,8 |
| Valle del Cauca | 166.349 | 9,7 |

---

## 5. Pendientes / NO CONFIRMADO (para una segunda ronda)
1. Total nacional de UE del Censo General 2005 y su distribución por sector (síntesis DANE, `sintesis_corregido.pdf`).
2. Número de establecimientos de los censos de 1953, 1954 y 1970/71, y alcance exacto de las cifras de 1971.
3. Bogotá: 23,2 % en 1990 (verificar en los cuadros del CE 1990).
4. Totales DEE/REE 2022-2024 por tamaño, sector y departamento (anexos del Panorama REE).
5. Confecámaras, año completo 2025.
6. Publicación efectiva de los microdatos del CENU en ANDA (catálogo y fecha).
7. CENU: personal ocupado total (>9,5 M según prensa), registro mercantil nacional, distribución por tamaño y composición del 9,4 % "otros".
8. EAM, EAC y EAS 2024: producción bruta, valor agregado e ingresos totales.
9. Censos locales de vendedores informales (IPES Bogotá, Medellín).
10. CNPV 2018: conteo de unidades de uso mixto o no residencial.
