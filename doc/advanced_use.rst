###############
Advanced Uses
###############

***************
Dynamic!
***************

Any functions in args/fields are called and the value substitued:

>>> import os
>>> from twiggy.lib import thread_name
>>> thread_name()
'MainThread'
>>> log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name) #doctest:+ELLIPSIS
INFO:pid=...:I'm in thread MainThread

This can be useful with partially-bound loggers, which let's us do some cool stuff:

>>> class ThreadTracker(object):
...     def __init__(self, obj):
...         self.__obj = obj
...         # a partially bound logger
...         self.__log = log.name("tracker").fields(obj_id=id(obj), thread=thread_name)
...         self.__log.debug("started tracking")
...     def __getattr__(self, attr):
...         self.__log.debug("accessed {0}", attr)
...         return getattr(self.__obj, attr)
...
>>> class Bunch(object):
...     pass
...
>>> foo = Bunch()
>>> foo.bar = 42
>>> tracked = ThreadTracker(foo) #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=MainThread:started tracking
>>> tracked.bar #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=MainThread:accessed bar
42
>>> import threading
>>> t=threading.Thread(target = lambda: tracked.bar * 2, name = "TheDoubler")
>>> t.start(); t.join() #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=TheDoubler:accessed bar

If you really want to log a callable, repr() it or wrap it in lambda.

*******************
Features
*******************
Twiggy supports adding additional functionality to :data:`log` using features.



