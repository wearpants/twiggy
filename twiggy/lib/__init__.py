import threading
import time

def thread_name():
    """return the name of the current thread"""
    return threading.currentThread().getName()

def iso8601time(gmtime = None):
    """convert time to ISO 8601 format - it sucks less!
    
    :arg int gmtime: time in seconds since epoch. If None, use ``time.gmtime()`` (UTC) 
    
    XXX timezone is not supported
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S", gmtime if gmtime is not None else time.gmtime())
