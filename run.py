import sys

import gozcu

try:
    gozcu.ana_fonksyon()
except Exception as e:
    print("An error occured:", file=sys.stderr)
    print("{cls}({args})".format(cls=type(e).__name__, args=", ".join(e.args)), file=sys.stderr)
    exit(1)
else:
    exit(0)
