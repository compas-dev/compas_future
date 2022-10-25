from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos, sin, sqrt
from math import pi

from compas_future.geometry.vector import Vector
from compas_future.geometry.point import Point
from compas_future.geometry.plane import Plane
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.line import Line
from compas_future.geometry.transformations.transformation import Transformation
from compas_future.geometry.curves.conic import Conic


class Parabola(Conic):
    """
    A parabola is defined by a plane and a major and minor axis.
    The origin of the coordinate frame is the center of the parabola.

    The parabola in this implementation is based on the equation ``y = a * x**2``.
    Therefore it will have the y axis of the coordinate frame as its axis of symmetry.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the parabola.
    major : float
        The major of the parabola.

    Attributes
    ----------
    is_periodic : bool, read-only
        An parabola is periodic (True).
    is_closed : bool, read-only
        An parabola is closed (True).
    domain : tuple[float, float], read-only
        The parameter domain: 0, 2pi
    eccentricity : float, read-only
        The eccentricity of an parabola is between 0 and 1.
    frame : :class:`compas.geometry.Point`
        The coordinate frame of the parabola.
    point : :class:`compas.geometry.Point`
        The center of the parabola.
    focal : float
        The distance between the two focus points.
    latus : :class:`compas.geometry.Point`, read-only
        The latus rectum of the parabola.
    xaxis : :class:`compas.geometry.Vector`, read-only
        The X axis of the frame of the parabola.
    yaxis : :class:`compas.geometry.Vector`, read-only
        The Y axis of the frame of the parabola.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the parabola.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the parabola.
    focus : :class:`compas.geometry.Point`, read-only
        The focus of the parabola.
    directix : :class:`compas.geometry.Line`, read-only
        The directix is the line perpendicular to the y axis of the parabola
        at a distance ``d = + major / eccentricity`` from the center of the parabola.
        The second directix intersects the positive x axis.

    """

    __slots__ = ["_frame", "_focal"]

    def __init__(self, frame, focal, **kwargs):
        super(Parabola, self).__init__(**kwargs)
        self._frame = None
        self._focal = None
        self._transformation = None
        self.frame = frame or Frame.worldXY()
        self.focal = focal

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema

        return schema.Schema(
            {
                "frame": Frame,
                "focal": float,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "parabola"

    @property
    def data(self):
        """dict : The data dictionary that represents the parabola."""
        return {"frame": self.frame, "focal": self.focal}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.focal = data["focal"]

    @classmethod
    def from_data(cls, data):
        """Construct a parabola from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Parabola`
            The constructed parabola.

        """
        return cls(data["frame"], data["focal"])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def is_periodic(self):
        return False

    @property
    def is_closed(self):
        return False

    @property
    def domain(self):
        return float("-inf"), float("+inf")

    @property
    def eccentricity(self):
        return 1

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
        self._transformation = Transformation.from_frame(frame)

    @property
    def focal(self):
        return self._focal

    @focal.setter
    def focal(self, focal):
        self._focal = focal

    @property
    def latus(self):
        return 2 * self.focal

    @property
    def point(self):
        return self.frame.point

    @point.setter
    def point(self, point):
        self.frame.point = point

    @property
    def xaxis(self):
        return self.frame.xaxis

    @property
    def yaxis(self):
        return self.frame.yaxis

    @property
    def normal(self):
        return self.frame.zaxis

    @property
    def plane(self):
        return Plane(self.point, self.frame.zaxis)

    @property
    def focus(self):
        return self.frame.point + self.yaxis * self.focal

    @property
    def vertex(self):
        return self.frame.point

    @property
    def directix(self):
        point = self.frame.point + self.yaxis * -self.focal
        return Line(point, point + self.xaxis)

    @property
    def a(self):
        return 1 / (4 * self.focal)

    @a.setter
    def a(self, a):
        self.focal = 1 / (4 * a)

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Parabola({0!r}, {1!r})".format(self.frame, self.focal)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.focal
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.focal = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.major, self.minor])

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def point_at(self, t):
        """
        Point at the parameter.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Point`

        """
        x = t
        y = self.a * x**2
        z = 0
        point = Point(x, y, z)
        point.transform(self._transformation)
        return point

    def tangent_at(self, t):
        """
        Tangent vector at the parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        x0 = t
        y0 = self.a * t**2
        x = 2 * t
        y = 2 * self.a * x0 * x - y0
        tangent = Vector(x - x0, y - y0, 0)
        tangent.unitize()
        tangent.transform(self._transformation)
        return tangent

    def normal_at(self, t):
        """
        Normal at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        x0 = t
        y0 = self.a * t**2
        x = 2 * t
        y = 2 * self.a * x0 * x - y0
        normal = Vector(y0 - y, x - x0, 0)
        normal.unitize()
        normal.transform(self._transformation)
        return normal

    def frame_at(self, t):
        """
        Frame at the parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Frame`

        """
        point = self.point_at(t, normalized=False)
        xaxis = self.tangent_at(t, normalized=False)
        yaxis = self.frame.zaxis.cross(xaxis)
        return Frame(point, xaxis, yaxis)
