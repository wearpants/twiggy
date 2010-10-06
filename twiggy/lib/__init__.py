import threading
import time

def thread_name():
    """return the name of the current thread"""
    return threading.currentThread().getName()

def iso8601time(gmtime = None):
    """ISO 8601 - it sucks less!"""
    return time.strftime("%Y-%m-%dT%H:%M:%S", gmtime if gmtime is not None else time.gmtime())
