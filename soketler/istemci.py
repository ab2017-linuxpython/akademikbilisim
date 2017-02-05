from socket import *

sunucuAd, sunucuPort = 'localhost', 12345
istemciSocket = socket(AF_INET, SOCK_DGRAM)  # datagram
while True:
    op = input('İşlem (B)üyült, (K)üçült, (Ç)ık: ').lower()
    if op not in "bkç":
        print("Hatalı Giriş")
        continue
    if op == "ç":
        mesaj = ""
    else:
        mesaj = input('Küçük harfle bir cümle yaz: ')
    mesaj = (op + "-" + mesaj).encode()
    istemciSocket.sendto(mesaj, (sunucuAd, sunucuPort))
    yeniMesaj, sunucuAdres = istemciSocket.recvfrom(4096)
    yeniMesaj = yeniMesaj.decode()
    print("Alınan cevap: {}".format(yeniMesaj))
    if yeniMesaj == "abisendekapansana":
        break
print("Kapatma mesajının cevabı alındı. İstemci kapanıyor.")
istemciSocket.close()
print("İstemci kapandı.")
