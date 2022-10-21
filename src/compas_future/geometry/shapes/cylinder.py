from .shape import Shape


class Cylinder(Shape):
    def __init__(self, radius, height, frame=None, **kwargs):
        super(Cylinder, self).__init__(frame=frame, **kwargs)
        self.radius = radius
        self.height = height
