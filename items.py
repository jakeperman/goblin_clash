import arcade

class Dagger(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/4x/dagger4x.png", .5)
        self.center_x, self.center_y = x, y
        self.damage = 5


class Slash(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/dagger_slash/0.png")
        self.center_x, self.center_y = x, y
        self.path = "resources/sprites/dagger_slash/"
        self.animation_length = 4
        self.animation_speed = 5
        self.textures = [arcade.load_texture(f"{self.path}{x}.png") for x in range(self.animation_length)]
        self.cur_texture_index = 0

    def update_animation(self, delta_time: float = 1/60):
        self.texture = self.textures[self.cur_texture_index]
        self.cur_texture_index += 1
        if self.cur_texture_index > self.animation_length -1:
            self.cur_texture_index = 0


