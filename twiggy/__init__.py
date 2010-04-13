__all__=['log']
import time
import sys

import Logger
import Emitter
import Formatter
import Outputter

log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

def quick_setup(min_level=Levels.DEBUG, file = None):
    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        conversion = Formatter.shell_conversion
        writer = file.write
    else:
        conversion = Formatter.line_conversion
        writer = open(file, 'a').write

    format = Formatter.LineFormatter(conversion=conversion).format
    outputter = Outputter.Outputter(format, writer)

    emitters['*'] = Emitter.Emitter(min_level, True, outputter)
