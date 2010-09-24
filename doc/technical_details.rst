######################
Technical Details
######################

**********************
Loggers
**********************

Independence of logger instances
================================
But the name has no relation to the object; it's just for human use:

>>> mylog is log.name('alfredo')
False

The internal log
================
:class:`twiggy.logger.InternalLog` just has an output, no emitters.  Using async is highly discouraged.

****************************
Internal optimizations
****************************
it goes fast!

****************************
Stays out of your way
****************************
error handling, safety.  Logging should **never** interrrupt the flow of your main app (ie, cause erorrs).  Reported w/ internal_log

****************************
Concurrency
****************************
what's threadsafe, what's not
