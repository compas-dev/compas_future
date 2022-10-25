from math import pi
from compas_future.colors import Color
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.curves.hyperbola import Hyperbola
from compas_future.viewer import Viewer

from compas.geometry import Polyline
from compas.utilities import linspace

frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
hyperbola = Hyperbola(frame, 1, 1)

viewer = Viewer()

viewer.add(
    Polyline([hyperbola.point_at(t) for t in linspace(0.00000 * pi, 0.5 * pi, 1000)])
)
viewer.add(
    Polyline([hyperbola.point_at(t) for t in linspace(0.50001 * pi, 1.0 * pi, 1000)])
)
viewer.add(
    Polyline([hyperbola.point_at(t) for t in linspace(1.00001 * pi, 1.5 * pi, 1000)])
)
viewer.add(
    Polyline([hyperbola.point_at(t) for t in linspace(1.50001 * pi, 2.0 * pi, 1000)])
)

viewer.run()
