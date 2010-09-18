__all__=['log']
import time
import sys

import Logger
import Emitter
import Formatter
import Outputter

## the magic log object, for end-users
log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

## Internal Log - for errors/loging within twiggy
internal_format = Formatter.LineFormatter(conversion=Formatter.line_conversion)
internal_outputter = Outputter.StreamOutputter(internal_format, stream=sys.stderr)
internal_log = Logger.InternalLogger({'time':time.gmtime}, outputter=internal_outputter).name('twiggy.internal')

## Twiggy's internal log for use by developers
devel_log = Logger.InternalLogger({'time':time.gmtime}, outputter = Outputter.NullOutputter()).name('twiggy.devel')


def quick_setup(min_level=Levels.DEBUG, file = None, msgBuffer = 0):
    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        format = Formatter.LineFormatter(conversion=Formatter.shell_conversion)
        outputter = Outputter.StreamOutputter(format, stream=file)
    else:
        format = Formatter.LineFormatter(conversion=Formatter.line_conversion)
        outputter = Outputter.FileOutputter(format, msgBuffer=msgBuffer, name=file, mode='a')

    emitters['*'] = Emitter.Emitter(min_level, True, outputter)
