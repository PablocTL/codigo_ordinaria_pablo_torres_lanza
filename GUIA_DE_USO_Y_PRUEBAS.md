# GUÍA DE USO Y CASOS DE PRUEBA
## Planificador de Rutas en Red de Transporte

---

## PARTE 1: GUÍA DE USO

### Requisitos
- Python 3.7+
- Librerías estándar (no requiere pip install)

### Ejecución
```bash
python transport_network_planner.py
```

### Archivos
- `transport_network.csv`: Base de datos de red (cargada automáticamente)
- `transport_network_planner.py`: Programa principal
- `network_analysis.json`: Informe generado (opcional)

---

## PARTE 2: DESCRIPCIÓN DEL MENÚ

### Opción 1: Cargar Red desde Archivo
```
Selecciona opción (1-9): 1
Nombre del archivo CSV (por defecto: transport_network.csv): [ENTER o nombre alternativo]
```

**Qué hace:**
- Lee archivo CSV formato: origen,destino,minutos
- Ignora líneas vacías y comentarios (#)
- Valida tiempos positivos y formato
- Reporta errores por línea sin detener

**Ejemplo de CSV:**
```csv
origen,destino,minutos
Sol,Plaza Mayor,5
Sol,Gran Vía,3
Gran Vía,Callao,4
```

### Opción 2: Añadir Estación
```
Selecciona opción (1-9): 2
Nombre de la estación: Nuevas Estaciones
✓ Estación 'Nuevas Estaciones' añadida.
```

**Qué hace:**
- Añade estación aislada (sin conexiones)
- Valida que no exista ya
- Disponible inmediatamente para conectar

### Opción 3: Añadir Conexión
```
Selecciona opción (1-9): 3
[Muestra red actual]
Estación origen: Sol
Estación destino: Plaza Mayor
Tiempo (minutos): 5
✓ Conexión añadida: 'Sol' → 'Plaza Mayor' (5 min)
```

**Qué hace:**
- Valida que ambas estaciones existan
- Verifica tiempo positivo
- Detecta duplicados
- Crea arista dirigida (unidireccional)

**Nota:** Para redes bidireccionales, añadir ambas direcciones:
```
Sol → Plaza Mayor (5 min)
Plaza Mayor → Sol (5 min)
```

### Opción 4: Ver Estaciones y Conexiones
```
Selecciona opción (1-9): 4

======================================================================
RED DE TRANSPORTE (13 estaciones, 20 conexiones)
======================================================================

Atocha:
  → Chamartín        ( 20 min)
  → Reina Sofía      (  3 min)

Bilbao:
  → Nuevos Ministerios (  10 min)

...
```

**Muestra:**
- Total de estaciones y conexiones
- Para cada estación: conexiones ordenadas por tiempo
- Estaciones sin salida no aparecen

### Opción 5: Ruta Más Rápida entre Dos Estaciones
```
Selecciona opción (1-9): 5
[Muestra red actual]
Estación de inicio: Sol
Estación destino: Chamartín

✓ RUTA MÁS RÁPIDA: Sol → Gran Vía → Callao → Opera → Plaza Mayor → Atocha → Chamartín
  Tiempo total: 47 minutos
```

**Algoritmo:** Dijkstra con min-heap
**Garantía:** Ruta óptima (tiempo mínimo)
**Complejidad:** O((V + E) · log V)

**Casos:**
- Misma estación: Retorna la estación con tiempo 0
- Sin ruta: Aviso "No hay ruta disponible"
- Desconexo: Aviso "No hay ruta disponible"

### Opción 6: ¿Están Conectadas Dos Estaciones?
```
Selecciona opción (1-9): 6
[Muestra red actual]
Primera estación: Sol
Segunda estación: Chamartín

✓ Las estaciones 'Sol' y 'Chamartín' ESTÁN conectadas.
```

**Algoritmo:** BFS (Breadth-First Search)
**Complejidad:** O(V + E)
**Nota:** No importa si la ruta es rápida o lenta, solo si existe algún camino

### Opción 7: Ruta con Parada Intermedia Obligatoria ⭐ BONUS
```
Selecciona opción (1-9): 7
[Muestra red actual]
Estación de inicio: Sol
Estación intermedia (obligatoria): Opera
Estación destino: Chamartín

✓ RUTA CON PARADA OBLIGATORIA: Sol → Gran Vía → Callao → Opera → Plaza Mayor → Atocha → Chamartín
  Tiempo total: 47 minutos
```

**Qué calcula:**
- Dijkstra(inicio → intermedia)
- + Dijkstra(intermedia → destino)
- = Ruta óptima pasando por intermedia

**Aplicación real:** "Quiero ir de A a B, pero necesito pasar por C"

### Opción 8: Exportar Informe de Análisis ⭐ BONUS
```
Selecciona opción (1-9): 8
Nombre del informe (por defecto: network_analysis.json): [ENTER]
✓ Informe exportado: 'network_analysis.json'
```

**Archivo generado (`network_analysis.json`):**
```json
{
  "num_stations": 13,
  "num_connections": 20,
  "hub_station": "Atocha",
  "hub_connections": 4,
  "all_stations": [
    "Atocha",
    "Bilbao",
    "Callao",
    ...
  ],
  "station_degrees": {
    "Atocha": 4,
    "Sol": 3,
    "Gran Vía": 3,
    ...
  }
}
```

**Contenido:**
- Número de estaciones y conexiones totales
- Estación "hub" (más conexiones salientes)
- Número de conexiones del hub
- Grado de cada estación (ordenado descendente)

### Opción 9: Guardar y Salir
```
Selecciona opción (1-9): 9
¿Guardar cambios? (s/n): s
✓ Red guardada en 'transport_network.csv'
¡Hasta luego!
```

**Qué hace:**
- Pregunta si guardar cambios
- Escribe toda la red en CSV
- Mantiene formato para recargar

---

## PARTE 3: CASOS DE PRUEBA

### Test 1: Carga Inicial
**Objetivo:** Verificar que el programa carga el archivo ejemplo

**Pasos:**
1. Ejecutar programa
2. Ver mensaje de carga automática
3. Seleccionar opción 4 (Ver red)

**Resultado esperado:**
```
✓ Red cargada: 13 estaciones, 20 conexiones.
RED DE TRANSPORTE (13 estaciones, 20 conexiones)
...
```

---

### Test 2: Añadir Estación Nueva
**Objetivo:** Verificar creación de estaciones aisladas

**Pasos:**
```
1. Opción 2
2. Nombre: "Leganés"
3. Opción 4 (Ver red)
```

**Resultado esperado:**
```
✓ Estación 'Leganés' añadida.
RED DE TRANSPORTE (14 estaciones, 20 conexiones)
Leganés: (sin conexiones salientes)
```

---

### Test 3: Conexión Válida
**Objetivo:** Crear nueva conexión

**Pasos:**
```
1. Opción 3
2. Origen: "Leganés"
3. Destino: "Sol"
4. Tiempo: 30
```

**Resultado esperado:**
```
✓ Conexión añadida: 'Leganés' → 'Sol' (30 min)
```

---

### Test 4: Validación de Errores en Conexión

**Test 4a: Estación inexistente**
```
1. Opción 3
2. Origen: "Estación Fantasma"
3. Destino: "Sol"
✗ La estación origen 'Estación Fantasma' no existe.
```

**Test 4b: Tiempo negativo**
```
1. Opción 3
2. Origen: "Sol"
3. Destino: "Gran Vía"
4. Tiempo: -5
✗ El tiempo debe ser positivo (recibido: -5).
```

**Test 4c: Tiempo no numérico**
```
1. Opción 3
2. Origen: "Sol"
3. Destino: "Gran Vía"
4. Tiempo: treinta
✗ Tiempo inválido. Introduce un número.
```

**Test 4d: Conexión duplicada**
```
1. Opción 3
2. Origen: "Sol"
3. Destino: "Plaza Mayor"
4. Tiempo: 10
✗ Conexión 'Sol' → 'Plaza Mayor' ya existe (5 min).
```

---

### Test 5: Dijkstra - Ruta Más Rápida
**Objetivo:** Verificar algoritmo de ruta óptima

**Caso A: Ruta directa existente**
```
Inicio: Sol
Destino: Gran Vía
Esperado: Sol → Gran Vía (3 min)
```

**Caso B: Ruta con múltiples saltos**
```
Inicio: Sol
Destino: Chamartín
Esperado: Sol → ... → Chamartín (tiempo mínimo)
```

**Caso C: Mismo origen y destino**
```
Inicio: Sol
Destino: Sol
Esperado: Sol (0 minutos)
```

**Caso D: Sin ruta posible (grafo desconectado)**
```
Inicio: Casa de Campo
Destino: Sol
Esperado: ✗ No hay ruta disponible entre...
```

---

### Test 6: Conectividad BFS
**Objetivo:** Verificar si dos estaciones están conectadas

**Caso A: Conectadas (ambas direcciones)**
```
A: Sol
B: Chamartín
Esperado: ✓ ESTÁN conectadas
```

**Caso B: Conectadas (una dirección)**
```
A: Sol
B: Casa de Campo
Esperado: ✓ ESTÁN conectadas (si existe camino)
```

**Caso C: No conectadas**
```
A: Casa de Campo
B: Sol
Esperado: ✗ NO están conectadas
```

---

### Test 7: Parada Intermedia Obligatoria ⭐
**Objetivo:** Verificar ruta con waypoint

**Escenario:**
```
Inicio: Sol
Intermedia: Opera
Destino: Chamartín
```

**Proceso interno:**
```
1. Dijkstra(Sol → Opera)  → camino1 + tiempo1
2. Dijkstra(Opera → Chamartín) → camino2 + tiempo2
3. Resultado: camino1 + camino2[1:] (sin duplicar Opera) + tiempo1 + tiempo2
```

---

### Test 8: Exportación de Análisis ⭐
**Objetivo:** Generar informe JSON

**Pasos:**
```
1. Opción 8
2. Presionar ENTER (nombre por defecto)
```

**Validación:**
```
1. Abrir network_analysis.json
2. Verificar:
   - num_stations: 13
   - num_connections: 20
   - hub_station: "Atocha" (o similar con más grado)
   - hub_connections: 4 (o corresponda)
   - all_stations: lista de todas
   - station_degrees: frecuencias correctas
```

---

### Test 9: Persistencia
**Objetivo:** Verificar que cambios se guardan y recargan

**Pasos:**
```
1. Ejecutar programa
2. Opción 2: Añadir estación "TestStation"
3. Opción 3: Conectar "TestStation" → "Sol" (10 min)
4. Opción 9: Guardar (responder 's')
5. Salir del programa
6. Ejecutar nuevamente
7. Opción 4: Ver red
```

**Resultado esperado:**
```
✓ Red cargada: ... estaciones, ... conexiones
Verificar que "TestStation" aparece en red
```

---

## PARTE 4: EJEMPLO COMPLETO DE SESIÓN

### Escenario: Viaje Madrid
```
Ejecutar programa...
✓ Red cargada: 13 estaciones, 20 conexiones.

MENÚ PRINCIPAL
1. Cargar red desde archivo
...
9. Guardar y salir

Selecciona opción (1-9): 4

RED DE TRANSPORTE (13 estaciones, 20 conexiones)
======================================================================

Atocha:
  → Chamartín        ( 20 min)
  → Reina Sofía      (  3 min)

Bilbao:
  → Nuevos Ministerios (  10 min)

...

Selecciona opción (1-9): 5

RED DE TRANSPORTE (13 estaciones, 20 conexiones)
...

Estación de inicio: Sol
Estación destino: Casa de Campo

✓ RUTA MÁS RÁPIDA: Sol → Gran Vía → Chueca → Bilbao → Nuevos Ministerios → Moncloa → Casa de Campo
  Tiempo total: 61 minutos

Selecciona opción (1-9): 6

RED DE TRANSPORTE (13 estaciones, 20 conexiones)
...

Primera estación: Casa de Campo
Segunda estación: Atocha

✓ Las estaciones 'Casa de Campo' y 'Atocha' ESTÁN conectadas.

Selecciona opción (1-9): 8

Nombre del informe (por defecto: network_analysis.json): 

✓ Informe exportado: 'network_analysis.json'

Selecciona opción (1-9): 9

¿Guardar cambios? (s/n): n
¡Hasta luego!
```

---

## PARTE 5: TROUBLESHOOTING

| Problema | Causa | Solución |
|----------|-------|----------|
| "Archivo no encontrado" | CSV no existe en carpeta | Crear con opción 1 o manualmente |
| "Estación no existe" | Typo en nombre | Verificar opción 4 |
| "No hay ruta" | Grafo desconectado | Usar opción 6 para verificar conexión |
| Programa lento | Red muy grande | Normal para V > 10000 |
| JSON no se genera | Permisos de escritura | Verificar carpeta |

---

## PARTE 6: DATOS DE EJEMPLO INCLUIDOS

### Red de Madrid (13 estaciones)
```
Sol         (centro, 3 conexiones)
Plaza Mayor (2 conexiones)
Atocha      (hub, 4 conexiones)
Gran Vía    (2 conexiones)
Callao      (2 conexiones)
Chueca      (2 conexiones)
Bilbao      (1 conexión)
Opera       (2 conexiones)
Malasaña    (1 conexión)
Reina Sofía (1 conexión)
Parque Retiro (1 conexión)
Chamartín   (1 conexión)
Nuevos Ministerios (2 conexiones)
Moncloa     (1 conexión)
Casa de Campo (0 conexiones salientes)
```

**Total: 13 estaciones, 20 conexiones, tiempo mínimo: 3 min, máximo: 25 min**

