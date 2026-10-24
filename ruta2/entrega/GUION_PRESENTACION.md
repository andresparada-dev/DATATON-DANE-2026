# Guion · Ruta 2 · Bogotá D.C. — 4 minutos de exposición + 1 de preguntas

**Antes de empezar:** abran las diapositivas en modo presentación y dejen el dashboard (`dashboard_ruta2_oscuro.html`) en otra pestaña por si el jurado pide verlo. Que hablen **dos personas**: una narra y otra pasa las diapositivas. Los nombres los decide el equipo.

| # | Tiempo | Diapositiva | Qué decir (texto sugerido) | Criterio de la rúbrica |
|---|---|---|---|---|
| 1 | 0:00–0:20 | Portada | “Buenos días. Somos [equipo] y trabajamos la Ruta 2: la economía real de Bogotá. Nuestra pregunta es doble: cómo se distribuye la actividad económica de la ciudad y dónde hay más oportunidades para emprender. Todo sale de la API del Visor Interactivo del CENU 2024, con resultados preliminares.” | Presentación · Validez (preliminar) |
| 2 | 0:20–0:50 | Datos y método | “Usamos el módulo de referencia sectorial 2023, que cubre 1.058.881 unidades en el país; Bogotá tiene 195.755. Tres reglas: porcentajes sobre quienes respondieron, ‘sin información’ como no respuesta y rangos leídos como rangos. Validamos: cada suma de rangos cuadra con el total de la API, y el ingreso del país da 2.421 billones, la misma cifra del DANE. Diez unidades de Bogotá no muestran su CIIU por reserva estadística.” | **Rigor (25 %)** · Validez (20 %) |
| 3 | 0:50–1:15 | Distribución | “Bogotá es una economía de comercio: 57,2 % de las unidades. Solo el comercio al por menor es el 47,2 %, con 92.335 unidades. Y está concentrada: las 10 divisiones más grandes suman el 81,7 %.” | Pertinencia (responde la 1.ª pregunta) |
| 4 | 1:15–1:55 | Top 10 por rangos | “Esta es la gráfica que pide la guía. Rojo es ingreso de 0 a 10 millones; azul, más de 1.000 millones. El comercio al por mayor tiene 36,1 % de unidades sobre 1.000 millones, seis veces el promedio nacional. La reparación de efectos personales tiene 32,2 % en el rango bajo y apenas 0,7 % en el alto.” | Visualización (15 %) |
| 5 | 1:55–2:20 | Cuadro top 10 | “El cuadro de la guía: unidades y porcentaje en rangos bajos y altos de ingreso y de personal. La tipología compara con el promedio nacional: 23,8 % bajo y 6,1 % alto. En reparación, el 98,5 % opera con 1 a 5 personas. Un rango bajo es una señal, no una prueba.” | Rigor · Validez |
| 6 | 2:20–2:55 | Subsistencia vs. escalamiento | “Señal de subsistencia: reparación, servicios personales y comercio al por menor; suman 106.718 unidades, el 54,5 % de la ciudad. Base para escalar: mayoristas, alimentos, almacenamiento, educación, metalmecánica y salud, todas por encima del 6,1 % nacional en ingreso alto. Ahí están las oportunidades para emprender.” | **Pertinencia (20 %)** · Creatividad |
| 7 | 2:55–3:20 | Bogotá frente al país | “Bogotá tiene menos negocios en el rango bajo y más en el alto; su ingreso promedio por unidad es 2,7 veces el nacional. Con el 18,5 % de las unidades genera el 48,8 % de los ingresos del país.” | Creatividad (cruce no obvio) |
| 8 | 3:20–3:45 | Recomendación | “Tres frentes: formalizar sin ahogar, con Régimen Simple, microcrédito y pagos digitales; encadenar a los mayoristas con las 92.335 tiendas; y orientar capital semilla y crédito productivo a las divisiones con techo alto.” | Pertinencia (decisión de política) |
| 9 | 3:45–4:00 | Cierre | “Bogotá tiene la escala; el reto es que llegue a la mitad de sus negocios. Límites: resultados preliminares, un rango bajo es una señal y la API publica por municipio. Todo es reproducible: notebook, Excel con controles y un dashboard que verifica cada cifra contra la API. Gracias.” | Validez · Presentación |

## Minuto de preguntas: respuestas preparadas

| Pregunta probable | Respuesta |
|---|---|
| ¿Por qué 195.745 y no 195.755? | Diez unidades no muestran su CIIU por reserva estadística. El universo es 195.755 y los porcentajes no cambian. |
| ¿Cómo trataron la no respuesta? | Fuera del denominador. La respuesta se reporta aparte: en la división 47, 71,5 % en ingreso y 69,4 % en personal. En personal, el rango “0” es “Sin información reportada”, según el visor. |
| ¿Por qué incluyen 10 y 52 si no están en el top 10? | Son las divisiones 11 y 12 por número de unidades, y después de la 46 tienen el mayor % de ingreso alto. El cuadro de entrega es el top 10. |
| ¿Por qué no analizan por localidad? | La API publica por municipio. Con microdatos o datos por manzana sería el siguiente paso. |
| ¿Cómo saben que las cifras están bien? | Cada suma de rangos cuadra con el total de la API, el ingreso nacional coincide con el publicado por el DANE ($2.421 billones) y el verificador del notebook compara el dashboard contra la API en vivo. |
| ¿Qué significa “Polarizado”? | Que la división tiene a la vez muchos negocios pequeños (≥ 20 % en el rango bajo) y una proporción alta de grandes (> 6,1 %). Es el caso de la confección (14). |
| ¿Por qué no usaron los salarios? | El visor indica que esa variable excluye el formulario PYMG (pequeñas, medianas y grandes empresas); compararla introduciría un sesgo. |
