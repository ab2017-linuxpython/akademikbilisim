import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("ipecho.net", 80))  # ipecho.net'in ip'sini DNS sunucularından otomatik alıyor
    s.sendall(b"GET http://ipecho.net/plain\r\n")  # Klasik bir HTTP 1.1 isteği
    response = s.recv(1024).decode()  # Gelen cevabı okuyor ve utf-8'e çeviriyoruz

print("Dış ağ IP adresiniz {}".format(response))