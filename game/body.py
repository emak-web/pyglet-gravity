from pyglet import shapes
from game.vector import Vector


class Body:
    def __init__(self, x, y, mass, radius=5, velocity=Vector(), color=(255, 255, 255)):
        self.shape = shapes.Circle(x=x, y=y, radius=radius, color=color)
        self.mass = mass
        self.velocity = velocity
        self.velocity_vector = shapes.Line(0, 0, 0, 0, 2, (0, 0, 255))
        self.acceleration = Vector()
    
    def draw(self):
        self.shape.draw()
    
    def draw_velocity_vector(self):
        self.velocity_vector.x, self.velocity_vector.y = self.shape.x, self.shape.y
        self.velocity_vector.x2, self.velocity_vector.y2 = self.shape.x+self.velocity.x*10, self.shape.y+self.velocity.y*10
        self.velocity_vector.draw()

    def move(self):
        self.velocity += self.acceleration
        self.shape.x += self.velocity.x
        self.shape.y += self.velocity.y

    def select(self):
        self.shape.color = (255, 0, 0)
    
    def unselect(self):
        self.shape.color = (255, 255, 255)
