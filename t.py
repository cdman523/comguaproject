import math as m


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __sub__(self, v2):
        return self + v2 * (-1)

    def __eq__(self, v2):
        return (self.x, self.y) == (v2.x, v2.y)

    @classmethod
    def angVec(cls, r, theta):
        return cls(m.cos(m.radians(theta)), m.sin(m.radians(theta))) * r

    def __abs__(self):
        return m.hypot(self.x, self.y)

    @property
    def angle(self):
        return m.degrees(m.atan2(self.y, self.x))


v1 = Vector(4, 3)
v2 = Vector(2, 5)
v3 = Vector(-5, -6)
print(v1.angle, (v3 - v1).angle)
