from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_future.geometry.curves.curve import Curve


class Conic(Curve):
    @property
    def eccentricity(self):
        raise NotImplementedError
