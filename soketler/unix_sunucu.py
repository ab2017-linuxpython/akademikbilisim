import socket
import sys
import os

server_address = './chat.sock'

# Socket'in daha önce açık olmadığına emin olmamız gerek
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# STREAM yapısı ile Unix Socket'i açıyoruz
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Socketi adrese bağlıyoruz
sock.bind(server_address)

# 1 uygulamanın bağlanabileceği şekilde dinlemeye geçiyoruz
sock.listen(1)

while True:
    print('Waiting')
    connection, client_address = sock.accept()  # Bağlantı bekliyoruz
    print('connected from ', client_address)  # Bağlantı kuruldu

    while True:
        data = connection.recv(1024).decode()
        print('> {}'.format(data))
        if data:
            data = data[::-1]  # yazıyı tersine çeviriyoruz
            print('< {}'.format(data))
            connection.sendall(data.encode())

    connection.close()
