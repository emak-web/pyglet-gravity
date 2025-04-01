from math import sqrt


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

        return self
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

        return self
    
    def __mul__(self, scalar):
        self.x *= scalar
        self.y *= scalar

        return self

    def __truediv__(self, scalar):
        if scalar == 0:
            self.x = 0
            self.y = 0
        else:
            self.x /= scalar
            self.y /= scalar

        return self

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            self.x = 0
            self.y = 0
        else:
            self.x /= mag
            self.y /= mag

        return self
