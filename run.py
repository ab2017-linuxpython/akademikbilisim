import os
import sys
import signal

import gozcu


def term_handle(sig, stack):
    print("{} numaralı sinyal alındı".format(sig), file=sys.stderr, flush=True)
    exit(100 + sig)


def int_handle(sig, stack):
    print("Kardeş yapma.... Yapma bak....", file=sys.stderr, flush=True)


def usr1_handle(sig, stack):
    print("PID: {}".format(os.getpid()), file=sys.stderr, flush=True)


def usr2_handle(sig, stack):
    sys.stdout = open(os.devnull, "w")


signal.signal(signal.SIGTERM, term_handle)
signal.signal(signal.SIGINT, int_handle)
signal.signal(signal.SIGUSR1, usr1_handle)
signal.signal(signal.SIGUSR2, usr2_handle)

try:
    print("PID: {}".format(os.getpid()))
    gozcu.ana_fonksyon()
except Exception as e:
    print("An error occured:", file=sys.stderr)
    print("{cls}({args})".format(cls=type(e).__name__, args=", ".join(e.args)), file=sys.stderr)
    exit(1)
else:
    exit(0)
