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

### 27th of November 2019
- player_shots are now animated, the same way as the enemies. by adding update_animation()
- added update_animation to player_shot for animations
- tiles and textures are now soreted alphabatically when using os.listdir using sorted()
    - Example: sorted(os.listdir(path))

### 22nd of November 2019
- Lots of things have happened
- The game now have levels
    - Tach level has its on map and maps are drawn with tiles from kenney.nl
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
