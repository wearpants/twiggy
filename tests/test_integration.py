from __future__ import print_function
import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
import twiggy
import time

from . import when
from twiggy.compat import StringIO

def fake_gmtime():
    return when

class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        twiggy._populate_globals()
        twiggy.log._fields['time'] = fake_gmtime
    
    def tearDown(self):
        twiggy._del_globals()

    def test_integration(self):
        everything = twiggy.outputs.StreamOutput(stream=StringIO(), format=twiggy.formats.line_format)
        out1 = twiggy.outputs.StreamOutput(stream=StringIO(), format=twiggy.formats.line_format)
        out2 = twiggy.outputs.StreamOutput(stream=StringIO(), format=twiggy.formats.line_format)
        
        twiggy.add_emitters(('*', twiggy.levels.DEBUG, None, everything),
                           ('first', twiggy.levels.INFO, None, out1),
                           ('second', twiggy.levels.DEBUG, twiggy.filters.glob_names('second.*'), out2),
                           ('first-filter', twiggy.levels.DEBUG, ".*pants.*", out1))
        
        def something():
            return "something cool"
        
        twiggy.log.debug("oh hi")
        twiggy.log.name("second").info("do you like cheese?")
        twiggy.log.name("second.child").fields(cheese="hate").warning("No")
        twiggy.log.name("first").error("Can you do {0}", something)
        twiggy.log.name("bob").debug("I wear pants")
        
        try:
            raise RuntimeError("Oh Noes!")
        except:
            twiggy.log.trace().critical("Went boom")

        print("***************** everything **********************")
        print(everything.stream.getvalue(), end=' ')
        print("****************** out 1 **************************")
        print(out1.stream.getvalue(), end=' ')
        print("****************** out 2 **************************")
        print(out2.stream.getvalue(), end=' ')       
        print("***************************************************")
        

        # XXX this should really be done with a regex, but I'm feeling lazy
        assert out1.stream.getvalue().startswith( \
"""2010-10-28T02:15:57Z:INFO:second|do you like cheese?
2010-10-28T02:15:57Z:WARNING:second.child:cheese=hate|No
2010-10-28T02:15:57Z:ERROR:first|Can you do something cool
2010-10-28T02:15:57Z:DEBUG:bob|I wear pants
2010-10-28T02:15:57Z:CRITICAL|Went boom
TRACE Traceback (most recent call last):
""")
#"""TRACE   File "/home/pfein/Projects/python-twiggy/tests/test_integration.py", line 39, in test_integration
        assert out1.stream.getvalue().endswith( \
"""TRACE     raise RuntimeError("Oh Noes!")
TRACE RuntimeError: Oh Noes!
""")
        

        assert out2.stream.getvalue() == \
"""2010-10-28T02:15:57Z:WARNING:second.child:cheese=hate|No
"""

