import twiggy.Emitter
twiggy.emitters['*'] = twiggy.Emitter.StandardEmitter(twiggy.Levels.DEBUG)
twiggy.log.debug('OMFG')
twiggy.log.name('alfredo').debug('hello\njulius')
twiggy.log.name('donjuan').fields(pants='sexy').info('hello, ladies')

try:
    1/0
except:
    twiggy.log.error('oh noes', trace="error")