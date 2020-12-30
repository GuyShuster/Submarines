"""

Author: Guy Shuster

Purpose: The module that manages all the game logic and it's dependencies

Date: 29/12/2020

"""

import constants
import input_structure_validator
import board
import network
import serializer
import deserializer


class GameManager:

    def __init__(self):
        self.input_handler = input_structure_validator.InputStructureValidator()
        self.board = board.Board()
        self.network = network.Network()
        self.serializer = serializer.Serializer()
        self.deserializer = deserializer.Deserializer()
        self.host = None

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
            self.host = True
        else:
            while True:
                print(constants.START_COMMUNICATION_IP_PROMPT)
                ip = self.input_handler.get_ip_from_user()
                if self.network.connect_to_host(ip):
                    print(f'Connected to {ip} successfully!')
                    break
                print('Connection timed out, trying again...')
            self.host = False

    def __safe_send(self, data):
        try:
            self.network.send_data(data)
        except RuntimeError as runtime_error:
            print(f'A network error occurred: {runtime_error.__str__()}. Exiting...')
            exit(1)

    def __safe_receive(self, message_size, attempts=1):
        for _ in range(attempts):
            try:
                return self.network.receive_data(message_size)
            except TimeoutError as _:
                continue
            except RuntimeError as runtime_error:
                print(f'A network error occurred: {runtime_error.__str__()}. Exiting...')
                exit(1)

    def synchronize_communication(self):
        self.network.set_timeout(constants.SYNCHRONIZATION_TIMEOUT)
        if self.host:
            for attempt_num in range(constants.MAX_CONNECTION_ATTEMPTS):
                print(f'Synchronizing with client. Attempt number {attempt_num + 1}')
                self.__safe_send(self.serializer.get_hello())
                data = self.__safe_receive(len(self.serializer.get_olleh()))
                if data is None:  # we didn't receive anything
                    continue
                if data != self.serializer.get_olleh():
                    print('The communication had a protocol error. Exiting...')
                    exit(1)
                if data == self.serializer.get_olleh():
                    print('Synchronized successfully!')
                    return
        else:
            print('Waiting for host to synchronize...')
            data = self.__safe_receive(len(self.serializer.get_hello()), attempts=constants.MAX_CONNECTION_ATTEMPTS)
            if data is None or data != self.serializer.get_hello():
                print('The communication had a protocol error. Exiting...')
                exit(1)
            self.__safe_send(self.serializer.get_olleh())
            print('Synchronized successfully!')

    def start_game(self):
        self.network.set_timeout(constants.GAME_TIMEOUT)


    def main_game_loop(self):
        print(constants.GREETING_MESSAGE)
        # self.set_board()
        self.start_communication()
        # self.synchronize_communication()
        # self.start_game()
        # self.network.disconnect()

