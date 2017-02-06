import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = './chat.sock'

sock.connect(server_address)

while True:
    # Send data
    message = input("<< ")
    sock.sendall(message.encode())

    data = sock.recv(1024)
    print('>> {}'.format(data.decode()))

