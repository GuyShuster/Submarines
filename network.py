"""

Author: Guy Shuster

Purpose: The module that manages the network connections

Date: 29/12/2020

"""

import socket
import constants


class Network:

    def __init__(self):
        self.socket = None
        self.address = None

    def listen_for_connections(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            listening_ip = socket.gethostbyname(socket.gethostname())
            s.bind((listening_ip, constants.HOST_PORT))
            s.listen(constants.MAX_CONNECTIONS)
            print(f'Listening on {listening_ip} port {constants.HOST_PORT}')
            self.socket, self.address = s.accept()
            print(f'Client {self.address} connected!')

    def connect_to_host(self, ip):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(constants.DEFAULT_TIMEOUT)
        try:
            self.socket.connect((ip, constants.HOST_PORT))
            return True
        except socket.timeout as _:
            return False

    def send_data(self, data):
        try:
            self.socket.sendall(data)
            return True
        except OSError as socket_error:
            return False

    def receive_data(self):
        pass

    def disconnect(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except OSError as disconnect_error:
            print(disconnect_error)
