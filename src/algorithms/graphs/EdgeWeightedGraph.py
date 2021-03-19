from src.algorithms.graphs.Graph import EdgeWeightedGraph
from src.algorithms.graphs.WeightedEdge import WeightedEdge
import heapq
import src.algorithms.graphs.Graph as graph
import sys


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


class DijkstraSP:
    def __init__(self, ewg, source_vertex):
        self._source_vertex = source_vertex
        self._ewg = ewg
        self.__visited_vertices = []
        # this is the dijkstra's greedy score where the index is the vertex and the value is the sum of the weights
        # of edges of the shortest path to this vertex from the source vertex
        self.distTo = [None] * ewg.get_num_vertices()
        # the index is a vertex and value is a min weight directed edge (crossing edge) that leads to this vertex
        self.edgeTo = [None] * ewg.get_num_vertices()
        # priority queue holding all the unexplored vertices of the graph with key being the min weight of the
        # crossing edge leading to this vertex. If there is no crossing edge that leads to the vertex the
        # key or min weight for the vertex is taken as positive infinity
        self.__unexplored_vertex_pq = []
        self.__initialize_pq()
        self.distTo[source_vertex] = 0.0
        self.__visit(source_vertex)
        while len(self.__visited_vertices) != ewg.get_num_vertices():
            min_weight_vertex = heapq.heappop(self.__unexplored_vertex_pq)
            self.__visit(min_weight_vertex.source)

    def __initialize_pq(self):
        for vertex in self._ewg.vertices:
            if vertex != self._source_vertex:
                heapq.heappush(self.__unexplored_vertex_pq, WeightedEdge(vertex, -1, float('inf')))
                self.distTo[vertex] = float('inf')

    def __visit(self, vertex):
        self.__visited_vertices.append(vertex)
        for visited_vertex in self.__visited_vertices:
            for crossing_edge in [edge for edge in self._ewg.get_out_edges(visited_vertex)
                                  if graph.is_directed_crossing_edge(edge.source, edge.destination,
                                                                     self.__visited_vertices)]:
                destination_vertex = crossing_edge.destination(visited_vertex)
                vertex_new_cost = self.distTo[crossing_edge.source] + crossing_edge.weight
                if self.distTo[destination_vertex] > vertex_new_cost:
                    heapq.heappush(self.__unexplored_vertex_pq, WeightedEdge(destination_vertex, -1, vertex_new_cost))
                    self.distTo[destination_vertex] = vertex_new_cost
                    self.edgeTo[destination_vertex] = crossing_edge

    def has_path_to(self, vertex):
        return True if vertex in self.__visited_vertices else False

    def path_to(self, vertex):
        path = []
        while vertex != self._source_vertex:
            edge_to_vertex = self.edgeTo[vertex]
            path.append(edge_to_vertex)
            vertex = edge_to_vertex.source
        return path

    def shortest_path_cost(self, vertex):
        return self.distTo[vertex]


def main():
    args = sys.argv[1]
    directed_ewg = DirectedEWG(args)
    dijkstra_sp = DijkstraSP(directed_ewg, 0)
    print('completed')


if __name__ == "__main__":
    main()
