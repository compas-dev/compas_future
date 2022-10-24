from compas_future.colors import Color
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.curves.parabola import Parabola
from compas_future.viewer import Viewer

from compas.geometry import Polyline
from compas.utilities import linspace

frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
parabola = Parabola(frame, 4.0)

parabola.a = 1

point = parabola.point_at(2)
tangent = parabola.tangent_at(2)
normal = parabola.normal_at(2)

viewer = Viewer()

viewer.add(Polyline([parabola.point_at(t) for t in linspace(-5, +5, 1000)]))
viewer.add(parabola.focus)
viewer.add(parabola.vertex)
viewer.add(parabola.directix)
viewer.add(point)
viewer.add(Line(point - tangent * 2, point + tangent * 2))
viewer.add(Line(point - normal * 2, point + normal * 2))

viewer.run()
