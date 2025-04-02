from pyglet import shapes
from game.vector import Vector


class Body:
    def __init__(self, x, y, mass, radius=5, velocity=Vector(), color=(255, 255, 255)):
        self.shape = shapes.Circle(x=x, y=y, radius=radius, color=color)
        self.mass = mass
        self.velocity = velocity
        self.acceleration = Vector()
    
    def move(self):
        self.velocity += self.acceleration
        self.shape.x += self.velocity.x
        self.shape.y += self.velocity.y

    def select(self):
        self.shape.color = (255, 0, 0)
    
    def unselect(self):
        self.shape.color = (255, 255, 255)
