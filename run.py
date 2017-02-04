import sys

import gozcu

try:
    gozcu.ana_fonksyon()
except Exception as e:
    sys.stderr.write("An error occured:\n")
    sys.stderr.write("{cls}({args})\n".format(cls=type(e).__name__, args=", ".join(e.args)))
    sys.stderr.flush()
    exit(1)
else:
    exit(0)
