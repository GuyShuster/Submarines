"""

Author: Guy Shuster

Purpose: The module that manages the game board

Date: 29/12/2020

"""

import constants


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

    def pretty_print_board(self):
        print(f'''\t {' '.join([str(index) for index in range(constants.BOARD_SIZE)])}''')
        print(f'''\t {''.join(['- ' for _ in range(constants.BOARD_SIZE)])}''')
        for index, line in enumerate(self.board):
            print(f'''{index}  | {' '.join(line)} |''')
        print(f'''\t {''.join(['- ' for _ in range(constants.BOARD_SIZE)])}''')
