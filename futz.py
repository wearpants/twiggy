import twiggy

twiggy.basicConfig()

# works out of the box; standard levels
twiggy.log.debug('You may not care')
twiggy.log.error('OMFG! Pants on fire!')

# support for format strings
twiggy.log.info('I like %s', "bikes")

# new style too
twiggy.log.info('I wear {0} on my {where}', 'pants', where='legs')

# loggers can have names
twiggy.log.name('alfredo').debug('hello')

# this is not getLogger tho
twiggy.log.name('alfredo') is not twiggy.log.name('alfredo') 

# structured logging
twiggy.log.fields(paths=42).info('Going for a walk')

# short cut
twiggy.log.struct(paths=42, dolphins='thankful')

twiggy.log.name('donjuan').fields(pants='sexy').info('hello, ladies')

try:
    1/0
except:
    twiggy.log.trace('error').error('oh noes')