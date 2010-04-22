__all__=['log']
import time
import sys

import Logger
import Emitter
import Formatter
import Outputter

log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

def quick_setup(min_level=Levels.DEBUG, file = None, async = False):
    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        format = Formatter.LineFormatter(conversion=Formatter.shell_conversion)
        outputter = Outputter.StreamOutputter(format, async = async, stream=file)
    else:
        format = Formatter.LineFormatter(conversion=Formatter.line_conversion)
        outputter = Outputter.FileOutputter(format, async = async, name=file, mode='a', )

    emitters['*'] = Emitter.Emitter(min_level, True, outputter)
