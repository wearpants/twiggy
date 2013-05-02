import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
import copy

from twiggy import formats, levels, message

from . import when
   
class ConversionsTestCase(unittest.TestCase):
   
    fields = {
        'time': when,
        'level': levels.INFO,
        'name': 'mylog',
        'pants': 42,
        }
   
    def test_line_conversion(self):
        d = self.fields.copy()
        assert formats.line_format.conversion.convert(d) == '2010-10-28T02:15:57Z:INFO:mylog:pants=42'

        del d['pants']
        assert formats.line_format.conversion.convert(d) == '2010-10-28T02:15:57Z:INFO:mylog'

        del d['name']
        assert formats.line_format.conversion.convert(d) == '2010-10-28T02:15:57Z:INFO'

        del d['level']
        with self.assertRaises(ValueError):
            formats.line_format.conversion.convert(d) 


    def test_shell_conversion(self):
        d = self.fields.copy()
        assert formats.shell_format.conversion.convert(d) == 'INFO:mylog:pants=42'

        del d['pants']
        assert formats.shell_format.conversion.convert(d) == 'INFO:mylog'

        del d['name']
        assert formats.shell_format.conversion.convert(d) == 'INFO'

        del d['level']
        with self.assertRaises(ValueError):
            formats.shell_format.conversion.convert(d) 


class FormatTestCase(unittest.TestCase):

    fields = {
        'time': when,
        'level': levels.INFO,
        'name': 'mylog',
        'pants': 42,
        }

    def test_copy(self):
        my_format = copy.copy(formats.line_format)
        assert my_format.separator == formats.line_format.separator
        assert my_format.traceback_prefix == formats.line_format.traceback_prefix
        
        # XXX it'd be nice to test the guts of the conversion for equality, but Converters don't support that
        assert my_format.conversion is not formats.line_format.conversion
    
    def test_basic(self):
        
        fmt = formats.LineFormat(separator='|', conversion=formats.line_conversion)
        
        opts = message.Message._default_options.copy()       
        msg = message.Message(levels.INFO, "I wear {0}", self.fields, opts, ['pants'], {})       
        assert fmt(msg) == '2010-10-28T02:15:57Z:INFO:mylog:pants=42|I wear pants\n'
        
    def test_suppress_newline_true(self):
        
        fmt = formats.LineFormat(separator='|', conversion=formats.line_conversion)
        
        fields = self.fields.copy()
        fields['shirt'] = 'extra\nlarge'
        
        opts = message.Message._default_options.copy()       
        opts['suppress_newlines'] = True
        msg = message.Message(levels.INFO, "I wear {0}\nDo you?", fields, opts, ['pants'], {})       
        s = fmt(msg)

        assert s == '2010-10-28T02:15:57Z:INFO:mylog:pants=42:shirt=extra\\nlarge|I wear pants\\nDo you?\n', repr(s)
    
    def test_suppress_newline_false(self):
        
        fmt = formats.LineFormat(separator='|', conversion=formats.line_conversion)
        
        fields = self.fields.copy()
        fields['shirt'] = 'extra\nlarge'        
        
        opts = message.Message._default_options.copy()       
        opts['suppress_newlines'] = False
        msg = message.Message(levels.INFO, "I wear {0}\nDo you?", fields, opts, ['pants'], {})       
        s = fmt(msg)
        assert s == '2010-10-28T02:15:57Z:INFO:mylog:pants=42:shirt=extra\nlarge|I wear pants\nDo you?\n', repr(s)
        
    
    def test_trace(self):
        
        fmt = formats.LineFormat(separator='|', conversion=formats.line_conversion)
        
        opts = message.Message._default_options.copy()       
        opts['trace'] = 'error'
        
        try:
            1/0
        except:
            msg = message.Message(levels.INFO, "I wear {0}", self.fields, opts, ['pants'], {})       
        
        s = fmt(msg)
        l = s.split('\n')
        assert len(l) == 6
        for i in l[1:-1]:
            assert i.startswith('TRACE')
            
        assert l[0] == '2010-10-28T02:15:57Z:INFO:mylog:pants=42|I wear pants'
            
    def test_trace_fold(self):
        
        fmt = formats.LineFormat(separator='|', traceback_prefix = '\\n', conversion=formats.line_conversion)
        
        opts = message.Message._default_options.copy()       
        opts['trace'] = 'error'
        
        try:
            1/0
        except:
            msg = message.Message(levels.INFO, "I wear {0}", self.fields, opts, ['pants'], {})       
        
        s = fmt(msg)
        l = s.split('\n')
        assert len(l) == 2
