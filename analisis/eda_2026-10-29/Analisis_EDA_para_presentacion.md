# Anticipa · Métricas adicionales para la presentación

Análisis realizado el 29/10/2026 sobre el histórico conservado. Se han leído **111.756 Parquet y 17.044.760 observaciones** de `trip_updates`, correspondientes a 47 fechas UTC con datos dentro del intervalo 17/05/2026–03/07/2026 (48 días naturales; falta el 03/06). Las cifras del inventario provienen de su versión de 29/10/2026. No se ha modificado el histórico ni la web.

## Qué añadiría a la presentación

| Métrica calculada | Resultado | Qué permite explicar |
|---|---:|---|
| Observaciones evaluables con retraso >5 min | **27,5 %** | Frecuencia de estimaciones de retraso relevantes, con un umbral fácil de entender. |
| Observaciones evaluables con retraso >10 min | **14,4 %** | Magnitud de los retrasos altos. Numerador: 2.316.038; denominador: 16.081.549. |
| Mediana / media / P90 / P95 | **2 / 5,1 / 14 / 21 min** | La cola de retrasos que queda oculta si solo se muestra la media. |
| >10 min, 04–06 h frente a 18–20 h | **1,7 % → 16,8 %** | Cómo cambia la frecuencia observada con la hora. Denominadores: 359.361 y 1.816.565. |
| >10 min, laborables frente a fin de semana | **15,3 % frente a 11,3 %** | Un patrón descriptivo para segmentar el análisis futuro. Solo horas 04–24. |

Para la presentación: usar [el riesgo por horario](01_riesgo_por_hora.png) como gráfico principal adicional y [la media y los percentiles](02_media_y_cola.png) para explicar por qué conviene mostrar percentiles. La comparación laborables/fin de semana puede quedar como apoyo para preguntas. Los SVG permiten editar o ampliar los gráficos sin perder nitidez.

## Otras cifras útiles para preguntas del tribunal

- **16.081.549 observaciones evaluables (94,3 %)** dentro de −300 a 7.200 segundos, incluidos.
- **857.457 sin arrival_delay (5,0 %)** y **105.754 fuera del intervalo (0,62 %)**. El bruto se conserva: excluir del indicador no significa borrar.
- **152.277 pares fecha local + trip_id observados**, de los cuales 152.061 tienen al menos un retraso evaluable. **46.984 (30,9 %)** muestran alguna estimación >10 minutos. Este porcentaje mide si se observó al menos una estimación alta por identificador y día; no es el porcentaje de viajes que llegaron tarde.
- Cada par fecha + trip_id aporta **111,9 observaciones de media; mediana 101**. Son lecturas repetidas de próximas paradas, no 111,9 trenes independientes. El porcentaje por observaciones puede sobrerrepresentar viajes visibles durante más tiempo.
- Inventario del mismo intervalo: **18.941.338 posiciones**, **17.044.760 actualizaciones de parada** y **6.900.582 filas de avisos**. Son tres tipos de registros; las filas de avisos contienen repeticiones y no equivalen a incidencias únicas.

## Correcciones concretas de la diapositiva adjunta

1. Sustituir «1 de cada 10 trenes» por **«1 de cada 10 observaciones»** cuando se interpreta el P90. Son estimaciones publicadas de retraso para próximas paradas, no llegadas verificadas.
2. No afirmar «captura continua» sin matizar. Se conserva información desde el 17 de mayo, pero hay huecos: el período comprende 48 días naturales y tiene archivos en 47 fechas. La ausencia de archivos no basta para atribuir una caída a Renfe.
3. Las medias recalculadas se parecen a las del Sprint 1, pero algunos percentiles difieren: a las 22–00 h el P90 recalculado es **17 minutos**, frente a 16 en la diapositiva. Conviene usar los valores de una única versión del análisis y mantener su método y fecha.
4. El EDA de retrasos aquí calculado usa **toda la red capturada**, sin filtro por Madrid. No presentarlo como un resultado exclusivo de Madrid. No depende de cruzar el GTFS de octubre con servicios de mayo–julio.
5. El aumento por horario es descriptivo: no demuestra por sí solo propagación de retrasos, causalidad por demanda ni rendimiento predictivo de Anticipa.

## Calidad comprobada en el original

Muestra determinista de **80 mensajes**: ocho fechas (18/05, 25/05, 01/06, 08/06, 15/06, 22/06, 29/06 y 01/07), un archivo central de cada hora UTC par entre las 04 y las 22. Contiene **12.941 actualizaciones de parada**:

- 605 no tienen campo de llegada.
- 123 tienen llegada pero **no incluyen delay**; el parser histórico puede guardarlas como cero.
- 12.213 incluyen delay explícito, de ellas 3.694 con cero explícito.

Esta muestra acredita la diferencia entre dato ausente y cero; no permite asignar esos porcentajes a todo el histórico. Las cifras agregadas se calculan sobre el Parquet tal como está conservado. Por tanto, **«delay ≤0» no debe denominarse puntualidad real** sin auditar y reprocesar la presencia del campo en el conjunto completo.

## Método y límites de interpretación

- Fuentes locales: `data/bronze/trip_updates/date=YYYY-MM-DD/*.parquet`, originales `data/raw/trip_updates/YYYY-MM-DD/*.pb` e inventario `data/inventory/pilot.json`.
- Selección por particiones **UTC** del 17/05 al 03/07, ambos incluidos. Franjas y día de semana calculados en `Europe/Madrid`. Las primeras dos horas locales del 04/07 pertenecen a la partición UTC del 03/07; se incluyen en las métricas globales. Los gráficos horarios y la comparación semanal muestran 04–24 h, por lo que no incorporan esas horas.
- Una observación es una fila de actualización de parada de un snapshot. El mismo viaje y parada puede aparecer en múltiples snapshots.
- Denominador de retrasos: filas con `arrival_delay` entre **−300 y 7.200 segundos**. Los nulos y los valores fuera de rango se cuentan aparte.
- Media: suma de los segundos de todas las observaciones evaluables dividida por su número y por 60; incluye adelantos y ceros. No es una media de medias diarias ni solo de retrasos positivos.
- Percentiles exactos con interpolación lineal sobre el histograma de segundos ponderado por frecuencia. No se promedian percentiles de días.
- Umbrales estrictos: >300 y >600 segundos; 5 y 10 minutos exactos no cuentan como superiores.
- Laborables = lunes a viernes; fin de semana = sábado y domingo, sin clasificación adicional de festivos. No se controla por diferencias de líneas y oferta, ni se infiere causalidad.
- Pares fecha + trip_id: día civil de Madrid y código normalizado con `trim`, sin validar calendario GTFS, terminal, llegada efectiva, cancelación o reutilización de códigos. Son identificadores observados, no circulaciones planificadas certificadas.
- Se utiliza el EDA declarado en el Sprint 1 y la memoria para comparar método y cifras. El recálculo sobre los archivos actualmente conservados no garantiza que el conjunto sea idéntico al empleado al redactarlos.

Los agregados completos y la selección de mensajes originales de la muestra se conservan en `datos_calculados/` (histograma comprimido en `histogram.json.gz`); `metricas.json` contiene las cifras de los gráficos. El análisis no incorpora datos personales de viajeros ni datos de demanda.
