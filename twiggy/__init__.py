__all__=['log', 'emitters', 'addEmitters', 'devel_log', 'filters', 'formats', 'outputs', 'levels', 'quickSetup']
import time
import sys

import logger
import filters
import formats
import outputs
import levels

## a useful default fields
__fields = {'time':time.gmtime}

#: the magic log object
log = logger.Logger(__fields)

#: the global emitters dictionary
emitters = log._emitters

__internal_format = formats.LineFormat(conversion=formats.line_conversion)
__internal_output = outputs.StreamOutput(__internal_format, stream=sys.stderr)

#: Internal Log - for errors/loging within twiggy
internal_log = logger.InternalLogger(__fields, output=__internal_output).name('twiggy.internal')

#: Twiggy's internal log for use by developers
devel_log = logger.InternalLogger(__fields, output = outputs.NullOutput()).name('twiggy.devel')

def quickSetup(min_level=levels.DEBUG, file = None, msg_buffer = 0):
    """Quickly set up `emitters`.

    :arg `levels.Level` min_level: lowest message level to cause output
    :arg string file: filename to log to, or ``sys.stdout``, or ``sys.stderr``
    :arg int msg_buffer: number of messages to buffer, see `outputs.Output.msg_buffer`
    """

    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        output = outputs.StreamOutput(formats.shell_format, stream=file)
    else:
        output = outputs.FileOutput(formats.line_format, msg_buffer=msg_buffer, name=file, mode='a')

    emitters['*'] = filters.Emitter(min_level, True, output)

def addEmitters(*tuples):
    """add multiple emitters

    ``tuples`` should be (name, min_level, filter, output). See
    :class:`Emitter` for description.
    """
    for name, min_level, filter, output in tuples:
        emitters[name] = filters.Emitter(min_level, filter, output)
