from compas_future.colors import Color
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.curves.circle import Circle
from compas_future.viewer import Viewer

from compas.geometry import Polyline
from compas.utilities import linspace

frame = Frame([0, 0, 0], [1, 1, 0], [-1, 1, -1])
frame = Frame.worldXY()
circle = Circle(frame, 3.0)

center = circle.point
point = circle.point_at(0.25)
normal = circle.normal_at(0.25)
tangent = circle.tangent_at(0.25)

viewer = Viewer()

viewer.add(
    Polyline(
        [circle.point_at(t) for t in linspace(circle.domain[0], circle.domain[1], 1000)]
    )
)

viewer.add(center)
viewer.add(Line(center, center + circle.normal), linewidth=3)

viewer.add(point)
viewer.add(Line(point, point + tangent), linewidth=3, linecolor=Color.red())
viewer.add(Line(point, point + normal), linewidth=3, linecolor=Color.green())
viewer.add(Line(point, point + circle.normal), linewidth=3, linecolor=Color.blue())

viewer.run()
