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

### 22nd of november 2019
- Lots of things have happened
- The game now have levels
    - each level has its on map and maps are drawn with tiles from kenney.nl
    - maps is defined by a list of lists
- Animations
    - The enemies are now animated
        - the enemies have a new function called update_animation()
        - they are still just normal sprites, but with the added functionalty of update_animation()
        - update_animation() increments the cur_texture_index every 0.2 seconds
        - update_animation() for in this case does not have a delta_time variable. I therefore had to make my own.
    - Killing an enemy spawns an explosion
        - an explosion is its own sprite
        - this way it can be used whenever its needed
        - an explosion is an AnimatedTimeSprite from arcade 

### 23rd of October 2019
- Added frame count
- The enemy now has lives

### 9th of October 2019
- The enemy now spawns every second.
- Before this change the enemy would spawn randomly.
