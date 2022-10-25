from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos, sin
from math import pi

from compas_future.geometry.vector import Vector
from compas_future.geometry.point import Point
from compas_future.geometry.frame import Frame
from compas_future.geometry.plane import Plane
from compas_future.geometry.transformations.transformation import Transformation
from compas_future.geometry.curves.conic import Conic


class Circle(Conic):
    """
    A circle is defined by a coordinate frame and a radius.
    The origin of the coordinate frame is the center of the circle.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the circle.
    radius : float
        The radius of the circle.

    Attributes
    ----------
    is_periodic : bool, read-only
        A circle is periodic (True).
    is_closed : bool, read-only
        A circle is closed (True).
    domain : tuple[float, float], read-only
        The parameter domain: 0, 2pi
    eccentricity : float, read-only
        The eccentricity of a circle is 0 (zero).
    frame : :class:`compas.geometry.Point`
        The center of the circle.
    radius : float
        The radius of the circle.
    xaxis : :class:`compas.geometry.Vector`, read-only
        The X axis of the frame of the circle.
    yaxis : :class:`compas.geometry.Vector`, read-only
        The Y axis of the frame of the circle.
    point : :class:`compas.geometry.Point`
        The center of the circle.
    center : :class:`compas.geometry.Point`
        The center of the circle.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the circle.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the circle.
    diameter : float, read-only
        The diameter of the circle.
    area : float, read-only
        The area of the circle.
    circumference : float, read-only
        The circumference of the circle.

    """

    __slots__ = ["_frame", "_radius"]

    def __init__(self, frame, radius, **kwargs):
        super(Circle, self).__init__(**kwargs)
        self._radius = None
        self._frame = None
        self._transformation = None
        self.frame = frame or Frame.worldXY()
        self.radius = radius

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
                "radius": schema.And(float, lambda x: x > 0),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "circle"

    @property
    def data(self):
        """dict : The data dictionary that represents the circle."""
        return {"frame": self.frame, "radius": self.radius}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.radius = data["radius"]

    @classmethod
    def from_data(cls, data):
        """Construct a circle from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        """
        return cls(data["frame"], data["radius"])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def is_periodic(self):
        return True

    @property
    def is_closed(self):
        return True

    @property
    def domain(self):
        return 0, 2 * pi

    @property
    def eccentricity(self):
        return 0

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
        self._transformation = Transformation.from_frame(frame)

    @property
    def point(self):
        return self.frame.point

    @point.setter
    def point(self, point):
        if point:
            self.frame.point = point

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def normal(self):
        return self.frame.zaxis

    @property
    def xaxis(self):
        return self.frame.xaxis

    @property
    def yaxis(self):
        return self.frame.yaxis

    @property
    def start(self):
        return self.point + self.xaxis * self.radius

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return pi * (self.radius**2)

    @property
    def circumference(self):
        return 2 * pi * self.radius

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Circle({0!r}, {1!r})".format(self.frame, self.radius)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius])

    def __eq__(self, other):
        try:
            frame = other[0]
            radius = other[1]
        except:  # noqa: E722
            return False
        return self.frame == frame and self.radius == radius

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def point_at(self, t, normalized=False):
        """
        Point at the parameter.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Point`

        """
        if normalized:
            t = t * 2 * pi
        x = self.radius * cos(t)
        y = self.radius * sin(t)
        z = 0
        point = Point(x, y, z)
        point.transform(self._transformation)
        return point

    def tangent_at(self, t, normalized=False):
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
        if normalized:
            t = t * 2 * pi
        normal = self.normal_at(t, normalized=False)
        tangent = normal.cross(self.frame.zaxis)
        tangent.unitize()
        return tangent

    def normal_at(self, t, normalized=False):
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
        if normalized:
            t = t * 2 * pi
        a = self.point_at(t, normalized=False)
        b = self.point
        normal = b - a
        normal.unitize()
        return normal

    def frame_at(self, t, normalized=False):
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
        if normalized:
            t = t * 2 * pi
        point = self.point_at(t, normalized=False)
        yaxis = self.normal_at(t, normalized=False)
        xaxis = yaxis.cross(self.frame.zaxis)
        return Frame(point, xaxis, yaxis)
