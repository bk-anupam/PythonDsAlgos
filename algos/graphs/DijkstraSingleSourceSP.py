from algos.graphs.WeightedEdge import WeightedEdge
from algos.graphs.WeightedGraphs import is_directed_crossing_edge
import heapq


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
                                  if is_directed_crossing_edge(edge.source, edge.destination,
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
        return round(self.distTo[vertex], 2)

    @staticmethod
    def print_spath(path):
        path_str = ""
        # path is treated as a stack
        path.reverse()
        for counter, item in enumerate(path):
            if counter == 0 and len(path) > 1:
                path_str += str(item.source) + "->" + str(item.destination(item.source)) + "->"
            elif counter == 0 and len(path) == 1:
                path_str += str(item.source) + "->" + str(item.destination(item.source))
            elif counter == len(path) - 1:
                path_str += str(item.destination(item.source))
            else:
                path_str += str(item.destination(item.source)) + "->"
        return path_str
