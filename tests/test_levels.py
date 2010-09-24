import unittest2
from twiggy import Levels

class LevelTestCase(unittest2.TestCase):
    
    def test_name2level(self):
        assert Levels.name2level('debug') is Levels.DEBUG
        assert Levels.name2level('Debug') is Levels.DEBUG
    
    def test_ordering(self):
        assert Levels.DEBUG < Levels.INFO
        assert Levels.INFO < Levels.WARNING
        assert Levels.WARNING < Levels.ERROR
        assert Levels.ERROR < Levels.CRITICAL
        assert Levels.CRITICAL < Levels.DISABLED