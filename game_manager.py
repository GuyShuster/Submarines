"""

Author: Guy Shuster

Purpose: The module that manages all the game logic and it's dependencies

Date: 29/12/2020

"""

import constants
import input_structure_validator
import board


class GameManager:

    def __init__(self):
        self.input_handler = input_structure_validator.InputStructureValidator()
        self.board = board.Board()

    def set_board(self):
        print(constants.SET_BOARD_GREETING_MESSAGE)
        for ship_size in constants.SHIPS_SIZES:
            while True:
                print(f'{constants.SET_BOARD_COORDINATE_INPUT_PROMPT} {ship_size}:')
                coordinates = self.input_handler.get_coordinates_input()
                print(constants.SET_BOARD_DIRECTION_PROMPT)
                direction = self.input_handler.get_ship_placement_direction_input()
                if self.board.place_ship(*coordinates, direction, ship_size):
                    print(f'Placed ship of size {ship_size}! Current board:\n')
                    self.board.pretty_print_board()
                    break
                print('Your placement was exceeded the board limits or had a collision with another ship. Try again...')

    def main_game_loop(self):
        print(constants.GREETING_MESSAGE)
        self.set_board()
