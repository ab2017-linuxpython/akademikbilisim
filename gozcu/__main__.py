import sys
import source


def main():
    args = source.get_args(sys.argv[1:])
    source.handle_logger(args)
    source.connect_signals()
    source.monitor(args)


try:
    main()
except Exception as e:
    print("An error occured:", file=sys.stderr)
    print("{cls}({args})".format(cls=type(e).__name__, args=", ".join(e.args)), file=sys.stderr)
    exit(1)
else:
    exit(0)

