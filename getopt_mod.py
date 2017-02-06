import getopt

import sys

opts, _ = getopt.getopt(sys.argv[1:], 'hi:', ["help", "x="])

opts = dict(opts)

if "--help" in opts or "-h" in opts:
    print("Kullanım: (-h --help) --x=<deger> -i <tekrar>")
    exit(0)

deger = opts.get("--x", "")
tekrar = int(opts.get("-i", 0))

for j in range(tekrar):
    print(deger)
