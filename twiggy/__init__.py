import time
import warnings
import sys
import os

from . import logger
from . import filters
from . import formats
from . import outputs
from . import levels
from .lib.validators import _validate_config


__all__ = ['log', 'emitters', 'add_emitters', 'addEmitters', 'devel_log', 'filters', 'formats',
           'outputs', 'levels', 'quick_setup', 'quickSetup', 'dict_config']


# globals creation is wrapped in a function so that we can do sane testing
def _populate_globals():
    global __fields, log, emitters, __internal_format, __internal_output, internal_log, devel_log

    try:
        log
    except NameError:
        pass
    else:
        raise RuntimeError("Attempted to populate globals twice")

    # a useful default fields
    __fields = {'time': time.gmtime}

    log = logger.Logger(__fields)

    emitters = log._emitters

    internal_log = logger.internal_log

    devel_log = logger.InternalLogger(fields=__fields, output=outputs.NullOutput()
                                      ).name('twiggy.devel')


def _del_globals():
    global __fields, log, emitters, internal_log, devel_log
    del __fields, log, emitters, internal_log, devel_log


if not os.environ.get('TWIGGY_UNDER_TEST', None):  # pragma: no cover
    _populate_globals()


def quick_setup(min_level=levels.DEBUG, file=None, msg_buffer=0):
    """Quickly set up `emitters`.

    quick_setup() quickly sets up logging with reasonable defaults and minimal customizablity.
    Quick setup is limited to sending all messages to a file, ``sys.stdout`` or ``sys.stderr``.
    A timestamp will be prefixed when logging to a file.

    :arg `.LogLevel` min_level: lowest message level to cause output
    :arg string file: filename to log to, or ``sys.stdout``, or ``sys.stderr``.  ``None`` means
        standard error.
    :arg int msg_buffer: number of messages to buffer, see `.outputs.AsyncOutput.msg_buffer`
    """

    if file is None:
        file = sys.stderr

    if file is sys.stderr or file is sys.stdout:
        output = outputs.StreamOutput(formats.shell_format, stream=file)
    else:
        output = outputs.FileOutput(file, format=formats.line_format,
                                    msg_buffer=msg_buffer, mode='a')

    emitters['*'] = filters.Emitter(min_level, True, output)


def quickSetup(*args, **kwargs):
    warnings.warn(
        "twiggy.quickSetup is deprecated in favor of twiggy.quick_setup",
        DeprecationWarning, stacklevel=2)
    return quick_setup(*args, **kwargs)


def dict_config(config):
    """
    Configure twiggy logging via a dictionary

    :arg config: a dictionary which configures twiggy's outputs and emitters.  See
        :attr:`TWIGGY_CONFIG_SCHEMA` for details of the format of the dict.

    .. seealso:: :ref:`dict_config` for a thorough explanation of the outputs and emitters
        concepts from the dictionary

    .. versionadded: 0.5
    """
    cfg = _validate_config(config)

    cfg_outputs = {}
    for name, output in cfg['outputs'].items():
        output['kwargs']['format'] = output['format']
        cfg_outputs[name] = output['output'](*output['args'], **output['kwargs'])

    cfg_emitters = []
    for name, emitter in cfg['emitters'].items():
        if not emitter['filters']:
            filters = None
        else:
            filters = []
            for filter_ in emitter['filters']:
                filters.append(filter_['filter'](*filter_['args'], **filter_['kwargs']))

        cfg_emitters.append((name, emitter['level'], filters, cfg_outputs[emitter['output_name']]))

    if not cfg['incremental']:
        emitters.clear()
    add_emitters(*cfg_emitters)


def add_emitters(*tuples):
    """
    Add multiple emitters

    ``tuples`` should be ``(name_of_emitter, min_level, filter, output)``.
    The last three are passed to :class:`.Emitter`.
    """
    for name, min_level, filter, output in tuples:
        emitters[name] = filters.Emitter(min_level, filter, output)


def addEmitters(*args, **kwargs):
    warnings.warn(
        "twiggy.addEmitters is deprecated in favor of twiggy.add_emitters",
        DeprecationWarning, stacklevel=2)
    return add_emitters(*args, **kwargs)
