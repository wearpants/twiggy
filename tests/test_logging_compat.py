import os
import sys
from unittest import TestCase

def setup_module():
    from twiggy import _populate_globals
    _populate_globals()

def teardown_module():
    from twiggy import _del_globals
    _del_globals()

class HijackTest(TestCase):

    def compare_modules(self, m1, m2):
        self.failUnlessEqual(m1.__name__, m2.__name__)
        
    def verify_orig(self):
        import logging
        from twiggy.logging_compat import orig_logging
        self.compare_modules(logging, orig_logging)
        
    def verify_comp(self):
        import logging
        from twiggy import logging_compat
        self.compare_modules(logging, logging_compat)

    def tearDown(self):
        sys.modules.pop('logging', None)

    def test_hijack(self):
        from twiggy.logging_compat import hijack
        self.verify_orig()
        hijack()
        self.verify_comp()

    def test_restore(self):
        from twiggy.logging_compat import hijack, restore
        hijack()
        restore()
        self.verify_orig()

class TestGetLogger(TestCase):
    
    def test_name(self):
        from twiggy.logging_compat import getLogger
        self.failUnlessEqual(getLogger("spam")._logger._fields["name"], "spam")
    
    def test_root(self):
        from twiggy.logging_compat import getLogger, root
        self.failUnlessEqual(getLogger(), root)

    def test_cache(self):
        from twiggy.logging_compat import getLogger
        eggs = getLogger("eggs")
        self.failUnless(getLogger("eggs") is eggs)
        
class TestFakeLogger(TestCase):
    
    def setUp(self):
        from twiggy import add_emitters
        from twiggy.logging_compat import getLogger, DEBUG
        from twiggy.outputs import ListOutput
        self.logger = getLogger("spam")
        self.logger.setLevel(DEBUG)
        self.list_output = ListOutput()
        self.messages = self.list_output.messages
        add_emitters(("spam", DEBUG, None, self.list_output))

    def test_level(self):
        from twiggy.logging_compat import INFO, ERROR
        for level in [INFO, ERROR]:
            self.logger.setLevel(level)
            self.failUnlessEqual(self.logger.level, level)
            
    def test_percent(self):
        self.failUnlessEqual(self.logger._logger._options["style"], "percent")

    def test_exception(self):
        try:
            1/0
        except:
            self.logger.exception("spam")
        self.failUnless("ZeroDivisionError" in self.messages[0].traceback)

    def test_isEnabledFor(self):
        from twiggy.logging_compat import INFO, DEBUG
        self.logger.setLevel(INFO)
        self.failIf(self.logger.isEnabledFor(DEBUG))
        self.logger.setLevel(DEBUG)
        self.failUnless(self.logger.isEnabledFor(DEBUG))

    def test_log_no_exc_info(self):
        self.logger.info("nothing", exc_info=True)
        self.failUnlessEqual(self.messages[0].traceback, None)

    def test_log_exc_info(self):
        try:
            1/0
        except:
            self.logger.error("exception", exc_info=True)
        self.failUnless("ZeroDivisionError" in self.messages[0].traceback)
        
    def test_basicConfig(self):
        from twiggy.logging_compat import basicConfig
        self.failUnlessRaises(RuntimeError, basicConfig)

    def test_log(self):
        from twiggy.logging_compat import INFO, ERROR
        for index, level in enumerate((INFO, ERROR)):
            self.logger.log(level, "spam")
            self.failUnlessEqual(self.messages[index].text, "spam")
            self.failUnlessEqual(self.messages[index].level, level)

    def test_log_bad_level(self):
        self.failUnlessRaises(ValueError, self.logger.log, "illegal level", "eggs")
        
class TestLoggingBridge(TestCase):
    
    def test_format(self):
        from twiggy import add_emitters
        from twiggy import log
        from twiggy.logging_compat import LoggingBridgeFormat, DEBUG, ERROR
        from twiggy.outputs import ListOutput
        logger = log.name("spam")
        list_output = ListOutput(format=LoggingBridgeFormat())
        messages = list_output.messages
        add_emitters(("spam", DEBUG, None, list_output))
        logger.error("eggs")
        self.failUnlessEqual(messages[0], ('|eggs\n', ERROR, 'spam'))
        
    def test_sanity(self):
        from twiggy import add_emitters, log
        from twiggy.logging_compat import LoggingBridgeOutput, DEBUG
        logger = log.name("decoy")
        add_emitters(("decoy", DEBUG, None, LoggingBridgeOutput()))
        logger.error("spam")
        logger.notice("eggs")
