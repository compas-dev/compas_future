from compas_view2.objects import Object
from compas_view2.objects import VectorObject
from compas_view2.objects import PointObject
from compas_view2.objects import LineObject
from compas_view2.objects import CircleObject
from compas_view2.objects import EllipseObject

from compas_future.geometry.vector import Vector
from compas_future.geometry.point import Point

from compas_future.geometry.curves.circle import Circle
from compas_future.geometry.curves.ellipse import Ellipse
from compas_future.geometry.curves.line import Line


Object.register(Vector, VectorObject)
Object.register(Point, PointObject)
Object.register(Line, LineObject)
Object.register(Circle, CircleObject)
Object.register(Ellipse, EllipseObject)
