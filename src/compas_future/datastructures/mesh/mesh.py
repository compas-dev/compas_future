from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Polygon
from compas.geometry import Plane
from compas.geometry import Frame

from compas.datastructures import Mesh as _Mesh


class Mesh(_Mesh):
    """
    Future implementation of the COMPAS mesh data structure.
    """

    def vertex_point(self, vertex):
        x, y, z = self.vertex_attributes(vertex, "xyz")
        return Point(x, y, z)

    def set_vertex_point(self, vertex, point):
        self.vertex_attributes(vertex, "xyz", point)

    def vertex_normal(self, vertex):
        x, y, z = super(Mesh, self).vertex_normal(vertex)
        return Vector(x, y, z)

    def edge_vector(self, edge):
        x, y, z = super(Mesh, self).edge_vector(*edge)
        return Vector(x, y, z)

    def edge_direction(self, edge):
        x, y, z = super(Mesh, self).edge_vector(*edge)
        return Vector(x, y, z).unitized()

    def edge_start(self, edge):
        return self.vertex_point(edge[0])

    def edge_end(self, edge):
        return self.vertex_point(edge[1])

    def edge_line(self, edge):
        a, b = self.vertices_attributes("xyz", keys=edge)
        return Line(a, b)

    def face_polygon(self, face):
        points = self.face_coordinates(face)
        return Polygon(points)

    def face_centroid(self, face):
        x, y, z = super(Mesh, self).face_centroid(face)
        return Point(x, y, z)

    def face_normal(self, face, unitized=True):
        x, y, z = super(Mesh, self).face_normal(face, unitized=unitized)
        return Vector(x, y, z)

    def face_plane(self, face):
        return Plane(self.face_centroid(face), self.face_normal(face))

    def face_frame(self, face):
        # vectors = [self.edge_vector(edge) for edge in self.face_halfedge(face)]
        # vectors = sorted(vectors, key=lambda v: v.length)
        # xaxis = vectors[-1]
        # yaxis = self.face_normal(face).cross(xaxis)
        # # the above two vectors are not necessarily orthogonal to the normal of the face
        return Frame.from_plane(self.face_plane(face))

    def halfedge_loop_vertices(self, edge):
        loop = self.halfedge_loop(edge)
        return [loop[0][0]] + [edge[1] for edge in loop]

    def halfedge_strip_faces(self, edge):
        strip = self.halfedge_strip(edge)
        return [self.halfedge_face(u, v) for u, v in strip]
