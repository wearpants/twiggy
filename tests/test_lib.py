import unittest
import threading

from twiggy import lib

from . import when

class ThreadNameTest(unittest.TestCase):

    def test_thread_name(self):
        def doit():
            self.name = lib.thread_name()
        
        t = threading.Thread(target=doit, name="Bob")
        t.start()
        t.join()
        assert self.name == "Bob"

class IsoTimeTest(unittest.TestCase):
    
    def test_iso_time(self):
        assert lib.iso8601time(when) == "2010-10-28T02:15:57Z" 
