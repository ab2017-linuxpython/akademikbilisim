import getopt
import os
import signal
import sys
import time

import psutil

# def safe_input(prompt=None):
#     try:
#         return input(prompt)
#     except KeyboardInterrupt:
#         print()
#         exit(0)


try:
    opts, _ = getopt.getopt(sys.argv[1:], 'hq:w:e:r:t:y:u:o',
                            ["help", "mode=", "cpu_warn=", "cpu_crit=", "ram_warn=",
                             "ram_crit=", "warn_out=", "crit_out=", "resolution="])
except getopt.GetoptError as e:
    print(e, file=sys.stderr, flush=True)
    exit(1)

opts = dict(opts)

if "--help" in opts or "-h" in opts:
    print("2. gün Etüt kullanım talimatları\n"
          "  --help -h        Shows this help\n"
          "  --mode= -q       Warn for [C]pu, [R]am, [A]ll (default: A)\n"
          "  --cpu_warn= -w   Warning level for CPU (defaut: None)\n"
          "  --cpu_crit= -e   Warning level for CPU (defaut: 80)\n"
          "  --ram_warn= -r   Warning level for RAM (defaut: None)\n"
          "  --ram_crit= -t   Warning level for RAM (defaut: 60)\n"
          "  --warn_out= -y   Warning output [file path, stdout, stderr] (default:'/dev/null')\n"
          "  --crit_out= -u   Critical output [file path, stdout, stderr] (default:stdout)\n"
          "  --resolution= -o Reading resolution (default:0.5)\n"
          "Örnek kullanımlar:\n"
          "  python3 odev.py --mode=c -e 90 --resolution=0.1\n"
          "  python3 odev.py -q r -t 80 --resolution=1.5\n"
          )
    exit(0)

mode = opts.get("--mode", opts.get("-q", "a")).lower()
# mode = safe_input("Warn for [C]pu, [R]am, [A]ll (default: A): ").lower()
if mode not in "car":
    print("Unknown Mode {}".format(mode), file=sys.stderr)
    exit(1)

if mode in "ca":
    cpu_warn = opts.get("--cpu_warn", opts.get("w", None))
    # cpu_warn = safe_input("Warning level for CPU (defaut: None): ")
    if cpu_warn and not cpu_warn.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif cpu_warn:
        cpu_warn = int(cpu_warn)

    cpu_crit = opts.get("--cpu_crit", opts.get("e", "80"))
    # cpu_crit = safe_input("Warning level for CPU (defaut: 80): ")
    if cpu_crit and not cpu_crit.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif cpu_crit:
        cpu_crit = int(cpu_crit)
    else:
        cpu_crit = 80

if mode in "ra":
    ram_warn = opts.get("--ram_warn", opts.get("r", None))
    # ram_warn = safe_input("Warning level for RAM (defaut: None): ")
    if ram_warn and not ram_warn.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif ram_warn:
        ram_warn = int(ram_warn)

    ram_crit = opts.get("--ram_crit", opts.get("t", "60"))
    # ram_crit = safe_input("Warning level for RAM (defaut: 60): ")
    if ram_crit and not ram_crit.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif ram_crit:
        ram_crit = int(ram_crit)

warn_out = opts.get("--warn_out", opts.get("y", os.devnull))
# warn_out = safe_input("Warning output [file path, stdout, stderr] (default:'/dev/null'): ").lower()
if os.path.exists(warn_out) and os.path.isfile(warn_out):
    try:
        warn_out = open(warn_out, "w")
    except:
        print("Unable to open file {}".format(warn_out), file=sys.stderr)
        exit(3)
elif warn_out == "stdout":
    warn_out = sys.stdout
elif warn_out == "stderr":
    warn_out = sys.stderr

crit_out = opts.get("--crit_out", opts.get("u", "stdout"))
# crit_out = safe_input("Critical output [file path, stdout, stderr] (default:stdout): ").lower()
if os.path.exists(crit_out) and os.path.isfile(crit_out):
    try:
        crit_out = open(crit_out, "w")
    except:
        print("Unable to open file {}".format(crit_out), file=sys.stderr)
        exit(3)
elif crit_out == "stdout":
    crit_out = sys.stdout
elif crit_out == "stderr":
    crit_out = sys.stderr

resolution = opts.get("--resolution", opts.get("o", 0.5))
# resolution = safe_input("Reading resolution (default:0.5): ")
if resolution:
    try:
        resolution = float(resolution)
    except ValueError:
        print("Invalid resolution {}".format(resolution))
        exit(4)

wait = False


def handle_sigint(sig, stack):
    global wait
    if wait:
        print()
        exit(20)
    wait = True
    choice = input("\rAre you sure you want to exit? (y/N)").lower()
    if choice == "y":
        exit(0)
    else:
        wait = False


signal.signal(signal.SIGINT, handle_sigint)

while True:
    if wait:
        time.sleep(0.1)
        continue
    if mode in "ca":
        cpu_reading = max(psutil.cpu_percent(resolution, percpu=True))
        if cpu_reading > cpu_crit:
            print("CPU kullanımı kritik", file=crit_out)
        elif cpu_warn is not None and cpu_reading > cpu_warn:
            print("CPU kullanımı yüksek", file=warn_out)
    if mode in "ra":
        ram_reading = psutil.virtual_memory().percent
        if ram_reading > ram_crit:
            print("RAM kullanımı kritik", file=crit_out)
        elif ram_warn is not None and ram_reading > ram_warn:
            print("RAM kullanımı yüksek", file=warn_out)
    time.sleep(resolution)
