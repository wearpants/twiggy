import sys
import logging as orig_logging
from unittest import TestCase
from twiggy import logging_compat, addEmitters, log
from twiggy.outputs import ListOutput
from twiggy.logging_compat import (hijack, restore, basicConfig,
                                   getLogger, root, DEBUG, INFO, ERROR,
                                   LoggingBridgeOutput)

class HijackTest(TestCase):

    def compare_modules(self, m1, m2):
        self.failUnlessEqual(m1.__name__, m2.__name__)
        
    def verify_orig(self):
        import logging
        self.compare_modules(logging, orig_logging)
        
    def verify_comp(self):
        import logging
        self.compare_modules(logging, logging_compat)

    def tearDown(self):
        sys.modules.pop('logging', None)

    def test_hijack(self):
        self.verify_orig()
        hijack()
        self.verify_comp()

    def test_restore(self):
        hijack()
        restore()
        self.verify_orig()

class TestGetLogger(TestCase):
    
    def test_name(self):
        self.failUnlessEqual(getLogger("spam")._logger._fields["name"], "spam")
    
    def test_root(self):
        self.failUnlessEqual(getLogger(), root)

    def test_cache(self):
        eggs = getLogger("eggs")
        self.failUnless(getLogger("eggs") is eggs)
        
class TestFakeLogger(TestCase):
    
    def setUp(self):
        self.logger = getLogger("spam")
        self.logger.setLevel(DEBUG)
        self.list_output = ListOutput()
        self.messages = self.list_output.messages
        addEmitters(("spam", DEBUG, None, self.list_output))

    def test_level(self):
        for level in [INFO, ERROR]:
            self.logger.setLevel(level)
            self.failUnlessEqual(self.logger.level, level)

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
        self.failUnlessRaises(RuntimeError, basicConfig)

    def test_log(self):
        for index, level in enumerate((INFO, ERROR)):
            self.logger.log(level, "spam")
            self.failUnlessEqual(self.messages[index].text, "spam")
            self.failUnlessEqual(self.messages[index].level, level)

    def test_log_bad_level(self):
        self.failUnlessRaises(ValueError, self.logger.log, "illegal level", "eggs")
        
class TestLoggingBridge(TestCase):
    
    def test_sanity(self):
        logger = log.name("spam")
        addEmitters(("spam", DEBUG, None, LoggingBridgeOutput()))
        logger.error("BLBLBLB")
