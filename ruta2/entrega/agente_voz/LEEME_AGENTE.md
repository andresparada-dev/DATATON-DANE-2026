# Agente de voz ElevenLabs · Ruta 2 · Bogotá

## 1. Corregir el agente (obligatorio)
El prompt actual del agente tiene las cifras de ingreso de la versión con error (por ejemplo, 46 = 19,6 % alto; el dato correcto es 36,1 %).

1. En ElevenLabs → **Agents → Ruta CENU AI → Agent → System prompt**: reemplaza todo el texto por el contenido de `prompt_agente.txt`.
2. **First message:**
   `[warmly] ¡Hola! Soy el asistente de voz del Grupo 07 para la DataJam CENU 2026. Te ayudo a entender los resultados preliminares del Censo Económico Nacional Urbano para Bogotá, año de referencia 2023. ¿Qué te gustaría saber?`
3. **Knowledge Base:** elimina el TXT actual ("Cenu ruta2 bogota base conocimiento") y sube `base_conocimiento_ruta2_bogota.txt`.
4. **Publish** (guardar y publicar la versión).

## 2. Integración en el dashboard
Los dos dashboards ya traen el widget antes de `</body>`:

```html
<elevenlabs-convai agent-id="agent_5901m5q8fk19fzbsy4zh3d8ngcx4"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

- El widget necesita **internet**; el resto del dashboard funciona sin conexión.
- **Micrófono:** el navegador pide permiso la primera vez. Funciona en `https://` o al abrir el archivo local en Chrome o Edge.
- **Google Sites:** el código incrustado corre dentro de un iframe que puede bloquear el micrófono. Si la voz no arranca, el chat de texto del widget sigue funcionando. Para usar la voz en la exposición, abre el `.html` directamente en el navegador.
- **Colores:** para que el widget combine con el diseño oscuro, en ElevenLabs → **Widget** usa fondo `#1e293b`, texto `#f1f5f9`, botón `#2563eb` y borde `#334155`.

## 3. Preguntas de prueba (antes de exponer)
- “¿Cuántas unidades económicas tiene Bogotá?” → 195.755 (195.745 con CIIU visible).
- “¿Qué porcentaje del comercio al por mayor tiene ingresos de más de mil millones?” → 36,1 %.
- “¿Dónde hay señal de subsistencia?” → 95, 96 y 47; suman 106.718 unidades (54,5 %).
- “¿Cuántos negocios hay en Kennedy?” → debe decir que no tiene datos por localidad.
