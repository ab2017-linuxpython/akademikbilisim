def typed_input(typ, prompt=None, extra_tries=3):
    for i in range(extra_tries + 1):
        veri = input(prompt)
        try:
            veri = typ(veri)
        except ValueError:
            print("Hatalı giriş")
        else:
            return veri
    else:
        raise TypeError("Girdi türü desteklenmiyor")


def ana_fonksyon():
    veri = typed_input(int, "Bir sayı giriniz: ")
    print("Girdiğiniz veri: {}".format(veri))
    print("Girdiğiniz verinin türü: {}".format(int.__name__))

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
