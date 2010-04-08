__all__=['log']
import time

import Logger
import Emitter

log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

def quick_setup(min_level=Levels.DEBUG, fname = None):
    if fname is None:
        writer = Emitter.printer
    else:
        writer = open(fname, 'a').write

    emitters['*'] = Emitter.Emitter(min_level, True,
                                    Emitter.LineFormatter().format,
                                    writer)