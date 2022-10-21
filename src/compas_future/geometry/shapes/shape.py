from compas.geometry import Frame
from ..geometry import Geometry


class Shape(Geometry):
    """
    Base class for all parametric shapes.
    Parametric shapes are defined by parameters with respect to frame or coordinate system.

    Parameters
    ----------
    *args : List[Any]
        The parameters defining the shape.
    frame : :class:`compas.geometry.Frame`, optional
        The coordinate system of the shape.
        Default is the world coordinate system.

    Other Parameters
    ----------------
    **kwargs : Dict
        Other keyword arguments passed on to the parent constructors.

    """

    def __init__(self, *args, frame=None, **kwargs):
        super(Geometry, self).__init__(**kwargs)
        self._frame = None
        self.frame = frame

    @property
    def frame(self):
        if self._frame is None:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value
