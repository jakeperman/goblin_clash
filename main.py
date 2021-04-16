import arcade
from player import *
from enemies import *
from terrain import *
from items import *
SW, SH = 832, 768
SCALE = 1
GRAVITY = 2
JUMP_SPEED = 24
LEFT_VIEW_MARGIN = 350
RIGHT_VIEW_MARGIN = 350
TOP_VIEW_MARGIN = 200
BOTTOM_VIEW_MARGIN = 200
TOP_VIEW_CHANGE = 128
VIEW_CHANGE = 128
BLOCK_SCALE = .75


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SW, SH, "Goblin Clash")
        arcade.set_background_color(arcade.color.SPANISH_SKY_BLUE)
        self.player = None
        self.players = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.controls = {"a": -3, "d": 3}
        self.jump = 32
        self.ground_list = None
        self.setup()
        self.keys_pressed = []
        self.goblin = Goblin(1600, 350)
        self.goblin.change_y = -GRAVITY
        self.enemies.append(self.goblin)
        self.dagger = Dagger(SW/2, SH/2)
        self.hurt_sound = arcade.Sound("resources/sounds/oof.wav")
        self.current_player = self.hurt_sound.play(1)
        self.right_view = SW
        self.left_view = 0
        self.top_view = SH
        self.bottom_view = 0
        self.set_vsync(True)
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0
        self.slash = Slash(SW/2, SH/2)


    def setup(self):
        self.player = Player(SW / 2, SH / 2, SCALE)
        self.players.append(self.player)
        map_name = "resources/maps/my_map.tmx"  # map file
        grass = "Grass"  # grass layer name
        dirt = "Dirt"  # dirt layer name
        # read the map
        level_map = arcade.tilemap.read_tmx(map_name)
        self.ground_list = arcade.tilemap.process_layer(map_object=level_map, layer_name="ground", scaling=BLOCK_SCALE, use_spatial_hash=True)

        # self.grass_blocks = arcade.tilemap.process_layer(map_object=level_map, layer_name=grass, scaling=SCALE,
        #                                                  use_spatial_hash=True)
        # self.dirt_blocks = arcade.tilemap.process_layer(map_object=level_map, layer_name=dirt, scaling=SCALE)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list, GRAVITY)
        self.physics_engine.disable_multi_jump()
        self.player.weapon = Dagger(self.player.right, self.player.center_y)

    def on_draw(self):
        arcade.start_render()
        self.enemies.draw()
        self.ground_list.draw()
        self.players.draw()
        self.player.weapon.draw()
        if self.player.should_attack:
            self.player.attack()
            self.player.should_attack = False
        self.slash.draw()



        # self.dagger.draw()
        # for block in self.ground_list:
        #     block.draw_hit_box(arcade.color.RED, 4)
        # self.player.draw_hit_box(arcade.color.RED, 4)

    def on_update(self, delta_time: float):
        # set screen scroll boundaries
        left_boundary = self.left_view + LEFT_VIEW_MARGIN
        right_boundary = self.left_view + SW - RIGHT_VIEW_MARGIN
        top_boundary = self.bottom_view + SH - TOP_VIEW_MARGIN
        bottom_boundary = self.bottom_view + BOTTOM_VIEW_MARGIN
        changed = False

        # register keypress actions
        if self.keys_pressed:
            self.player.change_x = self.controls[self.keys_pressed[0]]
        else:
            self.player.change_x = 0

        # update sprites
        self.slash.update_animation()
        self.enemies.update()
        self.players.update()
        self.player.update_animation()
        self.physics_engine.update()
        self.player.weapon.center_x = self.player.right
        self.player.weapon.center_y = self.player.center_y - 10

        # screen scrolling system

        # check if player is close enough to edges to scroll screen
        if self.player.left < left_boundary:
            self.left_view -= left_boundary - self.player.left
            changed = True
        elif self.player.right > right_boundary:
            self.left_view += self.player.right - right_boundary
            changed = True
        if self.player.top > top_boundary:
            self.bottom_view += self.player.top - top_boundary
            print(f"bottom: {self.bottom_view}")
            print(f"top: {self.top_view}")
            changed = True
        elif self.player.bottom < bottom_boundary:
            self.bottom_view -= bottom_boundary - self.player.bottom
            changed = True
        # prevent the view from going below y=0
        if self.bottom_view < 0:
            self.bottom_view = 0

        # if view has changed, update the window accordingly
        if changed:
            arcade.set_viewport(self.left_view, SW + self.left_view, self.bottom_view, SH + self.bottom_view)

        # check for collision of player with enemies
        if arcade.check_for_collision_with_list(self.player, self.enemies):
            if self.hurt_sound.get_stream_position(self.current_player) == 0:
                self.current_player = self.hurt_sound.play(1)

        # enemy physics
        for enemy in self.enemies:
            if arcade.check_for_collision_with_list(enemy, self.ground_list):
                enemy.change_y = 0
                # enemy.center_y += 30
            else:
                enemy.change_y = -GRAVITY

    def on_key_press(self, symbol: int, modifiers: int):
        key = chr(symbol)
        # for each key pressed, add it to the current keys pressed
        if key in list(self.controls.keys()):
            self.keys_pressed.insert(0, key)
        # if player presses space, and jump conditions are met, jump
        elif symbol == self.jump:
            if self.physics_engine.can_jump():
                self.physics_engine.jump(JUMP_SPEED)
        # print(self.keys_pressed)
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        key = chr(symbol)
        # removes keys from keys_pressed if they are no longer pressed
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        # if symbol == self.jump:
        #     self.player.change_y = 0
            pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # kill goblin if player is within range and attacks
        self.player.should_attack = True
        for goblin in self.enemies:
            if self.player.left < goblin.left <= self.player.right + 32:
                self.enemies.remove(goblin)


def main():
    game = Game()
    arcade.run()

if __name__ == '__main__':
    main()