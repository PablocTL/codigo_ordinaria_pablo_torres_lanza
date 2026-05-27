# 🚌 Planificador de Rutas en Red de Transporte

**Proyecto de Estructuras de Datos y Algoritmos**

Sistema completo para modelar redes de transporte, calcular rutas óptimas e implementar análisis de conectividad usando programación orientada a grafos.

---

## 📋 Tabla de Contenidos

1. [Características](#características)
2. [Requisitos](#requisitos)
3. [Instalación y Uso](#instalación-y-uso)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Funcionalidades Principales](#funcionalidades-principales)
6. [Requisitos Técnicos Cumplidos](#requisitos-técnicos-cumplidos)
7. [Análisis Teórico](#análisis-teórico)
8. [Mejoras y BONUS](#mejoras-y-bonus)
9. [Testing](#testing)

---

## ✨ Características

### Funcionalidades Base (15 puntos)

✅ **Cargar red desde archivo CSV**
- Formato: `origen,destino,minutos`
- Validación de formato y valores
- Ignorar líneas vacías y comentarios

✅ **Gestión de Estaciones**
- Añadir estaciones nuevas
- Ver todas las estaciones (ordenadas)
- Listar conexiones directas de una estación

✅ **Gestión de Conexiones**
- Añadir conexiones entre estaciones
- Validar existencia de estaciones
- Verificar tiempos positivos
- Detectar conexiones duplicadas

✅ **Cálculo de Rutas Óptimas (Dijkstra)**
- Encuentra la ruta más rápida (tiempo mínimo)
- Muestra recorrido completo y tiempo total
- Complejidad: O((V + E) · log V)

✅ **Verificar Conectividad (BFS/DFS)**
- Determina si existe camino entre dos estaciones
- Implementación con BFS (óptima)
- Implementación alternativa con DFS

✅ **Persistencia de Datos**
- Guardar red en archivo CSV
- Recargar automáticamente al iniciar
- Mantiene formato para edición manual

✅ **Validación Exhaustiva**
- Estaciones existentes
- Tiempos positivos
- Sin conexiones duplicadas
- Control robusto de errores con try/except

### Funcionalidades BONUS (5 puntos)

⭐ **Ruta con Parada Intermedia Obligatoria**
- Calcula camino óptimo pasando por estación específica
- Usa dos llamadas a Dijkstra
- Aplicación real: "Debo pasar por X yendo de A a B"

⭐ **Análisis y Exportación**
- Detecta estación "hub" (mayor grado)
- Exporta informe JSON con:
  - Número de estaciones
  - Número de conexiones
  - Estación hub y su grado
  - Grado de todas las estaciones

---

## 🔧 Requisitos

- **Python:** 3.7 o superior
- **Librerías:** Ninguna externa (solo stdlib)
  - `heapq` - Cola de prioridad para Dijkstra
  - `csv` - Lectura/escritura de archivos
  - `json` - Exportación de reportes
  - `collections` - deque y defaultdict

---

## 🚀 Instalación y Uso

### 1. Ejecución Básica

```bash
python transport_network_planner.py
```

Menú interactivo aparecerá automáticamente.

### 2. Menú Principal

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

### 3. Ejecutar Tests

```bash
python test_transport_network.py
```

Ejecuta 41 tests unitarios cubriendo todas las funcionalidades.

### 4. Archivos Incluidos

```
transport_network_planner.py     # Programa principal (~520 líneas)
test_transport_network.py        # Tests unitarios (~450 líneas)
transport_network.csv            # Red de ejemplo (Madrid)
ANALISIS_TEORICO.md              # Análisis teórico completo
GUIA_DE_USO_Y_PRUEBAS.md         # Guía detallada y casos de prueba
README.md                         # Este archivo
```

---

## 🏗️ Estructura del Proyecto

### Diagrama de Clases

```python
class TransportNetwork:
    # Atributos
    graph: Dict[str, List[Tuple[str, int]]]  # Lista de adyacencia
    stations: Set[str]                        # Conjunto de estaciones
    network_file: str                         # Archivo de persistencia
    
    # Métodos Principales
    + load_network() → bool
    + save_network() → bool
    + add_station(name: str) → bool
    + add_connection(origin, dest, time) → bool
    + dijkstra(start, end) → (time, path)
    + are_connected_bfs(a, b) → bool
    + are_connected_dfs(a, b) → bool
    + shortest_path_via_waypoint(start, way, end) → (time, path)
    + find_hub_station() → str
    + export_analysis_report(filename) → bool
```

### Flujo de Datos

```
Usuario
   ↓
Menu Principal
   ↓
├─ Cargar CSV → Parser → TransportNetwork
├─ Añadir Estación → Validar → Set.add()
├─ Añadir Conexión → Validar → Dict append
├─ Dijkstra → MinHeap → Resultado
├─ BFS/DFS → Visit Set → Resultado
└─ Guardar → CSV Writer → Archivo

   ↓
Salida
```

---

## 🎯 Funcionalidades Principales

### 1. Carga de Red

```python
# Archivo CSV
origen,destino,minutos
Sol,Plaza Mayor,5
Sol,Gran Vía,3
Plaza Mayor,Atocha,12

# Resultado
Red cargada: 3 estaciones, 3 conexiones
```

### 2. Algoritmo de Dijkstra

```
Grafo:       A --5--> B
             |        |
             2        3
             |        |
             +--6---> C

dijkstra(A, C)
Opciones:
1. A → C: 6 min
2. A → B → C: 8 min

Retorna: (6, [A, C])  ✓ Óptima
```

### 3. Conectividad BFS

```
BFS: A ---> B ---> C
     |             
     +---> D

are_connected(A, D) → True
are_connected(C, A) → False (dirigido)
```

### 4. Ruta con Waypoint

```
Requisito: A → X (obligatorio) → B

Cálculo:
1. dijkstra(A → X) = (t1, ruta1)
2. dijkstra(X → B) = (t2, ruta2)
3. Total = t1 + t2, ruta1 + ruta2
```

---

## ✅ Requisitos Técnicos Cumplidos

### Estructuras de Datos

| Estructura | Ubicación | Justificación |
|-----------|-----------|--------------|
| **Diccionario** (lista adyacencia) | `TransportNetwork.graph` | O(1) acceso a vecinos de nodo |
| **Set** (estaciones) | `TransportNetwork.stations` | O(1) búsqueda existencia |
| **Heap** (min-heap) | `dijkstra()` | O(log V) extracción mínimo |
| **Deque** (BFS) | `are_connected_bfs()` | O(1) encola/desencola |
| **Diccionarios** (distancias) | Dijkstra y BFS | O(1) acceso/actualización |

### Algoritmos

| Algoritmo | Líneas | Complejidad | Uso |
|-----------|--------|-----------|-----|
| **Dijkstra** | ~70 | O((V+E) log V) | Ruta más rápida |
| **BFS** | ~30 | O(V + E) | Conectividad |
| **DFS** | ~30 | O(V + E) | Conectividad alternativa |
| **Floyd-Warshall** | - | O(V³) | (Mencionado como mejora) |

### Persistencia

```python
# Carga automática
if os.path.exists("transport_network.csv"):
    network.load_network()

# Guardado controlado
if save == 's':
    network.save_network()
```

### Validación y Errores

```python
try:
    # Operación
    network.add_connection(origin, dest, time)
except Exception as e:
    print(f"Error: {e}")

# Validaciones inline
if station not in self.stations:
    print("✗ Estación no existe")
    return False
```

---

## 📊 Análisis Teórico

### Complejidad Temporal

```
add_station:           O(1)
add_connection:        O(grado) ≈ O(1)
dijkstra:              O((V + E) · log V)  ← Crítico
are_connected (BFS):   O(V + E)
find_hub_station:      O(V)
load_network:          O(E)
save_network:          O(V + E)
```

### Complejidad Espacial

```
Grafo:                 O(V + E)
Dijkstra:              O(V) adicional
BFS:                   O(V) adicional
Global:                O(V + E)
```

### Justificación de Decisiones

| Decisión | Alternativa | Por qué Mejor |
|----------|-----------|---|
| Dijkstra para ruta óptima | BFS | Maneja pesos correctamente |
| Lista adyacencia | Matriz | O(V+E) vs O(V²) espacio |
| Min-heap | Array lineal | O(log V) vs O(V) por operación |
| BFS por defecto | DFS | Evita búsquedas profundas |

**Ver ANALISIS_TEORICO.md para análisis completo.**

---

## 🎁 Mejoras y BONUS

### BONUS 1: Ruta con Parada Intermedia ⭐

```python
time, path = network.shortest_path_via_waypoint(
    start="Madrid",
    waypoint="Toledo",  # Parada obligatoria
    end="Sevilla"
)

# Resultado:
# Madrid → ... → Toledo → ... → Sevilla
# Tiempo total: suma de ambas rutas óptimas
```

**Complejidad:** O((V+E) log V) - Dos Dijkstra

### BONUS 2: Análisis y Exportación ⭐

```python
# Exportar informe
network.export_analysis_report("network_analysis.json")

# Contenido del JSON:
{
  "num_stations": 13,
  "num_connections": 20,
  "hub_station": "Atocha",
  "hub_connections": 4,
  "all_stations": ["Atocha", "Bilbao", ...],
  "station_degrees": {"Atocha": 4, "Sol": 3, ...}
}
```

**Aplicación:** Análisis de la red, detección de cuellos de botella, planificación de infraestructura.

---

## 🧪 Testing

### Suite de Tests Completa

**41 tests unitarios** cubriendo:

```
✓ 5 tests - Creación y operaciones básicas
✓ 8 tests - Gestión de conexiones
✓ 6 tests - Algoritmo de Dijkstra
✓ 8 tests - Conectividad (BFS/DFS)
✓ 4 tests - Características BONUS
✓ 4 tests - Persistencia
✓ 2 tests - Grafos complejos
✓ 4 tests - Casos extremos
────────────────
  41 tests TOTAL
```

### Ejecución

```bash
$ python test_transport_network.py

test_add_station_success (test_transport_network.TestTransportNetworkBasics) ... ok
test_dijkstra (test_transport_network.TestDijkstra) ... ok
test_export_analysis_report (test_transport_network.TestBonusFeatures) ... ok
...

======================================================================
Tests ejecutados: 41
Exitosos: 41
Fallos: 0
Errores: 0
======================================================================
```

---

## 📈 Mejoras Futuras

### Corto Plazo
- [ ] Caché de rutas frecuentes
- [ ] Algoritmo A* con heurística
- [ ] Soporte para grafos ponderados no dirigidos

### Largo Plazo
- [ ] Base de datos (SQLite)
- [ ] API REST con Flask/FastAPI
- [ ] Visualización con NetworkX + Matplotlib
- [ ] Interfaz web (React/Vue)
- [ ] Análisis de comunidades (Louvain)

### Optimizaciones por Escala

| Escala | Técnica | Beneficio |
|--------|---------|-----------|
| < 100 estaciones | Actual (Dijkstra) | Óptimo |
| 100-10k | Floyd-Warshall precalculado | O(1) consultas |
| > 10k | Hierarchical (Hub Labels) | O(log n) consultas |

---

## 📝 Ejemplo de Sesión Completa

```
$ python transport_network_planner.py

✓ Red cargada: 13 estaciones, 20 conexiones.

MENÚ PRINCIPAL
...
Selecciona opción (1-9): 5

RED DE TRANSPORTE (13 estaciones, 20 conexiones)
[Muestra grafo...]

Estación de inicio: Sol
Estación destino: Casa de Campo

✓ RUTA MÁS RÁPIDA: Sol → Gran Vía → Chueca → Bilbao → Nuevos Ministerios → Moncloa → Casa de Campo
  Tiempo total: 61 minutos

Selecciona opción (1-9): 8

Nombre del informe (por defecto: network_analysis.json): 

✓ Informe exportado: 'network_analysis.json'

Selecciona opción (1-9): 9

¿Guardar cambios? (s/n): s
✓ Red guardada en 'transport_network.csv'
¡Hasta luego!
```

---

## 📚 Documentación Incluida

1. **ANALISIS_TEORICO.md** (4000+ palabras)
   - Análisis detallado de estructuras de datos
   - Cálculo de complejidades
   - Justificación de decisiones
   - Mejoras potenciales

2. **GUIA_DE_USO_Y_PRUEBAS.md**
   - Tutorial paso a paso
   - 9 casos de prueba documentados
   - Ejemplo de sesión completa
   - Troubleshooting

3. **transport_network_planner.py**
   - 520+ líneas de código comentado
   - Docstrings en todas las funciones
   - Manejo robusto de errores

4. **test_transport_network.py**
   - 450+ líneas de tests
   - 41 casos de prueba
   - Ejecución automatizada

---

## 🎓 Conceptos Aprendidos

- ✅ Grafos dirigidos ponderados
- ✅ Algoritmo de Dijkstra
- ✅ Búsqueda en grafos (BFS/DFS)
- ✅ Colas de prioridad (min-heap)
- ✅ Análisis de complejidad
- ✅ Persistencia con archivos
- ✅ Programación defensiva
- ✅ Testing unitario
- ✅ Documentación técnica

---

## 📞 Contacto y Preguntas

Para dudas sobre implementación, consulta:
1. `ANALISIS_TEORICO.md` - Conceptos teóricos
2. `GUIA_DE_USO_Y_PRUEBAS.md` - Uso práctico
3. Comentarios en el código - Explicaciones inline

---

## 📄 Licencia

Proyecto educativo - Libre para usar, modificar y distribuir.

---

**¡Gracias por revisar este proyecto!** 🚀

El sistema está listo para producción en redes de transporte pequeñas a medianas (< 10,000 estaciones). Para escalas mayores, considere las optimizaciones sugeridas en el análisis teórico.

