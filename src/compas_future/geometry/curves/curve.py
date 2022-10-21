from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_future.geometry.geometry import Geometry


class Curve(Geometry):
    def __init__(self, *args, **kwargs):
        super(Curve, self).__init__(*args, **kwargs)

    @property
    def is_periodic(self):
        raise NotImplementedError

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def domain(self):
        raise NotImplementedError

    @property
    def start(self):
        raise NotImplementedError

    @property
    def end(self):
        raise NotImplementedError

    def point_at(self, t):
        raise NotImplementedError

    def frame_at(self, t):
        raise NotImplementedError

    def tangent_at(self, t):
        raise NotImplementedError

    def normal_at(self, t):
        raise NotImplementedError
