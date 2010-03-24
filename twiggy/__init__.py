__all__=['log', 'Levels']
import time

import Logger

log = Logger.Logger({'time':time.time})
emitters = log.emitters