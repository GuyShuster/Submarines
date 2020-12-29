"""

Author: Guy Shuster

Purpose: The module that manages the user input checking and filtration

Date: 29/12/2020

"""

import constants


class InputStructureValidator:

    def __init__(self):
        pass

    def check_if_number(self, num):
        try:
            int(num)
            return True
        except ValueError as _:
            return False

    def get_coordinates_input(self):
        while True:
            coordinates = input()
            comma_separated = coordinates.split(',')
            if len(comma_separated) != 2:
                print('Wrong number of coordinates. Format is: [row, column] (without the parentheses). Try again...')
                continue
            if not all([self.check_if_number(num.strip()) for num in comma_separated]):
                print('One of the coordinates was not a number. Try again...')
                continue
            return tuple([int(num) for num in comma_separated])

    def get_ship_placement_direction_input(self):
        while True:
            direction = input().strip().lower()
            if direction not in constants.DIRECTIONS:
                print(f'''The direction must be one of following {', '.join(constants.DIRECTIONS)}. Try again...''')
                continue
            return direction

    def get_host_or_connect_input(self):
        while True:
            host_or_connect = input().strip().lower()
            options = [constants.HOST, constants.CONNECT]
            if host_or_connect not in options:
                print(f'''The input must be one of following {', '.join(options)}. Try again...''')
                continue
            return host_or_connect

    def get_ip_from_user(self):
        while True:
            ip = input()
            ip_parts = ip.split('.')
            if len(ip_parts) != 4 or not all([self.check_if_number(ip_part) for ip_part in ip_parts]):
                print(f'''An ip address is of the following structure: X.Y.Z.W, all numbers. Try again...''')
                continue
            return ip


