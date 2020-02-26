# Exercise in creating games in Python
Using the python 3 library **Arcade**

**Python 2 is not supported**

### What have i learned
- Creating a game using **Arcade**
- Rotating a sprite based on its direction (Using sin and cos)
- Calculating an angle towards a destination point using math.atan2
- Working with delta_time in arcades MyGame's on_update() function

## LOG
Log of what has happened

### 26th of February 2020
- Changed the way powerups are handled
  - I now have a list of types each type is a dictionary containing info on the powerup, name, image and modifiers. When coliding with the player each modifier will change whatever the modifier is supposed to change if a powerup does not contain a certain modifier, it is just seen as if it had had the modifier but the value of modification was 0

### 19th of February 2020
- New powerup
  - Changes ENEMY_SPAWN_SPEED by a random amount

### 22nd of January 2020
- The player now has limited ammo
- Added Power Ups:
  - One Power Up gives extra ammo
  - One Power Up gives extra lives

### 27th of November 2019
- player_shots are now animated, the same way as the enemies. by adding update_animation()
- added update_animation to player_shot for animations
- tiles and textures are now sorted alphabetically when using os.listdir using sorted()
    - Example: sorted(os.listdir(path))

### 22nd of November 2019
- Lots of things have happened
- The game now have levels
    - each level has its on map and maps are drawn with tiles from kenney.nl
    - Maps is defined by a list of lists
- Animations
    - The enemies are now animated
        - The enemies have a new function called update_animation()
        - They are still just normal sprites, but with the added functionalty of update_animation()
        - update_animation() increments the cur_texture_index every 0.2 seconds
        - update_animation() for in this case does not have a delta_time variable. I therefore had to make my own.
    - Killing an enemy spawns an explosion
        - An explosion is its own sprite
        - This way it can be used whenever its needed
        - An explosion is an AnimatedTimeSprite from arcade

### 23rd of October 2019
- Added frame count
- The enemy now has lives

### 9th of October 2019
- The enemy now spawns every second.
- Before this change the enemy would spawn randomly.
