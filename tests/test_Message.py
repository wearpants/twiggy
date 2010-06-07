import unittest2

import twiggy.Levels
from twiggy.Message import Message

def make_mesg():
    return Message(twiggy.Levels.DEBUG,
                   "Hello {0} {who}",
                   {'shirt':42, 'name': 'jose'},
                   Message._default_options,
                   "Mister",
                   who="Funnypants",
                   )

class MessageTestCase(unittest2.TestCase):
    
    def test_basic(self):
        m = make_mesg()
        
        assert m.format_spec == "Hello {0} {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.Levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None
        
        assert m.text == "Hello Mister Funnypants"
    
    def test_level_property(self):
        m = make_mesg()
        assert m.level == twiggy.Levels.DEBUG
    
    def test_name_property(self):
        m = make_mesg()
        assert m.name == 'jose'
    
    def test_suppress_newlines_true(self):
        opts = Message._default_options.copy()
        opts['suppress_newlines'] = True
        
        m = Message(twiggy.Levels.DEBUG,
                    "Hello {0} {who}",
                    {},
                    opts,
                    "Mister",
                    who="Funnypants\nand shirt",
                    )
        
        assert m.text == '''Hello Mister Funnypants\nand shirt'''

    def test_suppress_newlines_false(self):
        opts = Message._default_options.copy()
        opts['suppress_newlines'] = False
        
        m = Message(twiggy.Levels.DEBUG,
                    "Hello {0} {who}",
                    {},
                    opts,
                    "Mister",
                    who="Funnypants\nand shirt",
                    )
        
        assert m.text == \
'''Hello Mister Funnypants
and shirt'''
    
    def test_no_args(self):
        m = Message(twiggy.Levels.DEBUG,
                    "Hello {who}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    who="Funnypants",
                    )
        
        assert m.format_spec == "Hello {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.Levels.DEBUG}
        assert m.args == ()
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None
        
        assert m.text == "Hello Funnypants"

    def test_no_kwargs(self):
        m = Message(twiggy.Levels.DEBUG,
                    "Hello {0}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    'Mister'
                    )
        
        assert m.format_spec == "Hello {0}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.Levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {}
        assert m.traceback is None
        
        assert m.text == "Hello Mister"

    def test_no_args_no_kwargs(self):
        m = Message(twiggy.Levels.DEBUG,
                    "Hello",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    )
        
        assert m.format_spec == "Hello"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.Levels.DEBUG}
        assert m.args == ()
        assert m.kwargs == {}
        assert m.traceback is None
        
        assert m.text == "Hello"

    def test_bad_style(self):
        opts = Message._default_options.copy()
        opts['style'] = 'badstyle'
        
        with self.assertRaises(ValueError):
            Message(twiggy.Levels.DEBUG,
                    "Hello {0} {who}",
                    {},
                    opts,
                    "Mister",
                    who="Funnypants",
                    )

    def test_dollar_style(self):
        opts = Message._default_options.copy()
        opts['style'] = 'dollar'
        
        m = Message(twiggy.Levels.DEBUG,
                    "Hello $who",
                    {},
                    opts,
                    who="Funnypants",
                    )
        
        assert m.text == "Hello Funnypants"
    
    def test_percent_style_args(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'
        
        m = Message(twiggy.Levels.DEBUG,
                    "Hello %s",
                    {},
                    opts,
                    "Funnypants",
                    )
        
        assert m.text == "Hello Funnypants"

    def test_percent_style_kwargs(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'
        
        m = Message(twiggy.Levels.DEBUG,
                    "Hello %(who)s",
                    {},
                    opts,
                    who="Funnypants",
                    )
        
        assert m.text == "Hello Funnypants"

    def test_percent_style_both(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'
        
        with self.assertRaises(ValueError):
            m = Message(twiggy.Levels.DEBUG,
                        "Hello %s %(who)s",
                        {},
                        opts,
                        "Mister",
                        who="Funnypants",
                        )

    def test_callables(self):
        m = Message(twiggy.Levels.DEBUG,
                    "Hello {0} {who}",
                    {'shirt': lambda: 42, 'name': 'jose'},
                    Message._default_options,
                    lambda: "Mister",
                    who=lambda: "Funnypants",
                    )
        
        assert m.format_spec == "Hello {0} {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.Levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None
        
        assert m.text == "Hello Mister Funnypants"

