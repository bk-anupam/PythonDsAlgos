from functools import total_ordering


@total_ordering
class WeightedEdge:
    """An edge of a edge weighted graph"""
    def __init__(self, first_vertex, second_vertex, weight):
        self.__first_vertex = first_vertex
        self.__second_vertex = second_vertex
        self.weight = weight

    @property
    def source(self):
        return self.__first_vertex

    def destination(self, vertex):
        if self.__first_vertex == vertex:
            return self.__second_vertex
        else:
            return self.__first_vertex

    def __eq__(self, other):
        if not isinstance(other, WeightedEdge):
            return NotImplemented

        return self.__first_vertex == other.__first_vertex \
               and self.__second_vertex == other.__second_vertex \
               and self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __hash__(self):
        return hash((self.__first_vertex, self.__second_vertex, self.weight))

    def __repr__(self):
        return "first_vertex: {}, second_vertex: {}, weight: {}".format(self.__first_vertex,
                                                                        self.__second_vertex, self.weight)
