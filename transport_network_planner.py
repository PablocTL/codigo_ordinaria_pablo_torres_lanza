"""
Planificador de Rutas en una Red de Transporte
==============================================
Sistema de gestión de redes de transporte con cálculo de rutas óptimas.

Características:
- Modelado de red como grafo ponderado (tiempo en minutos)
- Algoritmo de Dijkstra para ruta más rápida
- BFS/DFS para comprobar conectividad
- Persistencia en archivos (CSV y JSON)
- Validación exhaustiva de datos
"""

import heapq
import json
import csv
import os
from collections import deque, defaultdict
from typing import Dict, List, Tuple, Optional, Set


class TransportNetwork:
    """
    Clase que representa una red de transporte como un grafo ponderado.
    
    Estructura de datos:
    - graph: Dict[str, List[Tuple[str, int]]] - Lista de adyacencia
      Clave: estación origen
      Valor: lista de tuplas (estación_destino, tiempo_minutos)
    - stations: Set[str] - Conjunto de todas las estaciones
    """
    
    def __init__(self, network_file: str = "transport_network.csv"):
        """
        Inicializa la red de transporte.
        
        Args:
            network_file: Ruta del archivo CSV con la red
        """
        self.graph: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self.stations: Set[str] = set()
        self.network_file = network_file
        
    # ==================== CARGAR Y GUARDAR ====================
    
    def load_network(self) -> bool:
        """
        Carga la red desde un archivo CSV.
        Formato: origen,destino,minutos
        
        Returns:
            bool: True si carga exitosa, False si hay error o archivo no existe
        """
        if not os.path.exists(self.network_file):
            print(f"⚠️  Archivo '{self.network_file}' no encontrado. Iniciando red vacía.")
            return False
        
        try:
            with open(self.network_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Saltar encabezado si existe
                
                for line_num, row in enumerate(reader, start=2):
                    if not row or row[0].startswith('#'):  # Ignorar líneas vacías y comentarios
                        continue
                    
                    if len(row) != 3:
                        print(f"⚠️  Línea {line_num}: formato inválido. Se ignora.")
                        continue
                    
                    origen, destino, tiempo_str = row[0].strip(), row[1].strip(), row[2].strip()
                    
                    # Validar
                    if not origen or not destino:
                        print(f"⚠️  Línea {line_num}: estaciones vacías. Se ignora.")
                        continue
                    
                    try:
                        tiempo = int(tiempo_str)
                        if tiempo <= 0:
                            print(f"⚠️  Línea {line_num}: tiempo debe ser positivo. Se ignora.")
                            continue
                    except ValueError:
                        print(f"⚠️  Línea {line_num}: tiempo '{tiempo_str}' no es número. Se ignora.")
                        continue
                    
                    # Añadir conexión sin validación extra (se permite duplicados en carga inicial)
                    self.graph[origen].append((destino, tiempo))
                    self.stations.add(origen)
                    self.stations.add(destino)
                
                print(f"✓ Red cargada: {len(self.stations)} estaciones, {self._count_edges()} conexiones.")
                return True
                
        except IOError as e:
            print(f"✗ Error al leer archivo: {e}")
            return False
    
    def save_network(self) -> bool:
        """
        Guarda la red en un archivo CSV.
        
        Returns:
            bool: True si guardado exitoso
        """
        try:
            with open(self.network_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['origen', 'destino', 'minutos'])
                
                # Escribir todas las conexiones
                for origen in sorted(self.graph.keys()):
                    for destino, tiempo in self.graph[origen]:
                        writer.writerow([origen, destino, tiempo])
            
            print(f"✓ Red guardada en '{self.network_file}'")
            return True
        except IOError as e:
            print(f"✗ Error al guardar: {e}")
            return False
    
    # ==================== OPERACIONES BÁSICAS ====================
    
    def add_station(self, station_name: str) -> bool:
        """
        Añade una estación a la red.
        
        Args:
            station_name: Nombre de la estación
            
        Returns:
            bool: True si se añadió, False si ya existe
        """
        station_name = station_name.strip()
        
        if not station_name:
            print("✗ El nombre de la estación no puede estar vacío.")
            return False
        
        if station_name in self.stations:
            print(f"✗ La estación '{station_name}' ya existe.")
            return False
        
        self.stations.add(station_name)
        # Inicializar entrada en grafo si no existe
        if station_name not in self.graph:
            self.graph[station_name] = []
        
        print(f"✓ Estación '{station_name}' añadida.")
        return True
    
    def add_connection(self, origin: str, destination: str, time_minutes: int) -> bool:
        """
        Añade una conexión dirigida entre dos estaciones.
        Valida que las estaciones existan, el tiempo sea positivo y sin duplicados.
        
        Complejidad temporal: O(grado_origen) para detectar duplicados
        
        Args:
            origin: Estación de origen
            destination: Estación de destino
            time_minutes: Tiempo de viaje en minutos
            
        Returns:
            bool: True si conexión añadida exitosamente
        """
        origin = origin.strip()
        destination = destination.strip()
        
        # Validaciones
        if origin not in self.stations:
            print(f"✗ La estación origen '{origin}' no existe.")
            return False
        
        if destination not in self.stations:
            print(f"✗ La estación destino '{destination}' no existe.")
            return False
        
        if time_minutes <= 0:
            print(f"✗ El tiempo debe ser positivo (recibido: {time_minutes}).")
            return False
        
        # Verificar duplicados: O(grado del nodo origen)
        for dest, tiempo in self.graph[origin]:
            if dest == destination:
                print(f"✗ Conexión '{origin}' → '{destination}' ya existe ({tiempo} min).")
                return False
        
        # Añadir conexión
        self.graph[origin].append((destination, time_minutes))
        print(f"✓ Conexión añadida: '{origin}' → '{destination}' ({time_minutes} min)")
        return True
    
    def get_stations(self) -> List[str]:
        """
        Retorna lista ordenada de todas las estaciones.
        
        Returns:
            List[str]: Estaciones ordenadas alfabéticamente
        """
        return sorted(self.stations)
    
    def get_connections(self, station: str) -> List[Tuple[str, int]]:
        """
        Retorna todas las conexiones directas de una estación.
        
        Args:
            station: Nombre de la estación
            
        Returns:
            List[Tuple[str, int]]: Lista de (destino, tiempo)
        """
        if station not in self.stations:
            print(f"✗ Estación '{station}' no existe.")
            return []
        
        return self.graph.get(station, [])
    
    # ==================== ALGORITMO DE DIJKSTRA ====================
    
    def dijkstra(self, start: str, end: str) -> Tuple[Optional[int], Optional[List[str]]]:
        """
        Calcula la ruta más rápida (menor tiempo) entre dos estaciones.
        Usa algoritmo de Dijkstra con min-heap para eficiencia.
        
        Complejidad temporal: O((V + E) * log V)
        donde V = número de estaciones, E = número de conexiones
        
        Complejidad espacial: O(V) para distancias y visitados
        
        Args:
            start: Estación de inicio
            end: Estación de destino
            
        Returns:
            Tuple[int, List[str]]: (tiempo_total, [camino] o (None, None) si no hay ruta
        """
        if start not in self.stations:
            print(f"✗ Estación inicio '{start}' no existe.")
            return None, None
        
        if end not in self.stations:
            print(f"✗ Estación destino '{end}' no existe.")
            return None, None
        
        if start == end:
            return 0, [start]
        
        # Inicialización
        distances = {station: float('inf') for station in self.stations}
        distances[start] = 0
        parents = {station: None for station in self.stations}
        visited = set()
        
        # Min-heap: (distancia, estación)
        heap = [(0, start)]
        
        while heap:
            current_distance, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Si llegamos al destino, podemos terminar
            if current == end:
                break
            
            # Relajar aristas
            for neighbor, weight in self.graph[current]:
                if neighbor not in visited:
                    new_distance = current_distance + weight
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parents[neighbor] = current
                        heapq.heappush(heap, (new_distance, neighbor))
        
        # Reconstruir camino si es alcanzable
        if distances[end] == float('inf'):
            return None, None
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        
        return distances[end], path
    
    # ==================== CONECTIVIDAD: BFS/DFS ====================
    
    def are_connected_bfs(self, station_a: str, station_b: str) -> bool:
        """
        Verifica si dos estaciones están conectadas (existe camino).
        Usa BFS (Breadth-First Search).
        
        Complejidad temporal: O(V + E)
        Complejidad espacial: O(V) para cola y visitados
        
        Args:
            station_a: Primera estación
            station_b: Segunda estación
            
        Returns:
            bool: True si existe camino entre ellas
        """
        if station_a not in self.stations or station_b not in self.stations:
            print("✗ Una o ambas estaciones no existen.")
            return False
        
        if station_a == station_b:
            return True
        
        visited: Set[str] = set()
        queue: deque = deque([station_a])
        visited.add(station_a)
        
        while queue:
            current = queue.popleft()
            
            for neighbor, _ in self.graph[current]:
                if neighbor == station_b:
                    return True
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
    
    def are_connected_dfs(self, station_a: str, station_b: str) -> bool:
        """
        Verifica si dos estaciones están conectadas (existe camino).
        Usa DFS (Depth-First Search) - versión iterativa.
        
        Complejidad temporal: O(V + E)
        Complejidad espacial: O(V)
        
        Args:
            station_a: Primera estación
            station_b: Segunda estación
            
        Returns:
            bool: True si existe camino entre ellas
        """
        if station_a not in self.stations or station_b not in self.stations:
            print("✗ Una o ambas estaciones no existen.")
            return False
        
        if station_a == station_b:
            return True
        
        visited: Set[str] = set()
        stack: List[str] = [station_a]
        visited.add(station_a)
        
        while stack:
            current = stack.pop()
            
            for neighbor, _ in self.graph[current]:
                if neighbor == station_b:
                    return True
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        
        return False
    
    # ==================== BONUS: HUB Y ANÁLISIS ====================
    
    def find_hub_station(self) -> Optional[str]:
        """
        Encuentra la estación "hub" (mayor número de conexiones salientes).
        
        Complejidad: O(V)
        
        Returns:
            str: Nombre de la estación hub o None si red vacía
        """
        if not self.graph:
            return None
        
        hub = max(self.graph.keys(), key=lambda s: len(self.graph[s]))
        return hub
    
    def _count_edges(self) -> int:
        """Cuenta el número total de aristas en el grafo."""
        return sum(len(connections) for connections in self.graph.values())
    
    def export_analysis_report(self, filename: str = "network_analysis.json") -> bool:
        """
        Exporta un informe de análisis de la red en JSON.
        Incluye: nº estaciones, nº conexiones, estación hub, y más.
        
        Args:
            filename: Nombre del archivo de salida
            
        Returns:
            bool: True si exportación exitosa
        """
        try:
            hub = self.find_hub_station()
            hub_connections = len(self.graph[hub]) if hub else 0
            
            # Calcular conexiones por estación
            station_degrees = {
                station: len(self.graph[station])
                for station in self.stations
            }
            
            report = {
                "num_stations": len(self.stations),
                "num_connections": self._count_edges(),
                "hub_station": hub,
                "hub_connections": hub_connections,
                "all_stations": sorted(self.stations),
                "station_degrees": dict(sorted(
                    station_degrees.items(),
                    key=lambda x: x[1],
                    reverse=True
                ))
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Informe exportado: '{filename}'")
            return True
        except IOError as e:
            print(f"✗ Error al exportar informe: {e}")
            return False
    
    def shortest_path_via_waypoint(self, start: str, waypoint: str, end: str
                                    ) -> Tuple[Optional[int], Optional[List[str]]]:
        """
        Calcula el camino más rápido que pase obligatoriamente por una estación intermedia.
        
        Estrategia: Dijkstra(start → waypoint) + Dijkstra(waypoint → end)
        
        Complejidad: O(2 * (V + E) * log V) = O((V + E) * log V)
        
        Args:
            start: Estación de inicio
            waypoint: Estación intermedia obligatoria
            end: Estación de destino
            
        Returns:
            Tuple[int, List[str]]: (tiempo_total, camino_completo) o (None, None)
        """
        # Validar existencia
        for station in [start, waypoint, end]:
            if station not in self.stations:
                print(f"✗ Estación '{station}' no existe.")
                return None, None
        
        # Ruta 1: start → waypoint
        time1, path1 = self.dijkstra(start, waypoint)
        if path1 is None:
            print(f"✗ No hay camino de '{start}' a '{waypoint}'.")
            return None, None
        
        # Ruta 2: waypoint → end
        time2, path2 = self.dijkstra(waypoint, end)
        if path2 is None:
            print(f"✗ No hay camino de '{waypoint}' a '{end}'.")
            return None, None
        
        # Combinar rutas (sin duplicar waypoint)
        full_path = path1 + path2[1:]
        total_time = time1 + time2
        
        return total_time, full_path
    
    # ==================== UTILIDADES ====================
    
    def display_network(self):
        """Muestra toda la red de estaciones y conexiones."""
        if not self.stations:
            print("⚠️  La red está vacía.")
            return
        
        print("\n" + "="*70)
        print(f"RED DE TRANSPORTE ({len(self.stations)} estaciones, {self._count_edges()} conexiones)")
        print("="*70)
        
        for station in sorted(self.stations):
            connections = self.graph[station]
            if connections:
                print(f"\n{station}:")
                for dest, time in sorted(connections, key=lambda x: x[1]):
                    print(f"  → {dest:20} ({time:3} min)")
            else:
                print(f"\n{station}: (sin conexiones salientes)")
        
        print("\n" + "="*70 + "\n")
    
    def __str__(self) -> str:
        """Representación en string de la red."""
        return f"TransportNetwork({len(self.stations)} estaciones, {self._count_edges()} conexiones)"


# ==================== INTERFAZ DE USUARIO ====================

def print_menu():
    """Imprime el menú principal."""
    print("\n" + "="*70)
    print("PLANIFICADOR DE RUTAS - MENÚ PRINCIPAL")
    print("="*70)
    print("1. Cargar red desde archivo")
    print("2. Añadir estación")
    print("3. Añadir conexión")
    print("4. Ver estaciones y conexiones")
    print("5. Ruta más rápida entre dos estaciones")
    print("6. ¿Están conectadas dos estaciones?")
    print("7. Ruta con parada intermedia obligatoria (BONUS)")
    print("8. Exportar informe de análisis (BONUS)")
    print("9. Guardar y salir")
    print("="*70)


def main():
    """Función principal con menú interactivo."""
    network = TransportNetwork()
    
    # Intentar cargar red existente
    if os.path.exists("transport_network.csv"):
        network.load_network()
    
    while True:
        print_menu()
        choice = input("Selecciona opción (1-9): ").strip()
        
        try:
            if choice == "1":
                # Cargar red
                filename = input("Nombre del archivo CSV (por defecto: transport_network.csv): ").strip()
                if filename:
                    network.network_file = filename
                network.load_network()
            
            elif choice == "2":
                # Añadir estación
                station = input("Nombre de la estación: ").strip()
                network.add_station(station)
            
            elif choice == "3":
                # Añadir conexión
                network.display_network()
                origin = input("Estación origen: ").strip()
                destination = input("Estación destino: ").strip()
                try:
                    time = int(input("Tiempo (minutos): "))
                    network.add_connection(origin, destination, time)
                except ValueError:
                    print("✗ Tiempo inválido. Introduce un número.")
            
            elif choice == "4":
                # Ver red
                network.display_network()
            
            elif choice == "5":
                # Dijkstra
                network.display_network()
                start = input("Estación de inicio: ").strip()
                end = input("Estación destino: ").strip()
                
                time, path = network.dijkstra(start, end)
                if path:
                    print(f"\n✓ RUTA MÁS RÁPIDA: {' → '.join(path)}")
                    print(f"  Tiempo total: {time} minutos\n")
                else:
                    print(f"\n✗ No hay ruta disponible entre '{start}' y '{end}'.\n")
            
            elif choice == "6":
                # Conectividad
                network.display_network()
                st_a = input("Primera estación: ").strip()
                st_b = input("Segunda estación: ").strip()
                
                # Usar BFS por defecto (más típico en búsquedas)
                connected = network.are_connected_bfs(st_a, st_b)
                
                if connected:
                    print(f"\n✓ Las estaciones '{st_a}' y '{st_b}' ESTÁN conectadas.\n")
                else:
                    print(f"\n✗ Las estaciones '{st_a}' y '{st_b}' NO están conectadas.\n")
            
            elif choice == "7":
                # BONUS: Ruta con waypoint
                network.display_network()
                start = input("Estación de inicio: ").strip()
                waypoint = input("Estación intermedia (obligatoria): ").strip()
                end = input("Estación destino: ").strip()
                
                time, path = network.shortest_path_via_waypoint(start, waypoint, end)
                if path:
                    print(f"\n✓ RUTA CON PARADA OBLIGATORIA: {' → '.join(path)}")
                    print(f"  Tiempo total: {time} minutos\n")
                else:
                    print(f"\n✗ No hay ruta válida con la parada intermedia.\n")
            
            elif choice == "8":
                # BONUS: Exportar informe
                filename = input("Nombre del informe (por defecto: network_analysis.json): ").strip()
                if not filename:
                    filename = "network_analysis.json"
                network.export_analysis_report(filename)
            
            elif choice == "9":
                # Guardar y salir
                save = input("¿Guardar cambios? (s/n): ").strip().lower()
                if save == 's':
                    network.save_network()
                print("¡Hasta luego!")
                break
            
            else:
                print("✗ Opción no válida.")
        
        except KeyboardInterrupt:
            print("\n\n✗ Operación cancelada.")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")


if __name__ == "__main__":
    main()
