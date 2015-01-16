import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
import sys

import twiggy.levels
from twiggy.message import Message

from . import make_mesg

class MessageTestCase(unittest.TestCase):

    def test_basic(self):
        m = make_mesg()

        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
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
                    args=["Mister"],
                    kwargs={'who':"Funnypants\nand shirt"},
                    )

        assert m.text == '''Hello Mister Funnypants\nand shirt'''

    def test_suppress_newlines_false(self):
        opts = Message._default_options.copy()
        opts['suppress_newlines'] = False

        m = Message(twiggy.levels.DEBUG,
                    "Hello {0} {who}",
                    {},
                    opts,
                    args=["Mister"],
                    kwargs={'who':"Funnypants\nand shirt"},
                    )

        assert m.text == \
'''Hello Mister Funnypants
and shirt'''

    def test_no_args(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello {who}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    args=(),
                    kwargs={'who':"Funnypants"},
                    )

        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.traceback is None

        assert m.text == "Hello Funnypants"

    def test_no_kwargs(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello {0}",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    args=['Mister'],
                    kwargs={}
                    )

        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.traceback is None

        assert m.text == "Hello Mister"

    def test_no_args_no_kwargs(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello",
                    {'shirt':42, 'name': 'jose'},
                    Message._default_options,
                    (),
                    {}
                    )

        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
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
                    args=["Mister"],
                    kwargs={'who':"Funnypants\nand shirt"},
                    )

    def test_dollar_style(self):
        opts = Message._default_options.copy()
        opts['style'] = 'dollar'

        m = Message(twiggy.levels.DEBUG,
                    "Hello $who",
                    {},
                    opts,
                    args=[],
                    kwargs={'who':"Funnypants"},
                    )

        assert m.text == "Hello Funnypants"


    def test_dollar_style_bad(self):
        opts = Message._default_options.copy()
        opts['style'] = 'dollar'

        with self.assertRaises(ValueError):
            m = Message(twiggy.levels.DEBUG,
                        "Hello $who",
                        {},
                        opts,
                        args=[42],
                        kwargs={'who':"Funnypants"},
                        )

    def test_percent_style_args(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'

        m = Message(twiggy.levels.DEBUG,
                    "Hello %s",
                    {},
                    opts,
                    args=["Funnypants"],
                    kwargs={}
                    )

        assert m.text == "Hello Funnypants"

    def test_percent_style_kwargs(self):
        opts = Message._default_options.copy()
        opts['style'] = 'percent'

        m = Message(twiggy.levels.DEBUG,
                    "Hello %(who)s",
                    {},
                    opts,
                    args=[],
                    kwargs={'who':"Funnypants"},
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
                        args=["Mister"],
                        kwargs={'who':"Funnypants\nand shirt"},
                        )

    def test_callables(self):
        m = Message(twiggy.levels.DEBUG,
                    "Hello {0} {who}",
                    {'shirt': lambda: 42, 'name': 'jose'},
                    Message._default_options,
                    args=[lambda: "Mister"],
                    kwargs={'who':lambda: "Funnypants"},
                    )

        assert m.fields == {'shirt':42, 'name': 'jose', 'level':twiggy.levels.DEBUG}
        assert m.traceback is None

        assert m.text == "Hello Mister Funnypants"

    def test_empty_format_spec(self):
        m = Message(twiggy.levels.DEBUG,
            '',
            {'shirt': lambda: 42, 'name': 'jose'},
            Message._default_options,
            args=[lambda: "Mister"],
            kwargs={'who':lambda: "Funnypants"},
            )

        assert m.text == ''
        assert m.name == 'jose'
        assert m.fields['shirt'] == 42


    def test_bad_trace(self):
        opts = Message._default_options.copy()
        opts['trace'] = 'kaboom'

        with self.assertRaises(ValueError):
            m = Message(twiggy.levels.DEBUG,
                "Hello {0} {who}",
                {'shirt': lambda: 42, 'name': 'jose'},
                opts,
                args=[lambda: "Mister"],
                kwargs={'who':lambda: "Funnypants"},
                )

    def test_trace_error_without_error(self):
        opts = Message._default_options.copy()
        opts['trace'] = 'error'

        m = Message(twiggy.levels.DEBUG,
            "Hello {0} {who}",
            {'shirt': lambda: 42, 'name': 'jose'},
            opts,
            args=[lambda: "Mister"],
            kwargs={'who':lambda: "Funnypants"},
            )

        assert m.traceback is None


    def test_trace_error_with_error(self):
        opts = Message._default_options.copy()
        opts['trace'] = 'error'


        try:
            1/0
        except ZeroDivisionError:
            m = Message(twiggy.levels.DEBUG,
                "Hello {0} {who}",
                {'shirt': lambda: 42, 'name': 'jose'},
                opts,
                args=[lambda: "Mister"],
                kwargs={'who':lambda: "Funnypants"},
                )

        assert m.traceback.startswith('Traceback (most recent call last):')
        assert 'ZeroDivisionError:' in m.traceback

    def test_trace_tuple(self):
        opts = Message._default_options.copy()

        try:
            1/0
        except ZeroDivisionError:
            opts['trace'] = sys.exc_info()
            m = Message(twiggy.levels.DEBUG,
                "Hello {0} {who}",
                {'shirt': lambda: 42, 'name': 'jose'},
                opts,
                args=[lambda: "Mister"],
                kwargs={'who':lambda: "Funnypants"},
                )

        assert m.traceback.startswith('Traceback (most recent call last):')
        assert 'ZeroDivisionError:' in m.traceback
