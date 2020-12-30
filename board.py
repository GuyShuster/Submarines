"""

Author: Guy Shuster

Purpose: The module that manages the game board

Date: 29/12/2020

"""

import constants
import serializer

class Board:
    BLANK_SIGN = '*'
    SHIP_SIGN = '#'

    def __init__(self):
        self.board = [
            [Board.BLANK_SIGN for _ in range(constants.BOARD_SIZE)]
            for _ in range(constants.BOARD_SIZE)
        ]
        self.ships = []

    def __check_ship_placement(self, row, column):
        return 0 <= row < constants.BOARD_SIZE and \
               0 <= column < constants.BOARD_SIZE and \
               self.board[row][column] != Board.SHIP_SIGN

    @staticmethod
    def __board_iterator(row, column, direction, ship_size):
        if direction == constants.UP:
            for changing_row_index in range(row, row - ship_size, -1):
                yield changing_row_index, column
        elif direction == constants.DOWN:
            for changing_row_index in range(row, row + ship_size):
                yield changing_row_index, column
        elif direction == constants.LEFT:
            for changing_column_index in range(column, column - ship_size, -1):
                yield row, changing_column_index
        elif direction == constants.RIGHT:
            for changing_column_index in range(column, column + ship_size):
                yield row, changing_column_index

    def place_ship(self, row, column, direction, ship_size):
        if not all([self.__check_ship_placement(row, column)
                    for row, column
                    in Board.__board_iterator(row, column, direction, ship_size)]):
            return False
        for row, column in Board.__board_iterator(row, column, direction, ship_size):
            self.board[row][column] = Board.SHIP_SIGN
        self.ships.append({
            'row': row,
            'column': column,
            'direction': direction,
            'ship_size': ship_size
        })
        return True

    def enemy_won_check(self):
        for ship in self.ships:
            if any([self.board[row][column] == Board.SHIP_SIGN
                    for row, column
                    in Board.__board_iterator(ship['row'], ship['column'], ship['direction'], ship['ship_size'])]):
                return False
        return True

    def sunk_ship_test(self):
        ship_to_remove = None
        for ship in self.ships:
            if all([self.board[row][column] == Board.BLANK_SIGN
                    for row, column
                    in Board.__board_iterator(ship['row'], ship['column'], ship['direction'], ship['ship_size'])]):

                ship_to_remove = ship
        if ship_to_remove:
            self.ships.remove(ship_to_remove)
            return True
        return False

    def attack(self, row, column):
        if row < 0 or row >= constants.BOARD_SIZE or column < 0 or column >= constants.BOARD_SIZE:
            print(f'\nThe other player attacked you at {row}, {column}, missed the board completely...')
            print('It is now your turn!\n')
            return serializer.get_miss()

        sign_before_hit = self.board[row][column]  # save the sign
        self.board[row][column] = Board.BLANK_SIGN  # hit

        if self.enemy_won_check():
            print(f'\nThe other player attacked you at {row}, {column}, and won the game.\nBetter luck next time!\n')
            return serializer.get_gg()
        if self.sunk_ship_test():
            print(f'\nThe other player attacked you at {row}, {column}, and sunk your ship...')
            print('It is their turn again now...\n')
            return serializer.get_sink()
        if sign_before_hit == Board.SHIP_SIGN:
            print(f'\nThe other player attacked you at {row}, {column}, and hit your ship...')
            print('It is their turn again now...\n')
            return serializer.get_hit()

        print(f'\nThe other player attacked you at {row}, {column}, and missed!')
        print('It is now your turn!\n')
        return serializer.get_miss()

    def pretty_print_board(self):
        print(f'''\t     {' '.join([str(index) for index in range(constants.BOARD_SIZE)])}''')
        print(f'''\t     {''.join(['- ' for _ in range(constants.BOARD_SIZE)])}''')
        for index, line in enumerate(self.board):
            print(f'''\t{index}  | {' '.join(line)} |''')
        print(f'''\t     {''.join(['- ' for _ in range(constants.BOARD_SIZE)])}''')
