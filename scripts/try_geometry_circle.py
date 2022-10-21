from compas_future.colors import Color
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.curves.circle import Circle
from compas_future.viewer import Viewer

frame = Frame([0, 0, 0], [1, 1, 0], [-1, 1, -1])
circle = Circle(frame, 3.0)

center = circle.point
point = circle.point_at(0)
normal = circle.normal_at(0)
tangent = circle.tangent_at(0)

viewer = Viewer()

viewer.add(circle, u=64)
viewer.add(center)
viewer.add(Line(center, center + circle.normal), linewidth=3)
viewer.add(point)
viewer.add(Line(point, point + normal), linewidth=3, linecolor=Color.red())
viewer.add(Line(point, point + tangent), linewidth=3, linecolor=Color.green())
viewer.add(Line(point, point + circle.normal), linewidth=3, linecolor=Color.blue())

viewer.run()
