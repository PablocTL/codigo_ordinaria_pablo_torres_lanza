# Guía de Uso: Planificador de Rutas en Red de Transporte

## Requisitos previos

- Python 3.7 o superior (sin librerías externas, todo es de la librería estándar)
- Los archivos `transport_network_planner.py` y `transport_network.csv` en la misma carpeta

---

## Paso 0 — Si tienes tu propio CSV

Si ya tienes un archivo CSV con tu red de transporte, puedes cargarlo directamente en lugar de usar el de ejemplo.

### Formato requerido

El CSV debe tener exactamente tres columnas separadas por comas: origen, destino y tiempo en minutos. La primera línea es la cabecera y se ignora:

```csv
origen,destino,minutos
Sol,Plaza Mayor,5
Sol,Gran Vía,3
Gran Vía,Callao,4
Callao,Opera,6
Opera,Plaza Mayor,8
```

Reglas que debe cumplir el archivo:
- Una conexión por línea
- El tiempo debe ser un número entero positivo (sin decimales, sin ceros)
- Las líneas vacías se ignoran automáticamente
- Las líneas que empiecen por `#` se tratan como comentarios y también se ignoran
- Los nombres de estaciones son sensibles a mayúsculas (`Sol` y `sol` son estaciones distintas)

### Cómo cargarlo

**Opción A — Reemplazar el archivo por defecto:** Renombra tu CSV como `transport_network.csv` y ponlo en la misma carpeta que el programa. Se cargará automáticamente al arrancar.

**Opción B — Cargarlo desde el menú (opción 1):** Arranca el programa y en el menú elige la opción 1:

```
Selecciona opción (1-9): 1
Nombre del archivo CSV (por defecto: transport_network.csv): mi_red.csv
✓ Red cargada: 8 estaciones, 12 conexiones.
```

Puedes poner la ruta relativa o absoluta al archivo. Si pulsas Enter sin escribir nada, carga el archivo por defecto.

### Qué pasa con las líneas erróneas

El programa no se detiene si encuentra una línea mal formada. La reporta y continúa con el resto:

```
⚠ Línea 4 ignorada (formato inválido): "Sol,,abc"
⚠ Línea 7 ignorada (tiempo no positivo): "Atocha,Sol,-10"
✓ Red cargada: 6 estaciones, 9 conexiones.
```

Así puedes identificar exactamente qué líneas tienes que corregir en tu CSV.

---

## Paso 1 — Arrancar el programa

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python transport_network_planner.py
```

Al arrancar, el programa carga automáticamente la red desde `transport_network.csv`. Verás algo así:

```
✓ Red cargada: 13 estaciones, 20 conexiones.
```

A continuación aparece el menú principal con las 9 opciones disponibles.

---

## Paso 2 — Entender el menú

```
===============================================
PLANIFICADOR DE RUTAS - MENÚ PRINCIPAL
===============================================
1. Cargar red desde archivo
2. Añadir estación
3. Añadir conexión
4. Ver estaciones y conexiones
5. Ruta más rápida entre dos estaciones
6. ¿Están conectadas dos estaciones?
7. Ruta con parada intermedia obligatoria
8. Exportar informe de análisis
9. Guardar y salir
===============================================
```

Escribe el número de la opción y pulsa Enter.

---

## Paso 3 — Ver la red cargada (opción 4)

Antes de hacer nada, conviene ver qué estaciones y conexiones existen:

```
Selecciona opción (1-9): 4
```

El programa mostrará cada estación y sus conexiones con el tiempo en minutos:

```
RED DE TRANSPORTE (13 estaciones, 20 conexiones)

Atocha:
  → Chamartín        ( 20 min)
  → Reina Sofía      (  3 min)

Sol:
  → Gran Vía         (  3 min)
  → Plaza Mayor      (  5 min)
...
```

---

## Paso 4 — Buscar la ruta más rápida (opción 5)

Esta es la función principal. Usa el algoritmo de Dijkstra para encontrar el camino más rápido entre dos estaciones.

```
Selecciona opción (1-9): 5
Estación de inicio: Sol
Estación destino: Chamartín
```

El resultado muestra la ruta completa y el tiempo total:

```
✓ RUTA MÁS RÁPIDA: Sol → Gran Vía → Chueca → Bilbao → Nuevos Ministerios → Moncloa → Casa de Campo
  Tiempo total: 61 minutos
```

**Casos especiales:**
- Si origen y destino son la misma estación → devuelve esa estación con 0 minutos
- Si no existe ningún camino → avisa con `✗ No hay ruta disponible`

---

## Paso 5 — Comprobar si dos estaciones están conectadas (opción 6)

Si solo necesitas saber si existe algún camino (sin importar cuánto tarde):

```
Selecciona opción (1-9): 6
Primera estación: Sol
Segunda estación: Chamartín
```

Respuesta posible:

```
✓ Las estaciones 'Sol' y 'Chamartín' ESTÁN conectadas.
```

o bien:

```
✗ Las estaciones 'Casa de Campo' y 'Sol' NO están conectadas.
```

Importante: el grafo es dirigido. Que Sol llegue a Chamartín no implica que Chamartín llegue a Sol.

---

## Paso 6 — Añadir una estación nueva (opción 2)

Si necesitas ampliar la red con una estación que aún no existe:

```
Selecciona opción (1-9): 2
Nombre de la estación: Leganés
✓ Estación 'Leganés' añadida.
```

La estación queda creada sin conexiones. Para conectarla, usa la opción 3.

---

## Paso 7 — Añadir una conexión (opción 3)

Conecta dos estaciones indicando el tiempo de viaje en minutos:

```
Selecciona opción (1-9): 3
Estación origen: Leganés
Estación destino: Sol
Tiempo (minutos): 30
✓ Conexión añadida: 'Leganés' → 'Sol' (30 min)
```

**Validaciones automáticas:**
- Ambas estaciones deben existir en la red
- El tiempo debe ser un número positivo
- No se permiten conexiones duplicadas entre el mismo par de estaciones

Para una red bidireccional, añade las dos direcciones por separado (Sol → Leganés y Leganés → Sol).

---

## Paso 8 — Ruta con parada obligatoria (opción 7)

Útil cuando necesitas pasar por un punto intermedio concreto, por ejemplo ir de Sol a Chamartín pasando por Opera:

```
Selecciona opción (1-9): 7
Estación de inicio: Sol
Estación intermedia (obligatoria): Opera
Estación destino: Chamartín
```

El programa calcula internamente dos rutas de Dijkstra (inicio → intermedia y intermedia → destino) y las une:

```
✓ RUTA CON PARADA OBLIGATORIA: Sol → ... → Opera → ... → Chamartín
  Tiempo total: 47 minutos
```

---

## Paso 9 — Exportar un análisis de la red (opción 8)

Genera un archivo JSON con estadísticas de la red: número de estaciones, conexiones, estación hub (la más conectada) y grado de cada estación:

```
Selecciona opción (1-9): 8
Nombre del informe (por defecto: network_analysis.json): [Enter]
✓ Informe exportado: 'network_analysis.json'
```

El archivo resultante tiene esta estructura:

```json
{
  "num_stations": 13,
  "num_connections": 20,
  "hub_station": "Atocha",
  "hub_connections": 4,
  "all_stations": ["Atocha", "Bilbao", ...],
  "station_degrees": {"Atocha": 4, "Sol": 3, ...}
}
```

---

## Paso 10 — Guardar y salir (opción 9)

Al terminar, elige la opción 9. El programa pregunta si quieres guardar los cambios:

```
Selecciona opción (1-9): 9
¿Guardar cambios? (s/n): s
✓ Red guardada en 'transport_network.csv'
¡Hasta luego!
```

Si respondes `n`, los cambios de esa sesión se pierden y el CSV original queda intacto.

---

## Ejecutar los tests

Para verificar que todo funciona correctamente:

```bash
python test_transport_network.py
```

Salida esperada:

```
Ran 41 tests in 0.008s

OK
```

---

## Referencia rápida de errores comunes

| Mensaje | Causa | Solución |
|---|---|---|
| `✗ La estación no existe` | Nombre mal escrito | Revisar opción 4 para ver nombres exactos |
| `✗ El tiempo debe ser positivo` | Tiempo negativo o cero | Introducir un número mayor que 0 |
| `✗ Conexión ya existe` | Duplicado | Esa conexión ya está en la red |
| `✗ No hay ruta disponible` | Grafo desconectado | Comprobar conexiones con opción 6 |
| `Archivo no encontrado` | CSV ausente | Crear la red desde cero con opciones 2 y 3 |
