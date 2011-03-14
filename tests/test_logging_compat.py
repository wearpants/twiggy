import sys
import logging as orig_logging
from unittest import TestCase
from twiggy import logging_compat, log
from twiggy.logging_compat import hijack, restore, hijackContext, getLogger

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
        
    def test_hijackContext(self):
        with hijackContext():
            self.verify_comp()
        self.verify_orig()

class TestGetLogger(TestCase):
    
    def test_name(self):
        self.failUnlessEqual(getLogger("spam")._fields["name"], "spam")
    
    def test_root(self):
        self.failUnlessEqual(getLogger(), log)
