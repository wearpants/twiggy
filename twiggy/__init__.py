__all__=['log']
import time

import Logger
import Emitter

log = Logger.Logger({'time':time.gmtime})
emitters = log.emitters

def basicConfig(min_level=Levels.DEBUG):
    emitters['*'] = Emitter.Emitter2(min_level, True,
                                     Emitter.LineFormatter().format,
                                     Emitter.printer)