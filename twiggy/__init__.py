__all__=['log', 'Levels']
import time

import Logger
import Emitter

log = Logger.Logger({'time':time.time})
emitters = log.emitters

def basicConfig(min_level=Levels.DEBUG):
    emitters['*'] = Emitter.StandardEmitter(min_level)