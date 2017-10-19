import sys
import threading

from twiggy import lib

from . import when

if sys.version_info >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")


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
