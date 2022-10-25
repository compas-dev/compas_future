from compas_future.colors import Color
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.curves.ellipse import Ellipse
from compas_future.viewer import Viewer

from compas.geometry import Polyline
from compas.utilities import linspace

frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
ellipse = Ellipse(frame, 3.0, 2.0)

center = ellipse.point
point = ellipse.point_at(0.2, normalized=True)
normal = ellipse.normal_at(0.2, normalized=True)
tangent = ellipse.tangent_at(0.2, normalized=True)

viewer = Viewer()

viewer.add(
    Polyline(
        [
            ellipse.point_at(t)
            for t in linspace(ellipse.domain[0], ellipse.domain[1], 1000)
        ]
    )
)

viewer.add(center)
viewer.add(Line(center, center + ellipse.normal), linewidth=3)

viewer.add(point)
viewer.add(Line(point, point + tangent), linewidth=3, linecolor=Color.red())
viewer.add(Line(point, point + normal), linewidth=3, linecolor=Color.green())
viewer.add(Line(point, point + ellipse.normal), linewidth=3, linecolor=Color.blue())

viewer.add(ellipse.focus1)
viewer.add(ellipse.directix1)

viewer.run()
