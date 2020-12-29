"""

Author: Guy Shuster

Purpose: The module that manages the packet deserialization

Date: 29/12/2020

"""

import constants


class Deserializer:

    def __int__(self):
        pass

    def decode(self, data):
        return data.decode(constants.ENCODING)
