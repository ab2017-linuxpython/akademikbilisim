import sys, os


def ana_fonksyon():
    sys.stdout.write("Bir veri giriniz: ")
    sys.stdout.flush()
    veri = sys.stdin.readline()[:-len(os.linesep)]
    sys.stdout.write("Girdiğiniz veri: {}\n".format(veri))
    sys.stdout.write("Girdiğiniz verinin uzunluğu: {}\n".format(len(veri)))
    sys.stdout.flush()
    # temel_turleri_goster()


def temel_turleri_goster():
    s = "hello"
    i = 10
    f = 10.00000001
    t = s, i, f
    l = ["ali", 2.71, 3750000000, t]
    d = {"ismail": "ishmael", "gereksizler": l, "bin": 1000, 55: "ellibeş"}
    la = lambda x, y: x ** y

    def fn(x, y):
        return x ** y

    class c():
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def calculate(self):
            return self.x ** self.y

    ins = c(2, 5)
    print(s, i, f, t, l, d, la, la(2, 5), fn, fn(2, 5), c, ins, ins.calculate(), sep="\n-----\n")
