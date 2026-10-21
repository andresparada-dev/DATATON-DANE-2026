# 06 · Guía rápida del día: sábado 24 de octubre de 2026

**Lugar:** Universidad de La Salle, sede Chapinero, Auditorio Cincuentenario.
**Agenda:** registro 7:30 · reto 7:50–9:50 · refrigerio 9:50–10:00 · pitch de 5 minutos por equipo 10:00–11:30 · premiación 11:30–12:00.
**Detalle completo:** [05_ideas_negocio_y_estrategia.md](05_ideas_negocio_y_estrategia.md) (cronograma minuto a minuto, roles, 14 preguntas del jurado).

---

## 0. Antes de salir (viernes en la noche)

- [ ] Clonar el repo en el celular o en un USB, o tener a mano el enlace de GitHub. Los computadores de la sala pueden no tener Python, así que el plan es **Google Colab**.
- [ ] Probar en Colab: abrir `notebooks/00_quickstart_cenu.ipynb` → *Runtime → Run all* (usa datos sintéticos).
- [ ] Ensayar `python scripts/donde_falta.py --sintetico` y abrir el HTML.
- [ ] Con internet en casa: `python scripts/descargar_fuentes.py smoke` y `python scripts/descargar_fuentes.py divipola`. Guardar `data/referencia/divipola_municipios.csv` en Drive.
- [ ] Llevar impreso o en el celular el resumen de cifras (sección 3 de este documento).

## 1. Primeros 10 minutos (7:50–8:00)

1. Leer el reto y la **rúbrica**. Anotar los pesos.
2. Identificar el formato de datos: ¿microdatos por unidad o tablas agregadas? ¿Con coordenadas? ¿Qué variables trae?
3. Cargar y perfilar:

```bash
pip install -r requirements.txt folium
python scripts/analisis_rapido.py --input <archivo_entregado> --region municipio
# si las columnas no se reconocen:
python scripts/analisis_rapido.py --input <archivo> --mapeo "COD_ACTIVIDAD=ciiu" --mapeo "TOT_OCUPADOS=personal_ocupado"
```

Abrir `reports/<archivo>/reporte.html`. En 1 minuto tienen KPIs, sectores, tamaño, formalidad, género, LQ, HHI, mapa y clústeres.
Si los datos son **agregados** (municipio × sector × unidades), usar las funciones de `cenu.indicators` con `peso="unidades"`.

## 2. Decisión Go/No-Go de la idea (8:00–8:07)

| Si el dataset trae… | Idea recomendada | Comando o módulo base |
|---|---|---|
| Coordenadas + CIIU | **Donde Falta, Emprende** (desiertos de servicios) | `scripts/donde_falta.py` |
| RUT, registro mercantil y municipio | **Semáforo de Formalización** | `indicators.indice_formalidad` + LQ |
| Sexo del propietario | **Ellas Mueven la Economía Popular** | `indicators.brecha_genero` |
| Solo tablas por municipio | **Ficha territorial automática** (Plan B) | `report.generar_reporte` por municipio |
| Tipo de emplazamiento (móvil, semifijo) | **Calle Ordenada** (venta en calle) | `spatial.clusters_dbscan` + Gi* |

Frase de una línea: *"Ayudamos a [usuario] a [decisión] usando el CENU."*

## 3. Cifras de contexto (verificadas por fuente en `data/cifras_oficiales/`)

| Dato | Valor | Fuente |
|---|---|---|
| Unidades económicas urbanas visibles (CENU 2024, preliminar) | **2.005.613** | DANE, 11-nov-2025 |
| Comercio / servicios / industria | 53,1 % / 32,3 % / 5,2 % | DANE vía prensa |
| Bogotá / Antioquia / Valle | 360.565 / 250.574 / 193.974 | DANE vía prensa |
| Venta en calle | 219.042 (≈1 de cada 10) | DANE vía prensa |
| Con RUT (sobre 1,55 M con información) | **49,2 %** | 3.ª entrega, may-2026 |
| Mujeres propietarias / hombres | 613.953 / 576.983 | 3.ª entrega |
| Ingresos 2023 | ≈ $2.421 billones | prensa |
| Censo anterior (1990) | 1.001.398 unidades | ficha metodológica CENU |
| Micronegocios EMICRON 2024 | 5.297.252; 77,6 % sin RUT | boletín EMICRON 2024 |
| Informalidad laboral, 23 ciudades (jun–ago 2026) | 42,0 % (Bogotá 34,1 %, Sincelejo 65,4 %) | GEIH |

## 4. Plantilla del pitch (5:00)

Ver [`pitch/plantilla_pitch.md`](../pitch/plantilla_pitch.md). Estructura: Gancho (25 s) → Problema y usuario (35 s) → Solución (20 s) → **Demo (90 s)** → Hallazgos (45 s) → Sostenibilidad (45 s) → Rigor, ética y cierre (30 s).

## 5. Reglas de oro

1. **Agregados, nunca unidades individuales** en mapas o tablas públicas (reserva estadística: Ley 79/1993 y art. 37 de la Ley 2335/2023). Usar celdas con un mínimo de unidades.
2. **Cifras preliminares:** decir "preliminar" y citar la entrega y la fecha.
3. **Denominadores:** el % de RUT se calcula sobre las unidades con información.
4. **No comparar el Conteo 2021 con el CENU 2024 como crecimiento**; son definiciones distintas.
5. Code freeze a las 9:20. Hacer dos ensayos cronometrados. Tener un PNG de respaldo para cada mapa.
