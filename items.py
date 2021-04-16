import arcade

class Dagger(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/4x/dagger4x.png", .5)
        self.center_x, self.center_y = x, y
        self.damage = 5