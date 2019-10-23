"""
Simple program to show moving a sprite with the keyboard.

This program uses the Arcade library found at http://arcade.academy

Artwork from https://kenney.nl/assets/space-shooter-redux

"""

import random
import math
import time

import arcade

# Global variables ---------------------------

SPRITE_SCALING = 0.5

# Set the size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Variables controlling the player
PLAYER_LIVES = 3
PLAYER_SPEED_X = 5
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2
PLAYER_SHOT_SPEED = 5
PLAYER_SCORE = 0
# IN PERCENT
CHANCE_OF_ENEMY_SPAWN = 50

GAMESTATE = 1

ENEMY_SPAWN_POINTS = [
    [SCREEN_WIDTH / 2, 0],
    [SCREEN_WIDTH, SCREEN_HEIGHT / 2],
    [SCREEN_WIDTH / 2, SCREEN_HEIGHT],
    [0, SCREEN_HEIGHT / 2]
]

# delta_time in the MyGame updat function is in seconds
# therfore our ENEMY_SPAWN_SPEED is in seconds
ENEMY_SPAWN_SPEED = 1

# ----------------------------------------------

class Player(arcade.Sprite):
    """
    The player
    """

    def __init__(self, center_x=0, center_y=0):
        """
        Setup new Player object
        """

        # Set the graphics to use for the sprite
        super().__init__("images/playerShip1_blue.png", SPRITE_SCALING)

        self.center_x = center_x
        self.center_y = center_y

    def update(self):
        """
        Move the sprite
        """

        # Update center_x
        # self.center_x += self.change_x

        # Don't let the player move off screen
        # if self.left < 0:
        #     self.left = 0
        # elif self.right > SCREEN_WIDTH - 1:
        #     self.right = SCREEN_WIDTH - 1

class PlayerShot(arcade.Sprite):
    """
    A shot fired by the Player
    """

    def __init__(self, player):
        """
        Setup new PlayerShot object
        """

        # Set the graphics to use for the sprite
        super().__init__("images/Lasers/laserBlue01.png", SPRITE_SCALING)

        self.center_x = player.center_x
        self.center_y = player.center_y
        self.change_x = math.cos(player.radians + (math.pi / 2)) * PLAYER_SHOT_SPEED
        self.change_y = math.sin(player.radians + (math.pi / 2)) * PLAYER_SHOT_SPEED
        self.angle = player.angle

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

class Enemy(arcade.Sprite):

    def __init__(self, target):
        """
        Setup new Enemy object
        """

        # Set the graphics to use for the sprite
        super().__init__("./assets/pacman_scaled.png", scale=0.05)

        self.value = 1

        #Picks a random spawn point from the ENEMY_SPAWN_POINTS list
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
        angle = math.atan2(self.dest_y - self.start_y, self.dest_x - self.start_x)

        #Calculates change x and y with cosin and sin
        self.change_x = math.cos(angle)
        self.change_y = math.sin(angle)

        # Rotates the enemy based on the angle
        # The calculations above return the angle in radians
        # But lucky for us the arcade sprite objects has a variable that rotates
        # Based on radians
        self.radians = angle

    def update(self):
        #Updates the sprite by adding change_x and change_y to its position
        self.center_x += self.change_x
        self.center_y += self.change_y

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

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # No points when the game starts
        self.player_score = 0

        # No of lives
        self.player_lives = PLAYER_LIVES

        # Sprite lists
        self.player_shot_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
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

        # Draw the player sprite
        self.player_sprite.draw()

        self.enemy_list.draw()

        # Draw the player shot
        self.player_shot_list.draw()

        # Draw players score on screen
        arcade.draw_text(
            "SCORE: {}".format(self.player_score),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 20,  # Y positon
            arcade.color.WHITE   # Color of text
        )

        arcade.draw_text(
            "LIVES: {}".format(self.player_lives),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 40,  # Y positon
            arcade.color.WHITE   # Color of text
        )

        arcade.draw_text(
            "FPS: {}".format(self.fps),  # Text to show
            10,                  # X position
            SCREEN_HEIGHT - 60,  # Y positon
            arcade.color.WHITE   # Color of text
        )


    def on_update(self, delta_time):
        """
        Movement and game logic

        delta_time: time since previus update in seconds
        """

        # For some reason i have to kinda import the global variable PLAYER_LIVES
        # to change it
        global PLAYER_LIVES

        # Adds delta time to time_since_enemy_spawn and frame_timer
        self.time_since_enemy_spawn += delta_time
        self.frame_timer += delta_time
        
        # Increases frame count
        self.frame_count += 1 

        # print(self.time_since_enemy_spawn)

        # Checks timer
        # Spawns an enemmy if the timer is equal or over ENEMY_SPAWN_SPEED
        if self.time_since_enemy_spawn >= ENEMY_SPAWN_SPEED:
            enemy = Enemy(self.player_sprite)
            self.enemy_list.append(enemy)
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


        # Update player sprite
        self.player_sprite.update()

        # Update the player shots
        self.player_shot_list.update()

        # Update the enemy sprite
        self.enemy_list.update()


        # Loops through each enemy to checks if an enemy has hit a shot
        for enemy in self.enemy_list:
            # Checks if a shot collides with the enemy
            collisions = arcade.check_for_collision_with_list(enemy, self.player_shot_list)
            # Kills the enemy if there is any collisons
            if len(collisions) > 0:
                enemy.kill()
            # Kills each colliding shot
            for shot in collisions:
                self.player_score += enemy.value
                shot.kill()
                print("Enemy killed!!!!!!!!!!!")
                # Adds a point to the score

        # Check for collisions between the player and the enemies
        player_collisions = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

        if len(player_collisions) > 0:
            print("GAMEOVER")
            # Kill player
            # Right now im not killing the player 
            # as i will properly result in a couple of errors
            # self.player_sprite.kill()
            # Remove one live from PLAYER_LIVES
            self.player_lives -= 1
            # Kill enemys
            for enemy in player_collisions:
                enemy.kill()

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


        if key == arcade.key.SPACE:

            # Creates a new shot
            new_shot = PlayerShot(self.player_sprite)
            # Adds the shot to the list of shots
            self.player_shot_list.append(new_shot)

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


def main():
    """
    Main method
    """ 

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
