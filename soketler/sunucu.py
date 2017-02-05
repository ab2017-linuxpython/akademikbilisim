from socket import *

sunucuAd, sunucuPort = 'localhost', 12345
sunucuSocket = socket(AF_INET, SOCK_DGRAM)
sunucuSocket.bind((sunucuAd, sunucuPort))  # soketi verilen port üzerinden hosta bağlar
print('Sunucu veri almaya hazırdır')

isimler = {"b": "Büyült", "k": "Küçült", "ç": "Çıkış"}
islemler = {"b": str.upper, "k": str.lower, "ç": lambda x: "abisendekapansana"}

while True:
    mesaj, istemciAdres = sunucuSocket.recvfrom(4096)  # recvfrom(): mesajı alır
    op, mesaj = mesaj.decode().split("-")
    print("İstemciden {} işlemi için mesaj alındı: ".format(isimler[op]), mesaj)
    yeniMesaj = islemler[op](mesaj)
    print("Mesaj istemciye geri gönderilecek: ", yeniMesaj)
    yeniMesaj = yeniMesaj.encode()
    sunucuSocket.sendto(yeniMesaj, istemciAdres)
    if op == "ç":
        break
print("Kapatma mesajı alındı. Sunucu kapanıyor.")
sunucuSocket.close()  # soketi kapatır
print("Sunucu kapandı.")
