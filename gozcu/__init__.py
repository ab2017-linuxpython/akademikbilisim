def ana_fonksyon():
    veri = input("Bir veri giriniz: ")
    print("Girdiğiniz veri: {}".format(veri))
    print("Girdiğiniz verinin uzunluğu: {}".format(len(veri)))
    ty = str  # default olarak herşey string
    for possible_ty in (int, float):
        try:
            possible_ty(veri)
        except ValueError:
            continue
        else:
            ty = possible_ty
            break
    print("Girdiğiniz verinin tahmini türü: {}".format(ty.__name__))

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
