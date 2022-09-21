import random

from compas.colors import Color as _Color


class Color(_Color):
    @classmethod
    def random(cls):
        r = random.random()
        g = random.random()
        b = random.random()
        return cls(r, g, b)
