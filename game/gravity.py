from pyglet import window, clock, shapes
from pyglet.window import key

from game.vector import Vector
from game.body import Body


class GravityWindow(window.Window):

    def __init__(self, *args, **kwargs):
        super(GravityWindow, self).__init__(1400, 1000, *args, **kwargs)
        self.set_location(850, 300)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)      

        self.bodies = [
            Body(700, 500, 10000, radius=20, velocity=Vector(0, 0))
        ]
        self.selected = None
        self.selected_vector_line = shapes.Line(0, 0, 0, 0, 2, (0, 0, 255))
        self.freeze = True

        self.default_cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
        self.paste_cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)

        clock.schedule_interval(self.update_game, 1/60)
    
    def get_acceleration(self, body1, body2):
        direction = Vector(body2.x, body2.y) - Vector(body1.x, body1.y)
        distance = direction.magnitude()

        if distance < body1.radius + body2.radius:
            return Vector()
        
        g = body2.mass / (distance**2)

        return direction.normalize() * g

    def on_draw(self):
        self.clear()
        
        for b in self.bodies:
            b.draw()
            if self.freeze:
                b.draw_velocity_vector()
        
        if self.selected and self.keys[key.V]:
            self.selected_vector_line.draw()
    
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

    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_ACCEL:
            self.set_mouse_cursor(self.paste_cursor)
        
        elif symbol == key.ENTER and self.selected:
            self.selected.velocity = Vector(
                (self._mouse_x - self.selected.x)/10, 
                (self._mouse_y - self.selected.y)/10
            )

        elif symbol == key.SPACE:
            self.freeze = not self.freeze

            if self.selected:
                self.selected.unselect()
                self.selected = None

        elif symbol == key.EQUAL and self.selected:
            self.selected.mass += 1000
            self.selected.radius += 1

        elif symbol == key.MINUS and self.selected:
            self.selected.mass -= 1000
            self.selected.radius -= 1
        
        elif symbol == key.BACKSPACE and self.selected:
            self.bodies.remove(self.selected)
            self.selected = None

    def on_key_release(self, symbol, modifiers):
        if modifiers & key.MOD_ACCEL or key.UP:
            self.set_mouse_cursor(self.default_cursor)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selected:
            self.selected.x, self.selected.y = x, y
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.selected:
            self.selected_vector_line.x, self.selected_vector_line.y = self.selected.x, self.selected.y
            self.selected_vector_line.x2, self.selected_vector_line.y2 = x, y
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Set velocity/unselect         
        if self.selected:
            if self.keys[key.V]:
                self.selected.velocity = Vector(
                    (x - self.selected.x)/10, 
                    (y - self.selected.y)/10
                )

            self.selected.unselect()
            self.selected = None

        # Select body 
        if self.freeze:
            for b in self.bodies:
                if (x, y) in b:
                    b.select()
                    self.selected = b

        # Add body
        if modifiers & key.MOD_ACCEL:
            self.bodies.append(Body(x, y, 1000, 10, velocity=Vector(0, 0)))
