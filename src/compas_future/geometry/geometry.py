from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Geometry(Data):
    """
    Base class for all geometric objects.
    """

    def __ne__(self, other):
        # this is not obvious to ironpython
        return not self.__eq__(other)

    def transform(self, transformation):
        """
        Transform the geometry.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation used to transform the geometry.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed(self, transformation):
        """
        Returns a transformed copy of this geometry.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation used to transform the geometry.

        Returns
        -------
        :class:`Geometry`
            The transformed geometry.

        """
        geometry = self.copy()
        geometry.transform(transformation)
        return geometry

    def translate(self, vector):
        """
        Translate the geometry.

        Parameters
        ----------
        vector : [float, float, float] | :class:`compas.geometry.Vector`

        Returns
        -------
        None

        """
        from compas.geometry import Translation

        matrix = Translation.from_vector(vector)
        self.transform(matrix)

    def translated(self, vector):
        """
        Return a translated copy of the geometry.

        Parameters
        ----------
        vector : [float, float, float] | :class:`compas.geometry.Vector`

        Returns
        -------
        :class:`compas.geometry.Geometry`

        """
        geometry = self.copy()
        geometry.translate(vector)
        return geometry

    def rotate(self, axis, angle, point=None):
        """
        Rotate the geometry.

        Parameters
        ----------
        axis : [float, float, float] | :class:`compas.geometry.Vector`
        angle : float
        point : [float, float, float] | :class:`compas.geometry.Point`

        Returns
        -------
        None

        """
        from compas.geometry import Rotation

        point = point or [0, 0, 0]
        matrix = Rotation.from_axis_and_angle(axis=axis, angle=angle, point=point)
        self.transform(matrix)

    def rotated(self, axis, angle, point=None):
        """
        Return a rotated copy of the geometry.

        Parameters
        ----------
        axis : [float, float, float] | :class:`compas.geometry.Vector`
        angle : float
        point : [float, float, float] | :class:`compas.geometry.Point`

        Returns
        -------
        :class:`compas.geometry.Geometry`

        """
        geometry = self.copy()
        geometry.rotate(axis=axis, angle=angle, point=point)
        return geometry
