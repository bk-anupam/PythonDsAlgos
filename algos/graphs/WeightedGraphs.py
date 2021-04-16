import abc
from algos.graphs.WeightedEdge import WeightedEdge


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
        file_path = file_name
        data_file = open(file_path, "r")
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


class UndirectedEWG(EdgeWeightedGraph):
    def __init__(self, args):
        super().__init__(args)

    def add_edge(self, weighted_edge):
        u = weighted_edge.source
        v = weighted_edge.destination(u)
        if u not in self._adj_list:
            self._adj_list[u] = []
        if v not in self._adj_list:
            self._adj_list[v] = []
        self._adj_list[u].append(weighted_edge)
        self._adj_list[v].append(weighted_edge)
        self._all_edges.add(weighted_edge)

    def __repr__(self):
        for key in self._adj_list.keys():
            val = self._adj_list.get(key)
            print(str(key) + ":")
            for item in val:
                print("\t{}".format(item))

    @property
    def vertices(self):
        return [*self._adj_list]


class DirectedEWG(EdgeWeightedGraph):
    def __init__(self, args):
        super().__init__(args)

    def add_edge(self, weighted_edge):
        if weighted_edge.source not in self._adj_list:
            self._adj_list[weighted_edge.source] = []
        self._adj_list[weighted_edge.source].append(weighted_edge)
        self._all_edges.add(weighted_edge)

    @property
    def vertices(self):
        if len(self._all_vertices) == 0:
            self._all_vertices.update(self._adj_list.keys())
            sink_vertices = [value.destination(key)
                             for key in self._all_vertices
                             for value in self._adj_list[key] if value.destination(key) not in self._all_vertices]
            self._all_vertices.update(sink_vertices)
        # for vertex in all_vertices:
        #     for out_edge in self._adj_list[vertex]:
        #         if out_edge.destination not in all_vertices:
        #             all_vertices.add(out_edge.destination)
        return self._all_vertices