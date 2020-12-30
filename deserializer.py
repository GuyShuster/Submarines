"""

Author: Guy Shuster

Purpose: The module that manages the packet deserialization

Date: 29/12/2020

"""

import constants


def decode_message_size(message_size):
    return int.from_bytes(message_size[:constants.MESSAGE_LENGTH_SIZE], byteorder=constants.BYTEORDER)


def decode_message(data):
    return data.decode(constants.ENCODING)
