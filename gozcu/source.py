import os
import signal
import sys
import time
import argparse

import logging
import logging.handlers
import psutil

__all__ = ["get_args", "connect_signals", "monitor"]

logger = logging.getLogger(__name__)


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


def get_args(argv):
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

    parser.add_argument("-d", "--debug",
                        help="Activate debug logger",
                        action="store_true", default=False)

    parser.add_argument("-l", "--debug_level",
                        help="Change debug level",
                        choices=["CRITICAL", "WARNING", "ERROR", "INFO", "DEBUG"],
                        default="INFO")

    return parser.parse_args(argv)


def handle_logger(arglar):
    logger.setLevel(logging._nameToLevel[arglar.debug_level])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.handlers = []
    if arglar.debug:
        handler = logging.handlers.RotatingFileHandler(filename="output.log",
                                                               maxBytes=1024*1024,
                                                               backupCount=3)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    else:
        logger.addHandler(logging.NullHandler())


_wait = False


def connect_signals():
    def handle_sigint(sig, stack):
        """When user sends SIGINT (via Ctrl-C) we ask if it's sure or not"""
        logger.info("Signal received")
        global _wait  # If we're already interrupted, just exit and keep it in the global variables
        if _wait:
            logger.debug("_wait is already set, exiting")
            print()
            exit(20)
        _wait = True
        logger.debug("_wait variable set")
        choice = input("\rAre you sure you want to exit? (y/N)").lower()
        if choice == "y":
            exit(0)

        logger.debug("_wait variable unset")
        _wait = False
        logger.debug("User said {}, continuing".format(choice))

    signal.signal(signal.SIGINT, handle_sigint)
    logger.info("Sigint connected")


def monitor(arglar):
    logger.info("Starting main loop")
    while True:
        if arglar.mode in "ca":
            cpu_reading = max(psutil.cpu_percent(arglar.resolution, percpu=True))
            logger.debug("Cpu percents {}".format(cpu_reading))
            if cpu_reading > arglar.cpu_crit:
                logger.debug("Cpu percentage is higher than critical level")
                print("CPU usage is high", file=arglar.crit_out)
            elif arglar.cpu_warn is not None and cpu_reading > arglar.cpu_warn:
                logger.debug("Cpu percentage is higher than warning level")
                print("CPU usage is critical", file=arglar.warn_out)

        if arglar.mode in "ra":
            ram_reading = psutil.virtual_memory().percent
            logger.debug("Sleeping")
            if ram_reading > arglar.ram_crit:
                logger.debug("Ram percentage is higher than critical level")
                print("RAM usage is high", file=arglar.crit_out)
            elif arglar.ram_warn is not None and ram_reading > arglar.ram_warn:
                logger.debug("Ram percentage is higher than warning level")
                print("RAM usage is critical", file=arglar.warn_out)

        logger.debug("Sleeping")
        time.sleep(arglar.resolution)
