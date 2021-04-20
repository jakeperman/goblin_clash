import arcade
frames_per_update = 3
left = 1
right = 0

class Sword(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/4x/dagger4x.png", .5)
        self.center_x, self.center_y = x, y
        self.damage = 5
        self.animation = None
        self.use = False
        self.direction_facing = 0
        self.frame = 0

    def update(self):
        if self.animation:
            if not self.animation.is_complete():
                self.animation.update_animation()
            else:
                self.animation = None
                print("none")
        if self.use:
            self.animation.direction = self.direction_facing
            if self.direction_facing == right:
                if self.frame > 4:
                    self.angle += 22.5
                else:
                    self.angle -= 22.5
            elif self.direction_facing == left:

                if self.frame > 4:
                    self.angle -= 22.5
                else:
                    self.angle += 22.5
            print(f"weapon_frame: {self.frame}")
            self.frame += 1
            if self.frame > 9:
                self.frame = 0
                self.use = False
        else:
            if self.direction_facing == left:
                self.angle = 90
            elif self.direction_facing == right:
                self.angle = 360

    def slash(self):
        if self.direction_facing:
            self.animation = Slash(self.center_x - 10, self.center_y - 2)
        else:
            self.animation = Slash(self.center_x + 10, self.center_y - 4)
        self.use = True


class Dagger_new(arcade.AnimatedTimeBasedSprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x, self.center_y = x, y
        self.textures = ["resources/sprites/4x/dagger4x.png"]

# dagger wepaon class
class Dagger(arcade.Sprite):
    def __init__(self, x, y, parent):
        super().__init__("resources/sprites/4x/dagger4x.png", .4)
        self.center_x, self.center_y = x, y
        self.use = False
        self.frame = 0
        self.direction_facing = 0
        self.a_distance = 4
        self.parent = parent
        self.attacked = True

    def update(self):
        # update the position and direction while not attacking
        if not self.use or self.parent.changed_direction:
            self.set_direction(self.direction_facing)
        else:
            if self.direction_facing is left:
                self.center_y = self.parent.center_y - 10
            elif self.direction_facing is right:
                self.center_y = self.parent.center_y - 15
        self.attacked = False

    def slash(self):
        self.use = True

    def attack(self):
        # move the dagger in sync with the players movement
        if self.parent.moving:
            if self.direction_facing == 0:
                self.center_x += 4 + (self.parent.change_x * 3)
            else:
                self.center_x += -4 + (self.parent.change_x * 3)
        else:
            if self.direction_facing == 0:
                self.center_x += 4
            else:
                self.center_x -= 4
    def set_direction(self, direction):
        if direction == right:
            self.angle = -45
            self.center_x = self.parent.right
            self.center_y = self.parent.center_y - 14
        elif direction == left:
            self.angle = 90 + 45
            self.center_x = self.parent.left
            self.center_y = self.parent.center_y - 10



class Slash(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/sprites/dagger_slash/0.png", scale=.5)
        self.center_x, self.center_y = x, y
        self.path = "resources/sprites/dagger_slash/"
        self.animation_length = 4
        self.animation_speed = 5
        self.textures = [arcade.load_texture_pair(f"{self.path}{x}.png") for x in range(self.animation_length)]
        self.cur_texture_index = 0
        self.frame = 0
        self.complete = False
        self.direction = 0

    def update_animation(self, delta_time: float = 1/60):
        self.frame += 1
        if self.frame >= frames_per_update * self.animation_length:
            print("complete")
            self.frame = 0
            self.complete = True

        # print(f"frame:{self.frame}")
        self.cur_texture_index = self.frame // frames_per_update
        # print(self.cur_texture_index)
        self.texture = self.textures[self.cur_texture_index][self.direction]
        if self.cur_texture_index > self.animation_length -1:
            self.cur_texture_index = 0

    def is_complete(self):
        return self.complete


