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
                    print(f'\nConnected to {ip} successfully!\n')
                    break
                print('\nConnection timed out, trying again...\n')
            self.host = False

    def __safe_send(self, data):
        try:
            self.network.send_data(data)
        except RuntimeError as runtime_error:
            print(f'A network error occurred: {runtime_error.__str__()}. Exiting...')
            exit(1)

    def __safe_receive(self, attempts=1):
        for _ in range(attempts):
            try:
                return self.network.receive_data()
            except TimeoutError as _:
                continue
            except RuntimeError as runtime_error:
                print(f'A network error occurred: {runtime_error.__str__()}. Exiting...')
                exit(1)

    def synchronize_communication(self):
        self.network.set_timeout(constants.SYNCHRONIZATION_TIMEOUT)
        if self.host:
            for attempt_num in range(constants.MAX_CONNECTION_ATTEMPTS):
                print(f'\nSynchronizing with client. Attempt number {attempt_num + 1}\n')
                self.__safe_send(serializer.get_hello())
                data = self.__safe_receive()
                if data is None:  # we didn't receive anything
                    continue
                data = deserializer.decode_message(data)
                if data != constants.OLLEH:
                    print('\nThe communication had a protocol error. Exiting...\n')
                    exit(1)
                if data == constants.OLLEH:
                    print('\nSynchronized successfully!\n')
                    return
        else:
            print('\nWaiting for host to synchronize...\n')
            data = self.__safe_receive(attempts=constants.MAX_CONNECTION_ATTEMPTS)
            if data is None or deserializer.decode_message(data) != constants.HELLO:
                print('\nThe communication had a protocol error. Exiting...\n')
                exit(1)
            self.__safe_send(serializer.get_olleh())
            print('\nSynchronized successfully!\n')

    def __bomb(self):
        print(f'{constants.GAME_COORDINATE_INPUT_PROMPT}:')
        coordinates = self.input_handler.get_coordinates_input()
        self.__safe_send(serializer.get_bomb(*coordinates))

    def start_game(self):
        self.network.set_timeout(constants.GAME_TIMEOUT)
        if self.host:
            print('\nYou are the host so you will begin the game.\n')
            self.__bomb()
        else:
            print('\nPlease wait for the host to make a move...\n')

        while True:
            data = self.__safe_receive()
            if data is None:
                print('\nThe communication timed out. Exiting...\n')
                exit(1)
            data = deserializer.decode_message(data)

            if 'BOMB' in data:
                coordinates = data.split('~')[1:]
                if len(coordinates) == 2 and \
                        all([self.input_handler.check_if_number(coordinate) for coordinate in coordinates]):
                    response_to_attack = self.board.attack(*[int(coordinate) for coordinate in coordinates])
                    if response_to_attack == serializer.get_gg():
                        break
                    self.__safe_send(response_to_attack)
                    print('\nYour current board:\n')
                    self.board.pretty_print_board()
                    if response_to_attack == serializer.get_miss():
                        self.__bomb()
                    continue
                else:
                    print('\nThe other player sent a wrong protocol message\n')

            if data == constants.GG:
                print('\nYOU WON! Congratulations!\n')
                break
            if data == constants.MISS:
                print('\nOops, you missed. It is their turn now...\n')
                print('\nYour current board:\n')
                self.board.pretty_print_board()
                continue
            if data == constants.HIT:
                print('\nNice, you hit their boat. It is your turn again...\n')
                self.__bomb()
                print('\nYour current board:\n')
                self.board.pretty_print_board()
                continue
            if data == constants.SINK:
                print('\nWoah, you sunk their boat! Awesome. It is your turn again...\n')
                self.__bomb()
                print('\nYour current board:\n')
                self.board.pretty_print_board()
                continue

    def main_game_loop(self):
        print(constants.GREETING_MESSAGE)
        self.set_board()
        self.start_communication()
        self.synchronize_communication()
        self.start_game()
        self.network.disconnect()


