# ANÁLISIS TEÓRICO: PLANIFICADOR DE RUTAS EN RED DE TRANSPORTE

## 1. ESTRUCTURAS DE DATOS UTILIZADAS

### 1.1 Lista de Adyacencia (Grafo Ponderado)
```python
graph: Dict[str, List[Tuple[str, int]]]
```

**Descripción:**
- Representación del grafo dirigido ponderado
- Clave: nombre de estación (nodo)
- Valor: lista de tuplas (destino, tiempo_minutos)

**Ventajas:**
- Almacenamiento eficiente: solo guarda aristas que existen
- Iteración rápida sobre vecinos de un nodo: O(grado del nodo)
- Ideal para grafos dispersos (típico en redes de transporte)

**Alternativas descartadas:**
- Matriz de adyacencia: O(V²) espacio incluso para grafos dispersos
- Lista de aristas simple: O(E) para buscar vecinos de un nodo

### 1.2 Conjunto de Estaciones (Set)
```python
stations: Set[str]
```

**Descripción:**
- Almacena todas las estaciones únicas de la red

**Ventajas:**
- Búsqueda O(1) para verificar existencia de estación
- Evita duplicados automáticamente
- Operación rápida en validaciones

**Alternativa:** Lista ordenada habría requerido O(log n) o O(n) para búsquedas

### 1.3 Min-Heap en Dijkstra
```python
heap = [(distancia, estación)]
heapq.heappush(heap, elemento)
heapq.heappop(heap)
```

**Descripción:**
- Cola de prioridad implementada como min-heap binario
- Obtiene siempre el nodo con menor distancia

**Ventajas:**
- Extracción de mínimo: O(log V)
- Inserción: O(log V)
- Fundamental para eficiencia de Dijkstra

### 1.4 Estructuras Auxiliares
- **Diccionarios para distancias y padres:** O(1) acceso y actualización
- **Conjuntos para visitados (BFS/DFS):** O(1) búsqueda y adición
- **Cola (deque) para BFS:** O(1) popleft y append
- **Pila (list) para DFS:** O(1) pop y append

---

## 2. ANÁLISIS DE COMPLEJIDAD

### 2.1 Operación: Añadir Conexión
```python
def add_connection(self, origin, destination, time_minutes):
    # Validación de estaciones: O(1) búsqueda en set
    # Validación de tiempo: O(1)
    # Verificar duplicados: O(grado del nodo origen)
    # Añadir: O(1)
```

**Complejidad Temporal:**
- Mejor caso: O(1) - nodo sin conexiones previas
- Peor caso: O(d) - donde d = grado del nodo (número de conexiones salientes)
- Caso promedio: O(1) si el grado es bajo (típicamente constante en redes reales)

**Complejidad Espacial:** O(1) adicional

**Optimización posible:** Usar conjunto de tuplas en lugar de lista para O(1) búsqueda de duplicados, pero aumentaría complejidad espacial

### 2.2 Algoritmo de Dijkstra
```python
def dijkstra(self, start, end):
    # Inicialización: O(V)
    # Bucle while con hasta V extracciones
    # Cada extracción: O(log V) del heap
    # Relajación de hasta E aristas: E * O(log V) inserciones
```

**Complejidad Temporal:** **O((V + E) · log V)**
- V extracciones: O(V · log V)
- E inserciones en heap: O(E · log V)

**Complejidad Espacial:** O(V)
- Diccionarios de distancias y padres: O(V)
- Heap: O(V) en peor caso
- Conjunto de visitados: O(V)

**Comparación de algoritmos:**
- Dijkstra con matriz adyacencia: O(V²)
- Dijkstra con lista adyacencia + heap: O((V + E) · log V) ✓ MEJOR
- Bellman-Ford: O(V · E) - permitiría pesos negativos pero innecesario

**Justificación:** Dijkstra es óptimo para grafos dirigidos ponderados con pesos positivos, que es exactamente nuestro caso (tiempos siempre positivos).

### 2.3 Búsqueda de Conectividad: BFS
```python
def are_connected_bfs(self, station_a, station_b):
    # Inicialización: O(1)
    # Cada vértice entra y sale de cola una sola vez: O(V)
    # Cada arista se examina una sola vez: O(E)
    # Operaciones de conjunto (visited): O(1) por operación
```

**Complejidad Temporal:** **O(V + E)**
- V vértices visitados máximo
- E aristas examinadas máximo
- Operaciones O(1) en visitados

**Complejidad Espacial:** O(V)
- Cola: O(V) máximo
- Conjunto visitados: O(V)

### 2.4 Búsqueda de Conectividad: DFS
```python
def are_connected_dfs(self, station_a, station_b):
    # Exactamente el mismo análisis que BFS
```

**Complejidad Temporal:** **O(V + E)**
**Complejidad Espacial:** O(V)

**BFS vs DFS:**
- **Tiempo:** Idéntico
- **Espacio:**
  - BFS peor caso: O(V) en cola (grafo ancho)
  - DFS peor caso: O(V) en pila (grafo profundo)
- **En la práctica:** BFS suele ser preferible para redes (evita búsquedas profundas), pero ambas son válidas

### 2.5 Ruta con Parada Intermedia (BONUS)
```python
def shortest_path_via_waypoint(self, start, waypoint, end):
    # Dijkstra(start → waypoint): O((V + E) · log V)
    # + Dijkstra(waypoint → end): O((V + E) · log V)
    # Combinación de paths: O(V)
```

**Complejidad Temporal:** **O((V + E) · log V)**
- Factor constante de 2, pero sigue siendo O((V + E) · log V)

**Estrategia:**
- No es "camino más corto con restricción" general
- Simplemente suma dos problemas de Dijkstra
- Correcto porque ambas rutas son óptimas
- Garantiza menor tiempo total entre todas las rutas que pasan por waypoint

### 2.6 Operaciones de Carga/Guardado
```python
def load_network(self) / def save_network(self):
    # Lectura del archivo: O(E) líneas
    # Procesamiento por línea: O(1) validación
    # Escritura: O(V + E) filas
```

**Complejidad:** O(E) donde E = número de aristas

---

## 3. COMPLEJIDAD ESPACIAL GLOBAL

**Estructura principal del grafo:**
```
Grafo: V estaciones + E aristas
= O(V) para conjunto stations
+ O(V) para llaves dict graph
+ O(E) para todas las tuplas (destino, tiempo)
= O(V + E)
```

**En operaciones:**
- Dijkstra: O(V) adicional (distancias, padres, visitados)
- BFS/DFS: O(V) adicional (visitados, cola/pila)
- Global: O(V + E) para grafo + O(V) para operaciones

---

## 4. JUSTIFICACIÓN DE DECISIONES DE DISEÑO

### 4.1 Por qué Diccionarios para Lista de Adyacencia

| Alternativa | Pros | Contras |
|-------------|------|---------|
| **Dict[str, List]** ✓ | O(1) acceso, flexible con nombres, iterable | Orden no garantizado (Python 3.7+ sí) |
| Matriz 2D | Indexing directo | O(V²) espacio, necesita mapeo nombre↔índice |
| Lista de objetos Node | OOP puro | Más memoria, más complejidad |

**Decisión:** Diccionarios por su flexibilidad con nombres de estaciones reales y eficiencia de acceso.

### 4.2 Por qué Dijkstra en lugar de BFS

| Criterio | BFS | Dijkstra |
|----------|-----|----------|
| Grafos no ponderados | ✓ Óptimo | Funciona pero overkill |
| Grafos ponderados | ✗ Incorrecto | ✓ Correcto |
| Tiempo | O(V + E) | O((V+E)log V) |
| Aplicabilidad | Redes sin pesos | **Redes con tiempos** |

**Decisión:** Dijkstra es imprescindible para tiempo mínimo con pesos.

### 4.3 Validación de Duplicados en O(grado)

```python
# En lugar de:
if (destination, time) in set(neighbors)  # O(grado) hash, O(grado) espacio extra

# Usamos:
for dest, tiempo in graph[origin]:
    if dest == destination:  # O(grado) comparaciones directas
        return False
```

**Justificación:**
- Grado típico bajo en redes reales (≈2-5 conexiones por estación)
- O(grado) ≈ O(1) en la práctica
- No merece complejidad adicional de set de tuplas

---

## 5. ANÁLISIS DE VALIDACIONES Y MANEJO DE ERRORES

### Validaciones Implementadas

| Validación | Punto | Complejidad |
|-----------|-------|-------------|
| Estación existe | Antes de Dijkstra, add_connection | O(1) |
| Tiempo positivo | add_connection | O(1) |
| Duplicados | add_connection | O(grado) |
| Archivo existe | load_network | O(1) |
| Formato CSV | load_network | O(1) por línea |
| Estaciones no vacías | Múltiples puntos | O(1) |

### Recuperación de Errores

1. **Archivo no encontrado:** Iniciar red vacía
2. **Línea CSV malformada:** Informar y continuar
3. **Valores inválidos:** Rechazar y solicitar reintentos
4. **Arista duplicada:** Informar sin silencio
5. **Grafo desconectado:** Retornar None y explicar

---

## 6. MEJORAS POTENCIALES Y LIMITACIONES

### 6.1 Limitaciones Actuales

| Limitación | Impacto | Solución |
|-----------|--------|----------|
| Grafo dirigido | No hay caminos de retorno automáticos | Pedir ambas direcciones en carga |
| Sin pesos negativos | Dijkstra sería incorrecto | Usar Bellman-Ford si necesario |
| Sin caching de rutas | Recalcula cada vez | Memoización O(V²) espacio |
| Conexiones duplicadas rechazadas | Solo una ruta por par | Mantener lista de alternativas |
| Sin límite de complejidad | Puede lentarse con V,E muy grandes | Implementar parada anticipada BFS |

### 6.2 Mejoras Implementables

**Corto Plazo:**
1. **Crear índices de estaciones:** Dict[str, int] para matriz de distancias precalculada
   - Costo: O(V²) espacio
   - Beneficio: Dijkstra → O(V²) y evita heap

2. **Caché de rutas:** Dict[(start, end), (distancia, ruta)]
   - Beneficio: Consultas repetidas O(1)
   - Invalidación: al añadir conexiones

3. **Floyd-Warshall precalculado:** Todos vs todos
   - Costo: O(V³) tiempo, O(V²) espacio
   - Beneficio: Cualquier consulta O(1) después
   - Aplicable si V < 1000 (típico en ciudades)

**Largo Plazo:**
4. **Algoritmo A*:** Usar heurística (distancia Manhattan entre estaciones)
   - Mejora Dijkstra si hay heurística admisible
   - Tiempo: O((V + E) log V) pero mejor constante

5. **Grafo bipartito para búsqueda:** Horizonte temporal en dos capas
   - Modelo realista: misma estación a diferentes horas

6. **Análisis de comunidades:** Detectar clusters de estaciones
   - Algoritmo: Louvain o Label Propagation
   - Aplicación: Recomendaciones de rutas

### 6.3 Optimizaciones por Escala

**Red pequeña (< 100 estaciones):**
- Implementación actual es óptima
- Floyd-Warshall si muchas consultas

**Red mediana (100-10k estaciones):**
- Dijkstra actual es excelente
- Considerar A* si geometría disponible
- Caché local de rutas frecuentes

**Red grande (> 10k estaciones, ej. Google Maps):**
- Contracción jerárquica (Hub Labels)
- Procesamiento distribuido (Spark)
- Índices espaciales (R-tree)

---

## 7. RESUMEN DE COMPLEJIDADES

### Operaciones Principales

```
add_station:              O(1)
add_connection:           O(grado) ≈ O(1)
dijkstra:                 O((V + E) · log V)  ← Crítico
are_connected_bfs/dfs:    O(V + E)
find_hub_station:         O(V)
load_network:             O(E)
save_network:             O(V + E)
```

### Complejidad Combinada

- **Caso típico:** Crear red (O(E)) → n consultas Dijkstra: **O(E + n·(V+E)·log V)**
- **Con Floyd-Warshall:** Crear (O(E)) → precálculo (O(V³)) → n consultas (O(n)): **O(E + V³ + n)**

---

## 8. CONCLUSIONES

### Fortalezas del Diseño

✓ **Estructura eficiente:** Lista adyacencia es óptima para grafos dispersos típicos
✓ **Algoritmo correcto:** Dijkstra garantiza solución óptima con O((V+E)log V)
✓ **Validación robusta:** Detecta errores sin fallos silenciosos
✓ **Escalable:** Opera bien de 10 a 10,000 estaciones sin cambios
✓ **Extensible:** Bonus features sin romper core

### Debilidades Conocidas

⚠ No precalcula todas las rutas (OK para consultas esporádicas)
⚠ No optimiza con geometría (OK sin coordenadas GPS)
⚠ Grafo dirigido requiere ambas direcciones explícitamente (intencional)
⚠ Sin caché: consultas iguales no reutilizan (podría añadirse)

### Recomendación Final

**Uso en Producción:**
- Para sistema pequeño/mediano: Implementación actual es **production-ready**
- Para sistema grande: Considerar **Floyd-Warshall** precalculado o **A***
- Para escala Google: Requeriría técnicas especializadas (hierarchical)

