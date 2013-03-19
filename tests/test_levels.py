import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
import sys

from twiggy import levels

class LevelTestCase(unittest.TestCase):

    def test_display(self):
        assert str(levels.DEBUG) == 'DEBUG'
        assert repr(levels.DEBUG) == '<LogLevel DEBUG>'

    def test_name2level(self):
        assert levels.name2level('debug') is levels.DEBUG
        assert levels.name2level('Debug') is levels.DEBUG

    def test_less_than(self):
        assert levels.DEBUG < levels.INFO
        assert levels.INFO < levels.NOTICE
        assert levels.NOTICE < levels.WARNING
        assert levels.WARNING < levels.ERROR
        assert levels.ERROR < levels.CRITICAL
        assert levels.CRITICAL < levels.DISABLED

    def test_less_than_equals(self):
        assert levels.DEBUG <= levels.INFO
        assert levels.INFO <= levels.NOTICE
        assert levels.NOTICE <= levels.WARNING
        assert levels.WARNING <= levels.ERROR
        assert levels.ERROR <= levels.CRITICAL
        assert levels.CRITICAL <= levels.DISABLED

    def test_greater_than(self):
        assert levels.INFO > levels.DEBUG
        assert levels.NOTICE > levels.INFO
        assert levels.WARNING > levels.NOTICE
        assert levels.ERROR > levels.WARNING
        assert levels.CRITICAL > levels.ERROR
        assert levels.DISABLED > levels.CRITICAL

    def test_greater_than_equals(self):
        assert levels.INFO >= levels.DEBUG
        assert levels.NOTICE >= levels.INFO
        assert levels.WARNING >= levels.NOTICE
        assert levels.ERROR >= levels.WARNING
        assert levels.CRITICAL >= levels.ERROR
        assert levels.DISABLED >= levels.CRITICAL

    def test_equality(self):
        assert levels.DEBUG == levels.DEBUG
        assert levels.INFO == levels.INFO
        assert levels.NOTICE == levels.NOTICE
        assert levels.WARNING == levels.WARNING
        assert levels.ERROR == levels.ERROR
        assert levels.CRITICAL == levels.CRITICAL

    def test_inequality(self):
        assert not levels.DEBUG != levels.DEBUG
        assert not levels.INFO != levels.INFO
        assert not levels.NOTICE != levels.NOTICE
        assert not levels.WARNING != levels.WARNING
        assert not levels.ERROR != levels.ERROR
        assert not levels.CRITICAL != levels.CRITICAL

        assert levels.INFO != levels.DEBUG
        assert levels.NOTICE != levels.WARNING
        assert levels.WARNING != levels.NOTICE
        assert levels.ERROR != levels.WARNING
        assert levels.CRITICAL != levels.ERROR
        assert levels.DISABLED != levels.CRITICAL

    def test_dict_key(self):
        d={levels.DEBUG:42}
        assert d[levels.DEBUG] == 42

    def test_bogus_not_equals(self):
        assert levels.DEBUG != 1

    @unittest.skipIf(sys.version_info < (3,), "Python 2.x comparisons are insane")
    def test_bogus_compare(self):
        # XXX is there a comparable test for 2.x?
        with self.assertRaises(TypeError):
            levels.DEBUG < 42
