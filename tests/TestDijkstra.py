import unittest
from algos.graphs.DijkstraSingleSourceSP import DijkstraSP
from algos.graphs.WeightedGraphs import DirectedEWG


class TestDijkstra(unittest.TestCase):
    def test_dijkstra(self):
        directed_ewg = DirectedEWG("./../data/tinyEWD.txt")
        dijkstra_sp = DijkstraSP(directed_ewg, 0)
        expected_distTo = [0.0, 1.05, 0.26, 0.99, 0.38, 0.73, 1.51, 0.6]
        for vertex in directed_ewg.vertices:
            v_sp_cost = dijkstra_sp.shortest_path_cost(vertex)
            self.assertEqual(v_sp_cost, expected_distTo[vertex])


if __name__ == '__main__':
    unittest.main()