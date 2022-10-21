from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_future.geometry.vector import Vector
from compas_future.geometry.point import Point
from compas_future.geometry.frame import Frame
from compas_future.geometry.curves.curve import Curve


class Line(Curve):
    """
    A line is defined by two points.

    Parameters
    ----------
    p1 : [float, float, float] | :class:`compas.geometry.Point`
        The first point.
    p2 : [float, float, float] | :class:`compas.geometry.Point`
        The second point.

    Attributes
    ----------
    start : :class:`compas.geometry.Point`
        The start point of the line.
    end : :class:`compas.geometry.Point`
        The end point of the line.
    vector : :class:`compas.geometry.Vector`, read-only
        A vector pointing from start to end.
    length : float, read-only
        The length of the vector from start to end.
    direction : :class:`compas.geometry.Vector`, read-only
        A unit vector pointing from start and end.
    midpoint : :class:`compas.geometry.Point`, read-only
        The midpoint between start and end.

    Examples
    --------
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> line
    Line(Point(0.000, 0.000, 0.000), Point(1.000, 1.000, 1.000))
    >>> line.start
    Point(0.000, 0.000, 0.000)
    >>> line.midpoint
    Point(0.500, 0.500, 0.500)
    >>> line.length == math.sqrt(1 + 1 + 1)
    True
    >>> line.direction
    Vector(0.577, 0.577, 0.577)

    """

    __slots__ = ["_start", "_end"]

    def __init__(self, p1, p2, **kwargs):
        super(Line, self).__init__(**kwargs)
        self._start = None
        self._end = None
        self.start = p1
        self.end = p2

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        from schema import Schema

        return Schema({"start": Point, "end": Point})

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "line"

    @property
    def data(self):
        """dict : The data dictionary that represents the line."""
        return {"start": self.start, "end": self.end}

    @data.setter
    def data(self, data):
        self.start = data["start"]
        self.end = data["end"]

    @classmethod
    def from_data(cls, data):
        """Construct a frame from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Examples
        --------
        >>> line = Line.from_data({'start': [0.0, 0.0, 0.0], 'end': [1.0, 0.0, 0.0]})
        >>> line.end
        Point(1.000, 0.000, 0.000)

        """
        return cls(data["start"], data["end"])

    @classmethod
    def from_point_and_vector(cls, point, vector):
        return cls(point, point + vector)

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
        return float("inf"), float("inf")

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, point):
        self._start = Point(*point)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, point):
        self._end = Point(*point)

    @property
    def point(self):
        return self._start

    @point.setter
    def point(self, point):
        self._start = Point(*point)

    @property
    def vector(self):
        return self.end - self.start

    @property
    def length(self):
        return self.vector.length

    @property
    def direction(self):
        return self.vector * (1 / self.length)

    @property
    def midpoint(self):
        return (self.start + self.end) * 0.5

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Line({0!r}, {1!r})".format(self.start, self.end)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.start
        if key == 1:
            return self.end
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.start = value
            return
        if key == 1:
            self.end = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.start, self.end])

    def __eq__(self, other):
        try:
            other_start = other[0]
            other_end = other[1]
        except:  # noqa: E722
            return False
        return self.start == other_start and self.end == other_end

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
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Point`

        """
        if t == 0:
            return self.start
        if t == 1:
            return self.end
        return self.start + self.vector * t

    def frame_at(self, t):
        """
        Frame at the parameter.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Frame`

        """
        point = self.point_at(t)
        xaxis = self.vector
        zaxis = Vector.Zaxis()
        yaxis = zaxis.cross(xaxis)
        return Frame(point, xaxis, yaxis)

    def tangent_at(self, t):
        """
        Tangent vector at the parameter.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        return self.direction

    def normal_at(self, t):
        """
        Normal vector at the parameter.
        The normal vector is perpendicular to the tangent vector
        and the Z axis of the world coordinate system.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        xaxis = self.vector
        zaxis = Vector.Zaxis()
        yaxis = zaxis.cross(xaxis)
        yaxis.unitize()
        return yaxis

    def transform(self, T):
        """Transform this line.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> line = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(90))
        >>> line.transform(R)
        >>> line.end
        Point(0.000, 1.000, 0.000)

        """
        self.start.transform(T)
        self.end.transform(T)
