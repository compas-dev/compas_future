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
    Polyline(
        [
            hyperbola.point_at(t)
            for t in linspace(hyperbola.domain[0], hyperbola.domain[1], 1000)
        ]
    )
)

viewer.run()
