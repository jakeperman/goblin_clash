import arcade

class Goblin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/4x/goblin4X.png", 1)
        self.center_x, self.center_y = x, y
        self.change_x = -2
        self.hp = 10
        self.damage = 4

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y