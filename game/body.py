from pyglet import shapes
from game.vector import Vector


class Body(shapes.Circle):
    def __init__(self, x: int = 0, y: int = 0, mass: int = 1000, radius: int = 10, velocity=Vector(), color=(255, 255, 255)):
        super().__init__(x, y, radius, color=color)

        self.mass = mass
        self.velocity = velocity
        self.acceleration = Vector()

        self.velocity_vector = shapes.Line(0, 0, 0, 0, 2, (0, 0, 255))
    
    def draw_velocity_vector(self):
        self.velocity_vector.x, self.velocity_vector.y = self.x, self.y
        self.velocity_vector.x2, self.velocity_vector.y2 = self.x+self.velocity.x*10, self.y+self.velocity.y*10
        self.velocity_vector.draw()

    def move(self):
        self.velocity += self.acceleration
        self.x += self.velocity.x
        self.y += self.velocity.y

    def select(self):
        self.color = (255, 0, 0)
    
    def unselect(self):
        self.color = (255, 255, 255)
