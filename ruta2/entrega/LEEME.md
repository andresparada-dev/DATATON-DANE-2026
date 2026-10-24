# Entrega · DataJam CENU 2026 · Ruta 2 · Bogotá D.C.

| Archivo | Qué es |
|---|---|
| `Ruta2_Bogota_CENU.ipynb` | **Notebook de entrega** (Google Colab o Jupyter). Autónomo: consulta la API, aplica las reglas, genera el cuadro top 10, las gráficas, el Excel y la respuesta a la pregunta reto. Ejecutar con *Entorno de ejecución → Ejecutar todas*. |
| `dashboard/dashboard_ruta2_oscuro.html` | Dashboard interactivo (diseño oscuro). Un solo archivo: abre sin internet. |
| `dashboard/dashboard_ruta2_claro.html` | La misma información en diseño claro. |
| `ruta2_bogota_cifras_verificadas.xlsx` | Excel con cuadro top 10, Bogotá vs. nacional, rangos, controles y fuentes. |
| `GUION_PRESENTACION.md` | Guion de 4 minutos y respuestas para el minuto de preguntas. |
| `agente_voz/asistente_voz_cenu.html` | Página del asistente de voz (ElevenLabs): voz, chat de texto, preguntas sugeridas y tabla de datos. Necesita internet y permiso de micrófono. |
| `agente_voz/` (prompt, base de conocimiento, LEEME) | Textos corregidos para configurar el agente en ElevenLabs. |

**Salidas del notebook:** `ruta2_resultados.xlsx` (hojas `cuadro_top`, `rangos_detalle`, `divisiones`, `por_sector`, `bogota_vs_nacional`, `controles`), `ruta2_barras_apiladas.png`, `ruta2_cuadrantes.png`, `dashboard_data.js` y `ruta2_respuestas_api.json`.

**Fuente:** DANE, Censo Económico Nacional Urbano (CENU) 2024, API del Visor Interactivo (`/api/v1/structural/general`), módulo `sectoral_reference_2023`. Resultados preliminares.
