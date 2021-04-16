import arcade

UPDATES_PER_FRAME = 6

class Player(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.center_x, self.center_y = x, y
        self.scale = scale
        self.current_texture = 0
        self.can_jump = True
        self.direction_facing = 0
        # self.direction_textures = arcade.load_texture_pair("resources/sprites/char4x.png", "Simple")
        self.running_textures = []
        for i in range(2):
            t = arcade.load_texture_pair(f"resources/sprites/player/{i}.png", "Simple")
            self.running_textures.append(t)
        print(self.running_textures)
        self.texture = self.running_textures[1][0]

        self.win_x = x
        self.hp = 10
        self.walk_frame = 0
        self.frame = 0
        self.weapon = None

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1/60):
        left, right = 1, 0
        # calculate if frame needs to be updated
        d_time = 60 // UPDATES_PER_FRAME
        if self.frame % d_time == 0:
            if self.walk_frame:
                self.walk_frame = 0
            else:
                self.walk_frame = 1
        # set idle texture
        if self.change_x == 0:
            self.texture = self.running_textures[0][self.direction_facing]

        # set walking textures
        if self.change_x < 0:
            self.texture = self.running_textures[self.walk_frame][1]
            self.hit_box = self.texture.hit_box_points
            self.direction_facing = left
        elif self.change_x > 0:
            self.texture = self.running_textures[self.walk_frame][0]
            self.hit_box = self.texture.hit_box_points
            self.direction_facing = right

        self.frame += 1


    def attack(self, weapon):
        pass



