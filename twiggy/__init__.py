__all__=['log']
import time
import sys

import Logger
import Emitter

log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

def quick_setup(min_level=Levels.DEBUG, file = None):
    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        conversion = Emitter.shell_conversion
        writer = file.write
    else:
        conversion = Emitter.line_conversion
        writer = open(file, 'a').write

    format = Emitter.LineFormatter(conversion=conversion).format
    emitters['*'] = Emitter.Emitter(min_level, True, format, writer)
