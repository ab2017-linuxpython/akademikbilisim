import os
import signal
import sys
import time
import argparse

import psutil


def file_or_stdio(arg):
    """This is a validator to open files for writing or opening stdio"""
    if os.path.exists(arg) and os.path.isfile(arg):
        try:
            arg = open(arg, "w")
        except:
            argparse.ArgumentTypeError("Unable to open file {}".format(arg))
    elif arg.lower() == "stdout":
        arg = sys.stdout
    elif arg.lower() == "stderr":
        arg = sys.stderr
    return arg


parser = argparse.ArgumentParser(description="Warns user about CPU and RAM usages")

parser.add_argument("-q", "--mode",
                    help="Warn for given type, [C]pu, [R]am, [A]ll",
                    default="A", type=str, choices="CAR")

parser.add_argument("-w", "--cpu_warn",
                    help="Warning level for CPU",
                    default=None, type=int)

parser.add_argument("-e", "--cpu_crit",
                    help="Warning level for CPU",
                    default=80, type=int)

parser.add_argument("-r", "--ram_warn",
                    help="Warning level for RAM",
                    default=None, type=int)

parser.add_argument("-t", "--ram_crit",
                    help="Warning level for RAM",
                    default=60, type=int)

parser.add_argument("-y", "--warn_out",
                    help="Warning output (file path, stdout, stderr)",
                    default="/dev/null", type=file_or_stdio)

parser.add_argument("-u", "--crit_out",
                    help="Critical output (file path, stdout, stderr)",
                    default="stdout", type=file_or_stdio)

parser.add_argument("-o", "--resolution",
                    help="Warning level for CPU",
                    default=0.5, type=float)

arglar = parser.parse_args(sys.argv[1:])


def handle_sigint(sig, stack):
    """When user sends SIGINT (via Ctrl-C) we ask if it's sure or not"""
    global _wait  # If we're already interrupted, just exit and keep it in the global variables
    if _wait:
        print()
        exit(20)
    _wait = True
    choice = input("\rAre you sure you want to exit? (y/N)").lower()
    if choice == "y":
        exit(0)


signal.signal(signal.SIGINT, handle_sigint)

while True:
    if arglar.mode in "ca":
        cpu_reading = max(psutil.cpu_percent(arglar.resolution, percpu=True))
        if cpu_reading > arglar.cpu_crit:
            print("CPU usage is high", file=arglar.crit_out)
        elif arglar.cpu_warn is not None and cpu_reading > arglar.cpu_warn:
            print("CPU usage is critical", file=arglar.warn_out)

    if arglar.mode in "ra":
        ram_reading = psutil.virtual_memory().percent
        if ram_reading > arglar.ram_crit:
            print("RAM usage is high", file=arglar.crit_out)
        elif arglar.ram_warn is not None and ram_reading > arglar.ram_warn:
            print("RAM usage is critical", file=arglar.warn_out)

    time.sleep(arglar.resolution)
