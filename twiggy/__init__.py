__all__=['log', 'Levels']
import time

import Logger

log = Logger.Logger({'time':time.time})
emitters = log.emitters

#log.name('pants').fields(shirt=42, request_id='webtastic').info('Frobbing {0} with great {adj}', 666, 'temptation')
#log.name('structure').fields(numcalls=82, params = someargs).info()