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


class Hyperbola(Conic):
    """
    A hyperbola is defined by a plane and a major and minor axis.
    The origin of the coordinate frame is the center of the hyperbola.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the hyperbola.
    major : float
        The major of the hyperbola.
    minor : float
        The minor of the hyperbola.

    Attributes
    ----------
    is_periodic : bool, read-only
        An hyperbola is periodic (True).
    is_closed : bool, read-only
        An hyperbola is closed (True).
    domain : tuple[float, float], read-only
        The parameter domain: 0, 2pi
    eccentricity : float, read-only
        The eccentricity of a hyperbola is a number higher than 1.
    frame : :class:`compas.geometry.Point`
        The coordinate frame of the hyperbola.
    point : :class:`compas.geometry.Point`
        The center of the hyperbola.
    major : float
        The major radius of the hyperbola.
    minor : float
        The minor radius of the hyperbola.
    center : :class:`compas.geometry.Point`, read-only
        The center of the hyperbola.
    xaxis : :class:`compas.geometry.Vector`, read-only
        The X axis of the frame of the hyperbola.
    yaxis : :class:`compas.geometry.Vector`, read-only
        The Y axis of the frame of the hyperbola.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the hyperbola.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the hyperbola.
    focus1 : :class:`compas.geometry.Point`, read-only
        The first focus of the hyperbola is on the positive x axis.
    focus2 : :class:`compas.geometry.Point`, read-only
        The second focus of the hyperbola is on the negative x axis.
    asymptote1 : :class:`compas.geometry.Line`, read-only
        The first asymptote of the hyperbola.
    asymptote2 : :class:`compas.geometry.Line`, read-only
        The second asymptote of the hyperbola.
    semifocal : float, read-only
        The distance between the center and the focus points.
    focal : float, read-only
        The distance between the two focus points.

    """

    __slots__ = ["_frame", "_major", "_minor"]

    def __init__(self, frame, major, minor, **kwargs):
        super(Hyperbola, self).__init__(**kwargs)
        self._frame = None
        self._major = None
        self._minor = None
        self._transformation = None
        self.frame = frame or Frame.worldXY()
        self.major = major
        self.minor = minor

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
                "major": schema.And(float, lambda x: x > 0),
                "minor": schema.And(float, lambda x: x > 0),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "hyperbola"

    @property
    def data(self):
        """dict : The data dictionary that represents the hyperbola."""
        return {"frame": self.frame, "major": self.major, "minor": self.minor}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.major = data["major"]
        self.minor = data["minor"]

    @classmethod
    def from_data(cls, data):
        """Construct a hyperbola from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Hyperbola`
            The constructed hyperbola.

        """
        return cls(data["frame"], data["minor"], data["minor"])

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
        return 0, 2 * pi

    @property
    def eccentricity(self):
        return self.semifocal / self.major

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
        self.frame.point = point

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, major):
        self._major = float(major)

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, minor):
        self._minor = float(minor)

    @property
    def a(self):
        return self.major

    @property
    def b(self):
        return self.minor

    @property
    def c(self):
        return self.semifocal

    @property
    def center(self):
        return self.frame.point

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
        return Plane(self.point, self.normal)

    @property
    def focus1(self):
        return self.point + self.xaxis * self.semifocal

    @property
    def focus2(self):
        return self.point + self.xaxis * -self.semifocal

    @property
    def asymptote1(self):
        pass

    @property
    def asymptote2(self):
        pass

    @property
    def semifocal(self):
        return sqrt(self.major**2 + self.minor**2)

    @property
    def focal(self):
        return 2 * self.semifocal

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Hyperbola({0!r}, {1!r}, {2!r})".format(
            self.plane, self.major, self.minor
        )

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.major
        elif key == 2:
            return self.minor
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.major = value
        elif key == 2:
            self.minor = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.major, self.minor])

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # transformations
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
        secant = 1 / cos(t)
        x = self.a * secant
        y = self.b * sin(t) * secant
        point = Point(x, y, 0)
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
        raise NotImplementedError

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
        raise NotImplementedError

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
        xaxis = self.tangent_at(t, normalized=False)
        yaxis = self.frame.zaxis.cross(xaxis)
        return Frame(point, xaxis, yaxis)

    def transform(self, T):
        """Transform the hyperbola.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Hyperbola
        >>> hyperbola = Hyperbola(Plane.worldXY(), 8, 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> hyperbola.transform(T)

        """
        self.plane.transform(T)
