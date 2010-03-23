import twiggy.Emitter
twiggy.emitters['*'] = twiggy.Emitter.StandardEmitter(twiggy.Levels.DEBUG)
twiggy.log.debug('OMFG')
twiggy.log.name('alfredo').debug('hello\njulius')

try:
    1/0
except:
    twiggy.log.error('oh noes', trace="error")