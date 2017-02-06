import os
import signal
import sys
import time

import psutil


mode = input("Warn for [C]pu, [R]am, [A]ll (default: A): ").lower()
if mode not in "car":
    print("Unknown Mode", file=sys.stderr)
    exit(1)
elif not mode:
    mode = "a"

if mode in "ca":
    cpu_warn = input("Warning level for CPU (defaut: None): ")
    if cpu_warn and not cpu_warn.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif cpu_warn:
        cpu_warn = int(cpu_warn)
    else:
        cpu_warn = None

    cpu_crit = input("Warning level for CPU (defaut: 80): ")
    if cpu_crit and not cpu_crit.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif cpu_crit:
        cpu_crit = int(cpu_crit)
    else:
        cpu_crit = 80

if mode in "ra":
    ram_warn = input("Warning level for RAM (defaut: None): ")
    if ram_warn and not ram_warn.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif ram_warn:
        ram_warn = int(ram_warn)
    else:
        ram_warn = None

    ram_crit = input("Warning level for RAM (defaut: 60): ")
    if ram_crit and not ram_crit.isdigit():
        print("Unknown Level", file=sys.stderr)
        exit(2)
    elif ram_crit:
        ram_crit = int(ram_crit)
    else:
        ram_crit = 60

warn_out = input("Warning output [file path, stdout, stderr] (default:None): ").lower()
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
else:
    warn_out = None

crit_out = input("Critical output [file path, stdout, stderr] (default:stdout): ").lower()
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
else:
    crit_out = sys.stdout

resolution = input("Reading resolution (default:0.5): ")
if resolution:
    try:
        resolution = float(resolution)
    except ValueError:
        print("Invalid resolution {}".format(resolution))
        exit(4)
else:
    resolution = 0.5

wait = False


def handle_sigint(sig, stack):
    global wait
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

