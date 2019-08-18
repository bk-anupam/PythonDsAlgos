import abc
from src.algorithms.graphs.WeightedEdge import WeightedEdge


def is_directed_crossing_edge(source, destination, visited_vertices):
    if source in visited_vertices and destination not in visited_vertices:
        return True
    else:
        return False


class EdgeWeightedGraph(abc.ABC):
    """ Abstract base class representing a graph data type"""
    def __init__(self, args):
        self._adj_list = {}
        self._all_edges = set()
        self._all_vertices = set()
        self._num_vertices = 0
        if isinstance(args, str):
            self.__initialize_fromfile(args)
        elif isinstance(args, int):
            self.__initialize_only_vertices(args)

    def __initialize_fromfile(self, file_name):
        self._parse_file_load_graph(file_name)

    def __initialize_only_vertices(self, vertex_count):
        for vertex in range(vertex_count):
            self._adj_list[vertex] = []

    def _parse_file_load_graph(self, file_name):
        # dir_path = os.path.dirname(os.path.abspath(file_name))
        # file_path = dir_path + "\\data\\" + file_name
        data_file = open(file_name, "r")
        counter = 0
        for line in data_file:
            line = line.strip("\n")
            if counter > 1:
                str_array = line.split(" ")
                weighted_edge = WeightedEdge(int(str_array[0]), int(str_array[1]), float(str_array[2]))
                self.add_edge(weighted_edge)

            counter = counter + 1

    def get_out_edges(self, vertex):
        return self._adj_list[vertex]

    @abc.abstractmethod
    def add_edge(self, weighted_edge):
        pass

    @abc.abstractmethod
    def vertices(self):
        pass

    def get_all_edges(self):
        if len(self._all_edges) == 0:
            all_edges = [value for key, value in self._adj_list.items()
                         for edge in value]
            # for key, value in self._adj_list.items():
            #     [self._all_edges.add(edge) for edge in value]
        self._all_edges.update(all_edges)
        return self._all_edges

    def get_num_edges(self):
        return len(self.get_all_edges())

    def get_num_vertices(self):
        if self._num_vertices == 0:
            self._num_vertices = len(self.vertices)
        return self._num_vertices
