from pyglet import window, clock
from pyglet.window import key

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
        self.selected = None
        self.freeze = True

        clock.schedule_interval(self.update_game, 1/60)
    
    def get_acceleration(self, body1, body2):
        direction = Vector(body2.shape.x, body2.shape.y) - Vector(body1.shape.x, body1.shape.y)
        distance = direction.magnitude()

        if distance < body1.shape.radius + body2.shape.radius:
            return Vector()
        
        g = body2.mass / (distance**2)

        return direction.normalize() * g

    def on_draw(self):
        self.clear()
        for b in self.bodies:
            b.shape.draw()
    
    def update_game(self, dt):
        if not self.freeze:
            for current_body in self.bodies:
                acceleration = Vector()
                for b in self.bodies:
                    if b != current_body:
                        acceleration += self.get_acceleration(current_body, b)

                current_body.acceleration = acceleration
            
            for b in self.bodies:
                b.move()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.selected:
            self.selected.unselect()
            self.selected = None

        if modifiers & key.MOD_ACCEL:
            self.bodies.append(Body(x, y, 100, 5, velocity=Vector(0, 5)))
        else:
            for b in self.bodies:
                if (x, y) in b.shape:
                    b.select()
                    self.selected = b

    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_ACCEL:
            cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
            self.set_mouse_cursor(cursor)

        elif symbol == key.SPACE:
            self.freeze = not self.freeze

        elif symbol == key.EQUAL and self.selected:
            self.selected.mass += 1000
            self.selected.shape.radius += 1

        elif symbol == key.MINUS and self.selected:
            self.selected.mass -= 1000
            self.selected.shape.radius -= 1

    def on_key_release(self, symbol, modifiers):
        if modifiers & key.MOD_ACCEL or key.UP:
            cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
            self.set_mouse_cursor(cursor)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selected:
            self.selected.shape.x, self.selected.shape.y = x, y
            
