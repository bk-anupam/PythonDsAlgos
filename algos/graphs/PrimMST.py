import heapq
from algos.graphs.WeightedEdge import WeightedEdge


class PrimMST:
    def __init__(self, ewg):
        self.ewg = ewg
        self.visited_vertices = []
        self.dist_to = [None] * ewg.get_num_vertices()
        self.edge_to = [None] * ewg.get_num_vertices()
        self.__vertex_minweight_pq = []
        self.__initialize_pq()
        while not len(self.visited_vertices) == self.ewg.get_num_vertices():
            min_weight_edge = heapq.heappop(self.__vertex_minweight_pq)
            self.__visit(min_weight_edge)

    def __initialize_pq(self):
        for vertex in self.ewg.vertices:
            if vertex == 0:
                heapq.heappush(self.__vertex_minweight_pq, WeightedEdge(vertex, -1, 0.0))
            else:
                heapq.heappush(self.__vertex_minweight_pq, WeightedEdge(vertex, -1, float('inf')))
                self.dist_to[vertex] = float('inf')
                self.edge_to[vertex] = WeightedEdge(vertex, -1, float('inf'))

    def __visit(self, weighted_edge):
        self.visited_vertices.append(weighted_edge.source)
        for visited_vertex in self.visited_vertices:
            for crossing_edge in [edge for edge in self.ewg.get_out_edges(visited_vertex)
                                  if self.__is_crossing_edge(edge)]:
                other_vertex = crossing_edge.destination(visited_vertex)
                if crossing_edge.weight < self.dist_to[other_vertex]:
                    self.dist_to[other_vertex] = crossing_edge.weight
                    self.edge_to[other_vertex] = crossing_edge
                    # try:
                    #     self.__vertex_minweight_pq.remove(weighted_edge)
                    # except ValueError:
                    #     pass
                    self.__vertex_minweight_pq.append(WeightedEdge(other_vertex, visited_vertex, crossing_edge.weight))
                    heapq.heapify(self.__vertex_minweight_pq)

    def __is_crossing_edge(self, edge):
        u = edge.source
        v = edge.destination(u)
        if u in self.visited_vertices and v in self.visited_vertices:
            return False
        else:
            return True

    @property
    def mst(self):
        return self.edge_to
