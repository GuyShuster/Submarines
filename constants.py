"""

Author: Guy Shuster

Purpose: A file with al the global constants of the program

Date: 29/12/2020

"""

HOST_PORT = 8765

BOARD_SIZE = 10

NUMBER_OF_SHIPS = 5

SHIPS_SIZES = [2, 3, 3, 4, 5]

UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

GREETING_MESSAGE = '''Welcome! first we'll ask you some questions and then we will start the game.
'''

SET_BOARD_GREETING_MESSAGE = f'''We will start by setting your board. As you might know, 
you have {NUMBER_OF_SHIPS} ships available. Their lengths are: {', '.join([str(size) for size in SHIPS_SIZES])}, 
and you can set them vertically or horizontally. The board is {BOARD_SIZE} * {BOARD_SIZE}, be aware of that.

Now you will be requested to input coordinates for the placement of the ships. The board begins at (0, 0), 
and it is the top left corner. The coordinates (here and during the game itself) must be entered in a comma separated 
manner, for example: 5, 3, where 5 is the row and 3 is a column. 
After entering the coordinates you will be asked to enter a direction of placement.
Directions are {', '.join(DIRECTIONS)} and they stand for UP, DOWN, LEFT and RIGHT.
This will happen for each ship, and then the game will start.
'''
SET_BOARD_COORDINATE_INPUT_PROMPT = '''Please enter the starting coordinates [row, column] for the ship of size'''
SET_BOARD_DIRECTION_PROMPT = '''Please enter the direction of the ship's placement:'''
