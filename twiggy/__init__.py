__all__=['log']
import time
import sys

import logger
import Emitter
import Formatter
import outputs

## a useful default fields
__fields = {'time':time.gmtime}

#: the magic log object
log = logger.Logger(__fields)

#: the global emitters dictionary
emitters = log._emitters

__internal_format = Formatter.LineFormatter(conversion=Formatter.line_conversion)
__internal_output = outputs.StreamOutputter(__internal_format, stream=sys.stderr)

#: Internal Log - for errors/loging within twiggy
internal_log = logger.InternalLogger(__fields, output=__internal_output).name('twiggy.internal')

#: Twiggy's internal log for use by developers
devel_log = logger.InternalLogger(__fields, output = outputs.NullOutputter()).name('twiggy.devel')

def quick_setup(min_level=Levels.DEBUG, file = None, msgBuffer = 0):
    """Quickly set up `emitters`.

    :arg `levels.Level` min_level: lowest message level to cause output
    :arg string file: filename to log to, or ``sys.stdout``, or ``sys.stderr``
    :arg int msgBuffer: number of messages to buffer, see `outputs.Outputter.msgBuffer`
    """

    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        output = outputs.StreamOutputter(Formatter.shell_format, stream=file)
    else:
        output = outputs.FileOutputter(Formatter.line_format, msgBuffer=msgBuffer, name=file, mode='a')

    emitters['*'] = Emitter.Emitter(min_level, True, output)

def addEmitters(*tuples):
    """add multiple emitters

    ``tuples`` should be (name, min_level, filter, output). See
    :class:`Emitter` for description.
    """
    for name, min_level, filter, output in tuples:
        emitters[name] = Emitter.Emitter(min_level, filter, output)