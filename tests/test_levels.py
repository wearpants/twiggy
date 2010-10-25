import unittest2
from twiggy import levels

class LevelTestCase(unittest2.TestCase):

    def test_name2level(self):
        assert levels.name2level('debug') is levels.DEBUG
        assert levels.name2level('Debug') is levels.DEBUG

    def test_ordering(self):
        assert levels.DEBUG < levels.INFO
        assert levels.INFO < levels.NOTICE
        assert levels.NOTICE < levels.WARNING
        assert levels.WARNING < levels.ERROR
        assert levels.ERROR < levels.CRITICAL
        assert levels.CRITICAL < levels.DISABLED
