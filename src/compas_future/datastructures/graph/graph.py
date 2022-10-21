from compas.geometry import Point
from compas.geometry import Line
from compas.datastructures import Graph as _Graph


class Graph(_Graph):
    def node_point(self, node):
        return Point(*self.node_attributes(node, "xyz"))
