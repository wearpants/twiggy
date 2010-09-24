import unittest2

import twiggy.levels
from twiggy.Message import Message

from . import make_mesg

class MessageTestCase(unittest2.TestCase):

    def test_basic(self):
        m = make_mesg()

        assert m.format_spec == "Hello {0} {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None

        assert m.text == "Hello Mister Funnypants"

    def test_level_property(self):
        m = make_mesg()
        assert m.level == twiggy.levels.DEBUG

    def test_name_property(self):
        m = make_mesg()
        assert m.name == 'jose'

    def test_suppress_newlines_true(self):
        opts = Message._default_options.copy()
        opts['suppress_newlines'] = True

        m = Message(twiggy.levels.DEBUG,
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

        m = Message(twiggy.levels.DEBUG,
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
        m = Message(twiggy.levels.DEBUG,
                    "Hello {who}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    who="Funnypants",
                    )

        assert m.format_spec == "Hello {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.args == ()
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None

        assert m.text == "Hello Funnypants"

    def test_no_kwargs(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello {0}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    'Mister'
                    )

        assert m.format_spec == "Hello {0}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {}
        assert m.traceback is None

        assert m.text == "Hello Mister"

    def test_no_args_no_kwargs(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    )

        assert m.format_spec == "Hello"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.args == ()
        assert m.kwargs == {}
        assert m.traceback is None

        assert m.text == "Hello"

    def test_bad_style(self):
        opts = Message._default_options.copy()
        opts['style'] = 'badstyle'

        with self.assertRaises(ValueError):
            Message(twiggy.levels.DEBUG,
                    "Hello {0} {who}",
                    {},
                    opts,
                    "Mister",
                    who="Funnypants",
                    )

    def test_dollar_style(self):
        opts = Message._default_options.copy()
        opts['style'] = 'dollar'

        m = Message(twiggy.levels.DEBUG,
                    "Hello $who",
                    {},
                    opts,
                    who="Funnypants",
                    )

        assert m.text == "Hello Funnypants"

    def test_percent_style_args(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'

        m = Message(twiggy.levels.DEBUG,
                    "Hello %s",
                    {},
                    opts,
                    "Funnypants",
                    )

        assert m.text == "Hello Funnypants"

    def test_percent_style_kwargs(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'

        m = Message(twiggy.levels.DEBUG,
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
            m = Message(twiggy.levels.DEBUG,
                        "Hello %s %(who)s",
                        {},
                        opts,
                        "Mister",
                        who="Funnypants",
                        )

    def test_callables(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello {0} {who}",
                    {'shirt': lambda: 42, 'name': 'jose'},
                    Message._default_options,
                    lambda: "Mister",
                    who=lambda: "Funnypants",
                    )

        assert m.format_spec == "Hello {0} {who}"
        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.args == ('Mister',)
        assert m.kwargs == {'who': "Funnypants"}
        assert m.traceback is None

        assert m.text == "Hello Mister Funnypants"

