from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_future.geometry.curves.curve import Curve
from compas_future.geometry.transformations.transformation import Transformation


class Conic(Curve):
    @property
    def eccentricity(self):
        raise NotImplementedError

    def transform(self, T):
        """
        Transform the curve.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

        """
        self.frame.transform(T)
        self._transformation = Transformation.from_frame(self.frame)
