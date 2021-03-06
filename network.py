"""

Author: Guy Shuster

Purpose: The module that manages the network connections

Date: 29/12/2020

"""

import socket
import constants
import deserializer

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
        try:
            self.socket.connect((ip, constants.HOST_PORT))
            return True
        except socket.timeout as _:
            return False

    def send_data(self, data):
        try:
            self.socket.sendall(data)
        except OSError as _:
            raise RuntimeError('Socket connection broke')

    def receive_data(self):
        chunks = []
        received_bytes_count = 0

        try:
            message_size = self.socket.recv(constants.MESSAGE_LENGTH_SIZE)
            message_size = deserializer.decode_message_size(message_size)
        except socket.timeout as _:
            raise TimeoutError()
        except OSError as _:
            raise RuntimeError('Socket connection broke')

        while received_bytes_count < message_size:
            try:
                chunk = self.socket.recv(message_size - received_bytes_count)
            except socket.timeout as _:
                raise TimeoutError()
            except OSError as _:
                raise RuntimeError('Socket connection broke')

            if chunk == b'':
                raise RuntimeError('Socket connection broke')

            chunks.append(chunk)
            received_bytes_count = received_bytes_count + len(chunk)
        return b''.join(chunks)

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def disconnect(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except OSError as disconnect_error:
            print(disconnect_error)
