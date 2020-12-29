"""

Author: Guy Shuster

Purpose: The module that manages the packet serialization

Date: 29/12/2020

"""

import constants


class Serializer:

    def __int__(self):
        pass

    def get_hello(self):
        return str.encode('HELLO', encoding=constants.ENCODING)

    def get_olleh(self):
        return str.encode('OLLEH', encoding=constants.ENCODING)

    def get_bomb(self, row: int, column: int):
        return str.encode(f'BOMB~{row}~{column}', encoding=constants.ENCODING)

    def get_hit(self):
        return str.encode('HIT', encoding=constants.ENCODING)

    def get_miss(self):
        return str.encode('MISS', encoding=constants.ENCODING)

    def get_sink(self):
        return str.encode('SINK', encoding=constants.ENCODING)

    def get_gg(self):
        return str.encode('GG', encoding=constants.ENCODING)

