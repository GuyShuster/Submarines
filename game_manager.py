"""

Author: Guy Shuster

Purpose: The module that manages all the game logic and it's dependencies

Date: 29/12/2020

"""

import constants
import input_structure_validator
import board
import network


class GameManager:

    def __init__(self):
        self.input_handler = input_structure_validator.InputStructureValidator()
        self.board = board.Board()
        self.network = network.Network()

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

    def start_communication(self):
        print(constants.START_COMMUNICATION_INPUT_PROMPT)
        host_or_connect = self.input_handler.get_host_or_connect_input()
        if host_or_connect == constants.HOST:
            self.network.listen_for_connections()
        else:
            while True:
                print(constants.START_COMMUNICATION_IP_PROMPT)
                ip = self.input_handler.get_ip_from_user()
                if self.network.connect_to_host(ip):
                    print(f'Connected to {ip} successfully!')
                    break
                print('Connection timed out, trying again...')

    def main_game_loop(self):
        print(constants.GREETING_MESSAGE)
        self.set_board()
        self.start_communication()
        self.network.disconnect()
