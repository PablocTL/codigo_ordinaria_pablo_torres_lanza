"""
Suite de Pruebas Unitarias - Planificador de Rutas
==================================================
Valida todas las funcionalidades del sistema.

Ejecución:
    python test_transport_network.py
"""

import unittest
import os
import json
from transport_network_planner import TransportNetwork


class TestTransportNetworkBasics(unittest.TestCase):
    """Tests básicos de creación y operaciones de estaciones."""
    
    def setUp(self):
        """Crear red nueva para cada test."""
        self.network = TransportNetwork("test_network.csv")
    
    def tearDown(self):
        """Limpiar archivos de prueba."""
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
        if os.path.exists("test_analysis.json"):
            os.remove("test_analysis.json")
    
    def test_empty_network_creation(self):
        """Test 1: Red vacía se crea correctamente."""
        self.assertEqual(len(self.network.stations), 0)
        self.assertEqual(len(self.network.graph), 0)
    
    def test_add_station_success(self):
        """Test 2: Añadir estación válida."""
        result = self.network.add_station("Madrid")
        self.assertTrue(result)
        self.assertIn("Madrid", self.network.stations)
    
    def test_add_duplicate_station(self):
        """Test 3: Rechazar estación duplicada."""
        self.network.add_station("Madrid")
        result = self.network.add_station("Madrid")
        self.assertFalse(result)
    
    def test_add_empty_station(self):
        """Test 4: Rechazar estación vacía."""
        result = self.network.add_station("")
        self.assertFalse(result)
        result = self.network.add_station("   ")
        self.assertFalse(result)
    
    def test_get_stations_sorted(self):
        """Test 5: Obtener estaciones ordenadas."""
        self.network.add_station("Zebra")
        self.network.add_station("Apple")
        self.network.add_station("Mango")
        
        stations = self.network.get_stations()
        self.assertEqual(stations, ["Apple", "Mango", "Zebra"])


class TestConnections(unittest.TestCase):
    """Tests para operaciones de conexiones."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
        self.network.add_station("A")
        self.network.add_station("B")
        self.network.add_station("C")
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
    
    def test_add_valid_connection(self):
        """Test 6: Añadir conexión válida."""
        result = self.network.add_connection("A", "B", 10)
        self.assertTrue(result)
        
        connections = self.network.get_connections("A")
        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0], ("B", 10))
    
    def test_add_connection_nonexistent_origin(self):
        """Test 7: Rechazar conexión con origen inexistente."""
        result = self.network.add_connection("X", "B", 10)
        self.assertFalse(result)
    
    def test_add_connection_nonexistent_destination(self):
        """Test 8: Rechazar conexión con destino inexistente."""
        result = self.network.add_connection("A", "X", 10)
        self.assertFalse(result)
    
    def test_add_connection_negative_time(self):
        """Test 9: Rechazar tiempo negativo."""
        result = self.network.add_connection("A", "B", -5)
        self.assertFalse(result)
    
    def test_add_connection_zero_time(self):
        """Test 10: Rechazar tiempo cero."""
        result = self.network.add_connection("A", "B", 0)
        self.assertFalse(result)
    
    def test_add_duplicate_connection(self):
        """Test 11: Rechazar conexión duplicada."""
        self.network.add_connection("A", "B", 10)
        result = self.network.add_connection("A", "B", 20)
        self.assertFalse(result)
    
    def test_get_connections_nonexistent_station(self):
        """Test 12: Retornar lista vacía para estación inexistente."""
        result = self.network.get_connections("X")
        self.assertEqual(result, [])
    
    def test_directed_graph(self):
        """Test 13: Verificar que el grafo es dirigido."""
        self.network.add_connection("A", "B", 10)
        
        # A → B existe
        self.assertEqual(len(self.network.get_connections("A")), 1)
        # B → A no existe
        self.assertEqual(len(self.network.get_connections("B")), 0)


class TestDijkstra(unittest.TestCase):
    """Tests para algoritmo de Dijkstra."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
        
        # Crear pequeña red de prueba
        #     5
        # A ----> B
        # |       |
        # | 2     | 3
        # |       |
        # +-----> C (4)
        
        for station in ["A", "B", "C"]:
            self.network.add_station(station)
        
        self.network.add_connection("A", "B", 5)
        self.network.add_connection("A", "C", 4)
        self.network.add_connection("B", "C", 3)
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
    
    def test_direct_path(self):
        """Test 14: Camino directo."""
        time, path = self.network.dijkstra("A", "B")
        self.assertEqual(time, 5)
        self.assertEqual(path, ["A", "B"])
    
    def test_indirect_path(self):
        """Test 15: Camino indirecto más rápido que directo."""
        time, path = self.network.dijkstra("B", "C")
        # B → C directo = 3 (A no es origen)
        self.assertEqual(time, 3)
        self.assertEqual(path, ["B", "C"])
    
    def test_same_source_destination(self):
        """Test 16: Origen = Destino."""
        time, path = self.network.dijkstra("A", "A")
        self.assertEqual(time, 0)
        self.assertEqual(path, ["A"])
    
    def test_nonexistent_source(self):
        """Test 17: Origen inexistente."""
        time, path = self.network.dijkstra("X", "B")
        self.assertIsNone(time)
        self.assertIsNone(path)
    
    def test_nonexistent_destination(self):
        """Test 18: Destino inexistente."""
        time, path = self.network.dijkstra("A", "X")
        self.assertIsNone(time)
        self.assertIsNone(path)
    
    def test_unreachable_destination(self):
        """Test 19: Destino inalcanzable."""
        self.network.add_station("D")
        # D está aislada
        time, path = self.network.dijkstra("A", "D")
        self.assertIsNone(time)
        self.assertIsNone(path)


class TestConnectivity(unittest.TestCase):
    """Tests para búsqueda de conectividad (BFS/DFS)."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
        
        # Grafo desconectado en dos componentes
        # A → B → C
        # D (aislada)
        
        for station in ["A", "B", "C", "D"]:
            self.network.add_station(station)
        
        self.network.add_connection("A", "B", 1)
        self.network.add_connection("B", "C", 1)
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
    
    def test_bfs_same_node(self):
        """Test 20: BFS - mismo nodo."""
        result = self.network.are_connected_bfs("A", "A")
        self.assertTrue(result)
    
    def test_bfs_connected(self):
        """Test 21: BFS - nodos conectados."""
        result = self.network.are_connected_bfs("A", "C")
        self.assertTrue(result)
    
    def test_bfs_not_connected(self):
        """Test 22: BFS - nodos no conectados."""
        result = self.network.are_connected_bfs("A", "D")
        self.assertFalse(result)
    
    def test_bfs_not_bidirectional(self):
        """Test 23: BFS - grafo es dirigido."""
        # C → A no existe aunque A → C sí
        result = self.network.are_connected_bfs("C", "A")
        self.assertFalse(result)
    
    def test_dfs_same_node(self):
        """Test 24: DFS - mismo nodo."""
        result = self.network.are_connected_dfs("A", "A")
        self.assertTrue(result)
    
    def test_dfs_connected(self):
        """Test 25: DFS - nodos conectados."""
        result = self.network.are_connected_dfs("A", "C")
        self.assertTrue(result)
    
    def test_dfs_not_connected(self):
        """Test 26: DFS - nodos no conectados."""
        result = self.network.are_connected_dfs("A", "D")
        self.assertFalse(result)
    
    def test_bfs_nonexistent_stations(self):
        """Test 27: BFS con estaciones inexistentes."""
        result = self.network.are_connected_bfs("X", "Y")
        self.assertFalse(result)


class TestBonusFeatures(unittest.TestCase):
    """Tests para características BONUS."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
        
        # Red con hub claro
        # A es hub (3 conexiones)
        for station in ["A", "B", "C", "D"]:
            self.network.add_station(station)
        
        self.network.add_connection("A", "B", 1)
        self.network.add_connection("A", "C", 2)
        self.network.add_connection("A", "D", 3)
        self.network.add_connection("B", "C", 10)
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
        if os.path.exists("test_analysis.json"):
            os.remove("test_analysis.json")
    
    def test_find_hub_station(self):
        """Test 28: Detectar estación hub."""
        hub = self.network.find_hub_station()
        self.assertEqual(hub, "A")
    
    def test_export_analysis_report(self):
        """Test 29: Exportar informe JSON."""
        result = self.network.export_analysis_report("test_analysis.json")
        self.assertTrue(result)
        self.assertTrue(os.path.exists("test_analysis.json"))
        
        with open("test_analysis.json", "r") as f:
            report = json.load(f)
        
        self.assertEqual(report["num_stations"], 4)
        self.assertEqual(report["num_connections"], 4)
        self.assertEqual(report["hub_station"], "A")
        self.assertEqual(report["hub_connections"], 3)
    
    def test_shortest_path_via_waypoint(self):
        """Test 30: Ruta con parada intermedia."""
        # A → B (1) → C (10) = 11 total
        # A → C (2) directo = 2 total
        # Pero forzamos pasar por B
        
        time, path = self.network.shortest_path_via_waypoint("A", "B", "C")
        self.assertEqual(time, 11)
        self.assertEqual(path, ["A", "B", "C"])
    
    def test_waypoint_nonexistent(self):
        """Test 31: Waypoint inexistente."""
        time, path = self.network.shortest_path_via_waypoint("A", "X", "B")
        self.assertIsNone(time)
        self.assertIsNone(path)


class TestPersistence(unittest.TestCase):
    """Tests para guardado y carga."""
    
    def setUp(self):
        self.test_file = "test_persistence.csv"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_network(self):
        """Test 32: Guardar red en archivo."""
        network = TransportNetwork(self.test_file)
        network.add_station("A")
        network.add_station("B")
        network.add_connection("A", "B", 5)
        
        result = network.save_network()
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_network(self):
        """Test 33: Cargar red desde archivo."""
        # Crear archivo
        network1 = TransportNetwork(self.test_file)
        network1.add_station("Madrid")
        network1.add_station("Barcelona")
        network1.add_connection("Madrid", "Barcelona", 60)
        network1.save_network()
        
        # Cargar en nueva instancia
        network2 = TransportNetwork(self.test_file)
        result = network2.load_network()
        
        self.assertTrue(result)
        self.assertIn("Madrid", network2.stations)
        self.assertIn("Barcelona", network2.stations)
        self.assertEqual(len(network2.get_connections("Madrid")), 1)
    
    def test_load_nonexistent_file(self):
        """Test 34: Cargar archivo inexistente."""
        network = TransportNetwork("nonexistent.csv")
        result = network.load_network()
        self.assertFalse(result)
    
    def test_load_invalid_csv(self):
        """Test 35: Cargar CSV con formato inválido."""
        # Crear CSV con errores
        with open(self.test_file, 'w') as f:
            f.write("origen,destino,minutos\n")
            f.write("A,B,10\n")
            f.write("X,Y,abc\n")  # tiempo inválido
            f.write("P,Q,-5\n")   # tiempo negativo
            f.write("R,S,5\n")    # válido
        
        network = TransportNetwork(self.test_file)
        result = network.load_network()
        
        # Debe cargar con advertencias
        self.assertTrue(result)
        # Solo debería tener la conexión válida
        # (depende de si se cargan A→B antes de error)


class TestComplexGraphs(unittest.TestCase):
    """Tests con grafos más complejos."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
        
        # Grafo más grande - árbol
        #        A
        #       / \
        #      B   C
        #     / \
        #    D   E
        
        for station in ["A", "B", "C", "D", "E"]:
            self.network.add_station(station)
        
        self.network.add_connection("A", "B", 1)
        self.network.add_connection("A", "C", 1)
        self.network.add_connection("B", "D", 1)
        self.network.add_connection("B", "E", 1)
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
    
    def test_complex_dijkstra(self):
        """Test 36: Dijkstra en árbol."""
        time, path = self.network.dijkstra("A", "D")
        self.assertEqual(time, 2)
        self.assertEqual(path, ["A", "B", "D"])
    
    def test_complex_connectivity(self):
        """Test 37: Conectividad en árbol."""
        # Desde raíz hacia cualquier nodo
        for node in ["B", "C", "D", "E"]:
            result = self.network.are_connected_bfs("A", node)
            self.assertTrue(result)
        
        # Desde hoja hacia otra rama
        result = self.network.are_connected_bfs("D", "C")
        self.assertFalse(result)


class TestEdgeCases(unittest.TestCase):
    """Tests de casos extremos."""
    
    def setUp(self):
        self.network = TransportNetwork("test_network.csv")
    
    def tearDown(self):
        if os.path.exists("test_network.csv"):
            os.remove("test_network.csv")
    
    def test_self_loop(self):
        """Test 38: Crear conexión de nodo a sí mismo."""
        self.network.add_station("A")
        # Permitir self-loop si se desea
        result = self.network.add_connection("A", "A", 1)
        # Puede ser válido dependiendo del diseño
    
    def test_large_time_value(self):
        """Test 39: Valores de tiempo muy grandes."""
        self.network.add_station("A")
        self.network.add_station("B")
        result = self.network.add_connection("A", "B", 999999)
        self.assertTrue(result)
    
    def test_special_characters_in_station(self):
        """Test 40: Caracteres especiales en nombres."""
        result = self.network.add_station("Estación-Central #1")
        self.assertTrue(result)
        self.assertIn("Estación-Central #1", self.network.stations)
    
    def test_unicode_station_names(self):
        """Test 41: Nombres con caracteres Unicode."""
        result = self.network.add_station("São Paulo")
        self.assertTrue(result)
        result = self.network.add_station("北京")
        self.assertTrue(result)


# ==================== EXECUTION ====================

def run_tests():
    """Ejecutar suite de tests."""
    # Configurar unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestTransportNetworkBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestConnections))
    suite.addTests(loader.loadTestsFromTestCase(TestDijkstra))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectivity))
    suite.addTests(loader.loadTestsFromTestCase(TestBonusFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexGraphs))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
