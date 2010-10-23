import unittest2
from twiggy import log

class LogTestCase(unittest2.TestCase):

    def test_emitting_returns_true(self):
        assert log.debug('hi') is True
        assert log.info('hi') is True
        assert log.notice('hi') is True
        assert log.warning('hi') is True
        assert log.error('hi') is True
        assert log.critical('hi') is True