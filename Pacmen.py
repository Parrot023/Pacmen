"""
Simple program to show moving a sprite with the keyboard.

This program uses the Arcade library found at http://arcade.academy

Artwork from https://kenney.nl/assets/space-shooter-redux

"""

import random
import math
import time
import os
import sys
import time

import arcade

# Global variables ---------------------------

SPRITE_SCALING = 0.5

TILE_SIZE = 48

# Set the size of the screen
SCREEN_WIDTH = TILE_SIZE * 10
SCREEN_HEIGHT = TILE_SIZE * 10

# Variables controlling the player
PLAYER_LIVES = 3
PLAYER_SPEED_X = 5
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2
PLAYER_SHOT_SPEED = 4
PLAYER_SCORE = 0
PLAYER_DEFAULT_AMMO = 10
# IN PERCENT
CHANCE_OF_ENEMY_SPAWN = 50

EXPLOSION_LIFE_TIME = 0.5

TILE_PATH = "assets/Tiles"

GAMESTATE = 1

LEVEL = 0

TEXTURE_DIR = "assets/textures"

ENEMY_SPAWN_POINTS = [
    [SCREEN_WIDTH / 2, 0],
    [SCREEN_WIDTH, SCREEN_HEIGHT / 2],
    [SCREEN_WIDTH / 2, SCREEN_HEIGHT],
    [0, SCREEN_HEIGHT / 2]
]

MAPS = [
    [
        [2, 2, 2, 1, 0, 0, 1, 1, 1, 1],
        [2, 2, 2, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 1, 7, 7, 1, 1, 1, 1],
        [2, 2, 2, 1, 7, 7, 1, 1, 1, 1],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1],
        [1, 1, 1, 1, 7, 7, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 7, 7, 7, 7, 7, 7, 7],
        [2, 2, 2, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 6, 6, 7, 7, 7, 7],
        [7, 7, 7, 6, 7, 7, 6, 7, 7, 7],
        [7, 7, 7, 6, 7, 7, 6, 7, 7, 7],
        [7, 7, 7, 6, 6, 6, 6, 7, 7, 7],
        [7, 7, 7, 6, 7, 7, 6, 7, 7, 7],
        [7, 7, 7, 6, 7, 7, 6, 7, 7, 7],
        [7, 7, 7, 6, 7, 7, 6, 7, 7, 7],
    ],
    [
        [2, 2, 2, 4, 4, 4, 4, 4, 4, 4],
        [2, 2, 2, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    ]
],

# delta_time in the MyGame update function is in seconds
# therfore our ENEMY_SPAWN_SPEED is in seconds
ENEMY_SPAWN_SPEED = 1

# ----------------------------------------------


class PowerUp(arcade.Sprite):

    textures = [
        arcade.load_texture(
            "assets/textures/PowerUps/live.png", scale=SPRITE_SCALING * 2),
        arcade.load_texture(
            "assets/textures/PowerUps/ammo.png", scale=SPRITE_SCALING * 2)
    ]

    def __init__(self, type):

        super().__init__("assets/textures/PowerUps/live.png", SPRITE_SCALING * 2)

        self.parameters = {
            "lives": 0,
            "ammo": 0,
        }

        self.spawn_point = random.choice(ENEMY_SPAWN_POINTS)
        self.center_x, self.center_y = self.spawn_point

        self.dest_x = SCREEN_WIDTH / 2
        self.dest_y = SCREEN_HEIGHT / 2
        # Sets the start location
        self.start_x = self.center_x
        self.start_y = self.center_y

        # Calculates angle towards the detination point
        # with the difference between dest_y and start_y
        # and the difference between dest_x and start_x
        angle = math.atan2(self.dest_y - self.start_y,
                           self.dest_x - self.start_x)

        # Calculates change x and y with cosin and sin
        self.change_x = math.cos(angle)
        self.change_y = math.sin(angle)

        if type == 0:
            self.parameters["lives"] = random.randint(0, 10)
            self.texture = PowerUp.textures[0]
        elif type == 1:
            self.parameters["ammo"] = random.randint(0, 10)
            self.texture = PowerUp.textures[1]

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y


class Level():

    """
    Class for drawing out a level
    """

    def __init__(self):

        # Saying that we want to use the global variable LEVEL
        # Idk why this is needed, but without it i get errors
        global LEVEL

        # Prints out all the tiles in the TILE_PATH folder
        # And adds them to self.possible_tiles
        self.possible_tiles = sorted(os.listdir(TILE_PATH))
        for i in self.possible_tiles:
            print("Tile:", self.possible_tiles.index(i), i)

        TILE_SIZE = 48
        # To do get file dimensions

        # The default tile is used when there are no more maps
        self.default = 13

    def draw(self):

        self.tile_list = arcade.SpriteList()

        # Adding tiles to tile list
        for y in range(int(SCREEN_HEIGHT / TILE_SIZE)):
            for x in range(int(SCREEN_WIDTH / TILE_SIZE)):

                try:
                    tile = Tile(x * TILE_SIZE + (TILE_SIZE / 2), y * TILE_SIZE +
                                (TILE_SIZE / 2), self.possible_tiles[MAPS[0][LEVEL][9 - y][x]])
                except Exception as e:
                    tile = Tile(x * TILE_SIZE + (TILE_SIZE / 2), y * TILE_SIZE +
                                (TILE_SIZE / 2), self.possible_tiles[self.default])
                    # print("No more maps")

                self.tile_list.append(tile)
        # Drawing tiles
        self.tile_list.draw()


class Tile(arcade.Sprite):
    """
    A tile sprite used to create a level
    """

    def __init__(self, center_x, center_y, file_name):

        # texture is giving by the level
        super().__init__("{}/{}".format(TILE_PATH, file_name), 1)

        # position is given by the level
        self.center_x = center_x
        self.center_y = center_y


class Explosion(arcade.AnimatedTimeSprite):
    """
    An explsosion
    """

    def __init__(self, texture_list, SPRITE_SCALING, center_x=0, center_y=0):

        self.textures = texture_list

        super().__init__(scale=SPRITE_SCALING)

        self.age = 0.0

        super().update_animation()

    def update_animation(self, delta_time):

        if self.age > EXPLOSION_LIFE_TIME:
            self.kill
        else:
            self.age += delta_time

        super().update_animation()


class Player(arcade.Sprite):
    """
    The player
    """

    textures = {
        "has_ammo": arcade.load_texture("images/playerShip1_blue.png", scale=SPRITE_SCALING),
        "no_ammo": arcade.load_texture("images/playerShip1_red.png", scale=SPRITE_SCALING)
    }

    def __init__(self, center_x=0, center_y=0):
        """
        Setup new Player object
        """

        # Set the graphics to use for the sprite
        super().__init__("images/playerShip1_blue.png", SPRITE_SCALING)

        self.center_x = center_x
        self.center_y = center_y

        self.ammo = PLAYER_DEFAULT_AMMO

    def update(self):
        """
        Move the sprite
        """

        # Sets the Sprites textures based on the wether or not they have shots left
        # More than 0 shots left is a blue ship
        # Otherwise it is a red ship
        if self.ammo > 0:
            self.texture = Player.textures["has_ammo"]
        else:
            self.texture = Player.textures["no_ammo"]

        # self.texture = Player.textures["has_ammo"] if self.ammo > 0 else Player.textures["no_ammo"]

    def explode(self):
        self.angle = 100


class PlayerShot(arcade.Sprite):
    """
    A shot fired by the Player
    """

    def __init__(self, player, texture_list):
        """
        Setup new PlayerShot object
        """

        # Set the graphics to use for the sprite
        super().__init__("images/Lasers/laserBlue01.png", SPRITE_SCALING)

        self.center_x = player.center_x
        self.center_y = player.center_y
        self.change_x = math.cos(
            player.radians + (math.pi / 2)) * PLAYER_SHOT_SPEED
        self.change_y = math.sin(
            player.radians + (math.pi / 2)) * PLAYER_SHOT_SPEED
        self.angle = player.angle

        self.animation_textures = texture_list

        self.time_now = 0
        self.time_before = 0
        self.frame_timer = 0
        self.update_delta_time = 0
        self.cur_texture_index = 0

    def update(self):
        """
        Move the sprite
        """

        # Update y position
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Remove shot when over top of screen
        if self.bottom > SCREEN_HEIGHT:
            self.kill()

    def update_animation(self):
        # Calculating delta_time
        self.time_before = self.time_now
        self.time_now = time.time()
        self.update_delta_time = self.time_now - self.time_before

        # adding delta_time to frame timer
        self.frame_timer += self.update_delta_time
        print("updating")

        # increasing cur_texture_index
        if (self.frame_timer > 5 / 60):
            self.cur_texture_index += 1
            if self.cur_texture_index > len(self.animation_textures) - 1:
                self.cur_texture_index = 1
            self.texture = self.animation_textures[self.cur_texture_index]
            self.frame_timer = 0


class Enemy(arcade.Sprite):

    def __init__(self, target, texture_list):
        """
        Setup new Enemy object
        """

        # Set the graphics to use for the sprite
        super().__init__("./assets/pacman_scaled.png", scale=0.05)

        self.value = 1

        # Picks a random spawn point from the ENEMY_SPAWN_POINTS list
        self.spawn_point = random.choice(ENEMY_SPAWN_POINTS)
        self.center_x, self.center_y = self.spawn_point

        # Sets the destination location
        self.dest_x = target.center_x
        self.dest_y = target.center_y
        # Sets the start location
        self.start_x = self.center_x
        self.start_y = self.center_y

        # Calculates angle towards the detination point
        # with the difference between dest_y and start_y
        # and the difference between dest_x and start_x
        angle = math.atan2(self.dest_y - self.start_y,
                           self.dest_x - self.start_x)

        # Calculates change x and y with cosin and sin
        self.change_x = math.cos(angle)
        self.change_y = math.sin(angle)

        # Rotates the enemy based on the angle
        # The calculations above return the angle in radians
        # But lucky for us the arcade sprite objects has a variable that rotates
        # Based on radians
        self.radians = angle

        self.move_textures = texture_list

        # for i in os.listdir("assets/Pacman"):
        #     self.move_textures.append(arcade.load_texture("assets/Pacman/{}".format(i), scale=0.2))

        self.time_now = 0
        self.time_before = 0
        self.frame_timer = 0
        self.update_delta_time = 0

    def update(self):
        # Updates the sprite by adding change_x and change_y to its position
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_animation(self):

        # Calculating delta_time
        self.time_before = self.time_now
        self.time_now = time.time()
        self.update_delta_time = self.time_now - self.time_before

        # adding delta_time to frame timer
        self.frame_timer += self.update_delta_time

        # increasing cur_texture_index
        if (self.frame_timer > 0.2):
            self.cur_texture_index += 1
            if self.cur_texture_index > len(self.move_textures) - 1:
                self.cur_texture_index = 1
            self.texture = self.move_textures[self.cur_texture_index]
            self.frame_timer = 0


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height)

        self.explosion_textures = []
        self.enemy_textures = []
        self.player_shot_textures = []

        # importing textures for explosion animation
        # os.listdir returns the list in an unknown and incorrect order
        # Therfore we sort them with sorted()
        for i in sorted(os.listdir(TEXTURE_DIR + "/explosion")):
            self.explosion_textures.append(
                arcade.load_texture(TEXTURE_DIR + "/explosion/" + i))

        # importing textures for enemy animation
        # os.listdir returns the list in an unknown and incorrect order
        # Therfore we sort them with sorted()
        for i in sorted(os.listdir(TEXTURE_DIR + "/enemy")):
            self.enemy_textures.append(arcade.load_texture(
                TEXTURE_DIR + "/enemy/{}".format(i), scale=0.2))

        for i in sorted(os.listdir(TEXTURE_DIR + "/player_shot")):
            self.player_shot_textures.append(arcade.load_texture(
                TEXTURE_DIR + "/player_shot/{}".format(i), scale=SPRITE_SCALING))

        # checks to see if any textures were found
        if self.enemy_textures == [] or self.explosion_textures == [] or self.player_shot_textures == []:
            # exits program with message and exit code 1
            print("Missing textures in", TEXTURE_DIR)
            sys.exit(1)

        # Variable that will hold a list of shots fired by the player
        self.player_shot_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_score = None
        self.player_lives = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # self.powerup = PowerUp("live", self.player_sprite)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.level = Level()

        self.score_for_level_up = random.randint(5, 10)

        # No points when the game starts
        self.player_score = 0

        # No of lives
        self.player_lives = PLAYER_LIVES

        # Sprite lists
        self.player_shot_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()

        # Create explosion
        # self.new_explosion(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # self.e = Explosion(self.explosion_textures,
        # SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # timers and fps
        self.time_since_enemy_spawn = 0
        self.frame_timer = 0
        self.frame_count = 0
        self.fps = 0

        # Create a Player object
        self.player_sprite = Player(PLAYER_START_X, PLAYER_START_Y)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # self.e.draw()

        # Drawing the level
        self.level.draw()

        self.powerup_list.draw()

        # Drawing the explosions
        self.explosions_list.draw()

        # Drawing the enemies
        self.enemy_list.draw()

        # Drawing the player shots
        self.player_shot_list.draw()

        # Draw the player sprite
        self.player_sprite.draw()

        # Draw players score on screen
        arcade.draw_text(
            "SCORE: {}".format(self.player_score),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 20,  # Y positon
            arcade.color.WHITE   # Color of text
        )

        # Player lives
        arcade.draw_text(
            "LIVES: {}".format(self.player_lives),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 40,  # Y positon
            arcade.color.WHITE   # Color of text
        )

        # FPS
        arcade.draw_text(
            "FPS: {}".format(self.fps),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 60,  # Y positon
            arcade.color.WHITE   # Color of text
        )

        # Player sprite ammo
        arcade.draw_text(
            "AMMO: {}".format(self.player_sprite.ammo),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 80,  # Y positon
            arcade.color.WHITE   # Color of text
        )

    def on_update(self, delta_time):
        """
        Movement and game logic

        delta_time: time since previus update in seconds
        """

        # self.e.update_animation(delta_time)

        # For some reason i have to kinda import the global variable PLAYER_LIVES
        # to change it
        global PLAYER_LIVES
        global LEVEL

        # Adds delta time to time_since_enemy_spawn and frame_timer
        self.time_since_enemy_spawn += delta_time
        self.frame_timer += delta_time

        # Increases frame count
        self.frame_count += 1

        # Update player sprite
        self.player_sprite.update()

        # Update the player shots
        self.player_shot_list.update()
        self.player_shot_list.update_animation()

        # Update the enemy sprite
        self.enemy_list.update()
        self.enemy_list.update_animation()

        self.powerup_list.update()

        # print(self.time_since_enemy_spawn)

        # Checks timer
        # Spawns an enemmy if the timer is equal or over ENEMY_SPAWN_SPEED
        if self.time_since_enemy_spawn >= ENEMY_SPAWN_SPEED:

            if (random.random() > 0.5):
                enemy = Enemy(self.player_sprite, self.enemy_textures)
                self.enemy_list.append(enemy)
            else:
                powerup = PowerUp(random.randint(0, 1))
                self.powerup_list.append(powerup)
            self.time_since_enemy_spawn = 0

        # If frame timer is more than 1. (a second has passed)
        if self.frame_timer >= 1:
            # Resets the frame_timer
            self.frame_timer = 0
            # Sets self.fps to frame count every second
            self.fps = self.frame_count
            # Prints the fps
            print("FPS: {}".format(self.fps))
            # Resets frame_count
            self.frame_count = 0

        # Loops through explosions to kill when end of animation is reached
        for i in self.explosions_list:
            if (i.texture == self.explosion_textures[-1]):
                i.kill()

        self.explosions_list.update()
        self.explosions_list.update_animation()

        for powerup in self.powerup_list:
            collisions = arcade.check_for_collision(
                powerup, self.player_sprite)
            collisons_with_shots = arcade.check_for_collision_with_list(
                powerup, self.player_shot_list)

            if collisons_with_shots:
                powerup.kill()

                self.new_explosion(powerup.center_x, powerup.center_y)

            if collisions:
                self.player_sprite.ammo += powerup.parameters["ammo"]
                PLAYER_LIVES += powerup.parameters["lives"]
                print(powerup.parameters["lives"])
                powerup.kill()

        # Loops through each enemy to checks if an enemy has hit a shot
        for enemy in self.enemy_list:
            # Checks if a shot collides with the enemy
            collisions = arcade.check_for_collision_with_list(
                enemy, self.player_shot_list)
            # Kills the enemy if there is any collisons
            if len(collisions) > 0:
                enemy.kill()
                self.new_explosion(enemy.center_x, enemy.center_y)
            # Kills each colliding shot
            for shot in collisions:
                self.player_score += enemy.value

                # create new explosion where the shot meets the enemy

                # it is needed to update animation to init first texture
                # otherwise draw will be called before update_animation

                shot.kill()
                print("Enemy killed!!!!!!!!!!!")
                # Adds a point to the score

        # Check for collisions between the player and the enemies
        player_collisions = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list)

        if len(player_collisions) > 0:

            # Kill enemies by redefining self.enemy_list
            for enemy in player_collisions:

                enemy.kill()

                # Remove in life from PLAYER_LIVES
                self.player_lives -= 1

                if self.player_lives > 0:
                    self.reset_level()
                    break

                else:
                    self.setup()
                    print("GAME RESET")
                    break

        if self.player_score >= self.score_for_level_up:
            LEVEL += 1
            self.player_score = 0
            self.score_for_level_up = random.randint(5, 10)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        # Track state of arrow keys
        if key == arcade.key.UP:
            # self.up_pressed = True
            # changes the angle of the player
            self.player_sprite.angle = 0

        elif key == arcade.key.DOWN:
            # self.down_pressed = True
            self.player_sprite.angle = 180

        elif key == arcade.key.LEFT:
            # self.left_pressed = True
            self.player_sprite.angle = 90

        elif key == arcade.key.RIGHT:
            # self.right_pressed = True
            self.player_sprite.angle = 270

        if key == arcade.key.R:

            self.player_sprite.ammo = PLAYER_DEFAULT_AMMO

        if key == arcade.key.SPACE:

            # Creates a new shot
            if (self.player_sprite.ammo > 0):
                self.player_sprite.ammo -= 1
                new_shot = PlayerShot(self.player_sprite,
                                      self.player_shot_textures)
                self.player_shot_list.append(new_shot)
            else:
                print("no ammo left")
            # Adds the shot to the list of shots

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released.
        """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def reset_level(self):
        """
        Function to reset a level.
        """
        # Removes all the enemies
        self.enemy_list = arcade.SpriteList()

        # Define self.player.explode
        self.player_sprite.explode()

    def new_explosion(self, x, y):

        # Create explosion
        explosion = arcade.AnimatedTimeSprite(
            scale=0.5,
            center_x=x,
            center_y=y,
        )

        # make list of textures
        explosion.textures = []

        # add our explosion textures to the textures list
        explosion.textures = self.explosion_textures
        explosion.angle = random.randint(0, 360)

        # updates the animation to get first texture
        explosion.update_animation()

        # adds explosion to explosion list
        self.explosions_list.append(explosion)


def main():
    """
    Main method
    """

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
