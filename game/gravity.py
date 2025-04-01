from pyglet import window, clock, shapes

from game.vector import Vector
from game.body import Body


class GravityWindow(window.Window):

    def __init__(self, *args, **kwargs):
        super(GravityWindow, self).__init__(1400, 1000, *args, **kwargs)
        self.set_location(850, 300)

        self.bodies = [
            Body(700, 500, 10000, velocity=Vector(0, 0), radius=15),
            Body(900, 500, 100, velocity=Vector(0, 5)),
            Body(500, 500, 100, velocity=Vector(0, -4)),
        ]

        clock.schedule_interval(self.update_game, 1/60)
    
    def get_acceleration(self, body1, body2):
        direction = Vector(body2.shape.x, body2.shape.y) - Vector(body1.shape.x, body1.shape.y)
        distance = direction.magnitude()

        if distance == 0:
            return Vector()
        
        g = body2.mass / (distance**2)

        return direction.normalize() * g

    def on_draw(self):
        self.clear()
        for b in self.bodies:
            b.shape.draw()
    
    def update_game(self, dt):
        for current_body in self.bodies:
            acceleration = Vector()
            for b in self.bodies:
                if b != current_body:
                    acceleration += self.get_acceleration(current_body, b)

            current_body.acceleration = acceleration
        
        for b in self.bodies:
            b.move()
