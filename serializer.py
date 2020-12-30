"""

Author: Guy Shuster

Purpose: The module that manages the packet serialization

Date: 29/12/2020

"""

import constants


def get_hello():
    return len(constants.HELLO).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(constants.HELLO, encoding=constants.ENCODING)


def get_olleh():
    return len(constants.OLLEH).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder='big') + \
           str.encode(constants.OLLEH, encoding=constants.ENCODING)


def get_bomb(row: int, column: int):
    return len(f'BOMB~{row}~{column}').to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(f'BOMB~{row}~{column}', encoding=constants.ENCODING)


def get_hit():
    return len(constants.HIT).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(constants.HIT, encoding=constants.ENCODING)


def get_miss():
    return len(constants.MISS).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(constants.MISS, encoding=constants.ENCODING)


def get_sink():
    return len(constants.SINK).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(constants.SINK, encoding=constants.ENCODING)


def get_gg():
    return len(constants.GG).to_bytes(constants.MESSAGE_LENGTH_SIZE, byteorder=constants.BYTEORDER) + \
           str.encode(constants.GG, encoding=constants.ENCODING)

