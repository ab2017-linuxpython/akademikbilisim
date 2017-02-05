import sys
dosya = open("cikti.txt","a+")
a = sys.stdout
sys.stdout=dosya
print("hello world33333")
sys.stdout=a



file= open("deneme.txt","a+")


file.write("hello world2\n")

file.flush()
print("akademik bilisim",file=file)
print("imlecin yeri {}".format(file.tell()))
file.seek(5)
print("imleci yeri {}".format(file.tell()))


file.close()

dosya.close()

with open("run.py", "r") as dosyam:
    print("---")
    satirlar = [satir[:-1] for satir in dosyam.readlines() if not satir.startswith(" ") and
                satir[:-1]]
    print(satirlar)
    print("---")
    print("dosyam kapandı mı? {}".format(dosyam.closed))
print("dosyam kapandı mı? {}".format(dosyam.closed))
