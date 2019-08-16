import abc
import sys
from src.algorithms.graphs.WeightedEdge import WeightedEdge
from src.algorithms.graphs.PrimMST import PrimMST


class EdgeWeightedGraph(abc.ABC):
    """ Abstract base class representing a graph data type"""
    def __init__(self, file_name):
        self._adj_list = {}
        self._all_edges = set()
        self._num_vertices = 0
        self._parse_file_load_graph(file_name)

    @abc.abstractmethod
    def _parse_file_load_graph(self, file_name):
        pass

    def get_out_edges(self, vertex):
        return self._adj_list[vertex]

    @abc.abstractmethod
    def add_edge(self):
        pass

    @abc.abstractmethod
    def vertices(self):
        pass

    @abc.abstractmethod
    def get_all_edges(self):
        pass

    @abc.abstractmethod
    def get_num_edges(self):
        pass

    @abc.abstractmethod
    def get_num_vertices(self):
        pass


class UndirectedEWG(EdgeWeightedGraph):
    def __init__(self, file_name):
        super().__init__(file_name)

    def _parse_file_load_graph(self, file_name):
        #dir_path = os.path.dirname(os.path.abspath(file_name))
        #file_path = dir_path + "\\data\\" + file_name
        data_file = open(file_name, "r")
        counter = 0
        for line in data_file:
            line = line.strip("\n")
            if counter > 1:
                str_array = line.split(" ")
                weighted_edge = WeightedEdge(int(str_array[0]), int(str_array[1]), float(str_array[2]))
                self.add_edge(weighted_edge)

            counter = counter + 1

    def add_edge(self, weighted_edge):
        u = weighted_edge.either
        v = weighted_edge.other(u)

        if u not in self._adj_list:
            self._adj_list[u] = []
        if v not in self._adj_list:
            self._adj_list[v] = []

        self._adj_list[u].append(weighted_edge)
        self._adj_list[v].append(weighted_edge)
        self._all_edges.add(weighted_edge)

    @property
    def vertices(self):
        return [*self._adj_list]

    def get_all_edges(self):
        if len(self._all_edges) == 0:
            for key, value in self._adj_list.items():
                [self._all_edges.add(edge) for edge in value]

        return self._all_edges

    def get_num_edges(self):
        return len(self.get_all_edges())

    def get_num_vertices(self):
        return len(self.vertices)


def main():
    ewg = UndirectedEWG(sys.argv[1])
    prim_mst = PrimMST(ewg)
    for edge in prim_mst.edge_to:
        print(edge)
    print("No of vertices: " + str(ewg.get_num_vertices()))
    print("No of edges: " + str(ewg.get_num_edges()))


if __name__ == "__main__":
    main()