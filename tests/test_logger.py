# coding: utf-8

import itertools
import re
import sys

import pytest
from six import StringIO, string_types

import twiggy as _twiggy
from twiggy import logger, outputs, levels, filters

if sys.version_info >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")


@pytest.fixture(params=(logger.Logger, logger.InternalLogger))
def test_logger(request):
    output = outputs.ListOutput(close_atexit=False)
    if issubclass(request.param, logger.InternalLogger):
        yield request.param(output=output)
    else:
        log = request.param()
        emitters = log._emitters
        emitters['*'] = filters.Emitter(levels.DEBUG, None, output)
        yield log

    output.close()


class TestLoggerFields(object):
    TEST_FIELDS_DATA = (
            {42: 42},
            {b'a': 42},
            {u'a': 42},
            {b'a': b'b'},
            {u'a': u'b'},
            {b'\xe4\xb8\xad': 42},
            {u'中': 42},
            {b'a': b'\xe4\xb8\xad'},
            {u'a': u'中'},
            )

    TEST_NAMES_DATA = (
            ('bob', {'name': 'bob'}),
            (b'\xe4\xb8\xad', {'name': b'\xe4\xb8\xad'}),
            (u'中', {'name': u'中'}),
            )

    @pytest.mark.parametrize('fields', TEST_FIELDS_DATA)
    def test_fields_dict(self, test_logger, fields):
        log = test_logger.fields_dict(fields)
        assert log is not test_logger
        assert log._fields == fields
        assert log._fields is not fields

    # Note: On python2, byte strings are valid keyword argument identifiers but not on python3
    @pytest.mark.parametrize('fields', (d for d in TEST_FIELDS_DATA if
                                        isinstance(list(d.keys())[0], string_types)))
    def test_fields(self, test_logger, fields):
        log = test_logger.fields(**fields)
        assert log is not test_logger
        assert log._fields == fields
        assert log._fields is not fields

    @pytest.mark.parametrize('name, expected', TEST_NAMES_DATA)
    def test_name(self, test_logger, name, expected):
        log = test_logger.name(name)
        assert log is not test_logger
        assert log._fields == expected


class TestOptions(object):
    # More comprehensive options tests done in test_message
    def test_options(self, test_logger):
        log = test_logger.options(suppress_newlines=True)
        assert log is not test_logger
        assert log._options['suppress_newlines'] is True

    def test_bad_options(self, test_logger):
        with pytest.raises(ValueError):
            test_logger.options(boom=True)

    def test_trace(self, test_logger):
        log = test_logger.trace('error')
        assert log is not test_logger
        assert log._options['trace'] == 'error'


class TestLevels(object):
    TEST_LEVELS_MSGS = (
            (u'hi', u'hi'),
            (b'hi', u'hi'),
            (b'\xe4\xb8\xad', u'中'),
            (u'中', u'中'),
            )

    TEST_LEVELS_LEVELS = (
            ('debug', levels.DEBUG),
            ('info', levels.INFO),
            ('notice', levels.NOTICE),
            ('warning', levels.WARNING),
            ('error', levels.ERROR),
            ('critical', levels.CRITICAL),
            )

    @pytest.fixture
    def level_logger(self, test_logger):
        if isinstance(test_logger, logger.InternalLogger):
            messages = test_logger.output.messages
        else:
            emitter = None
            for emitter in test_logger._emitters.values():
                break
            messages = emitter._output.messages

        yield test_logger, messages

    @pytest.mark.parametrize('level_params, msg_params',
                             itertools.product(TEST_LEVELS_LEVELS, TEST_LEVELS_MSGS))
    def test_level_functions(self, level_logger, level_params, msg_params):
        level, expected_level = level_params
        msg, expected_msg = msg_params
        test_logger, test_messages = level_logger

        level_function = getattr(test_logger, level)
        level_function(msg)
        assert len(test_messages) == 1
        m = test_messages.pop()
        assert m.text == expected_msg
        assert m.fields['level'] == expected_level

    @pytest.mark.parametrize('msg, expected', TEST_LEVELS_MSGS)
    def test_logger_min_level(self, level_logger, msg, expected):
        test_logger, test_messages = level_logger

        log = test_logger.name('test_min_level')
        log.min_level = levels.WARNING

        log.warning(msg)
        assert len(test_messages) == 1
        m = test_messages.pop()
        assert m.text == expected

        log.error(msg)
        assert len(test_messages) == 1
        m = test_messages.pop()
        assert m.text == expected

        log.info(msg)
        assert len(test_messages) == 0


class InternalLoggerTest(unittest.TestCase):

    def setUp(self):
        self.output = outputs.ListOutput(close_atexit=False)
        self.messages = self.output.messages
        self.log = logger.InternalLogger(output=self.output)

    def tearDown(self):
        self.output.close()

    def test_clone(self):
        log = self.log._clone()
        assert log is not self.log
        assert isinstance(log, logger.InternalLogger)
        assert isinstance(self.log, logger.InternalLogger)
        assert log.output is self.output

        assert log._fields == self.log._fields
        assert log._fields is not self.log._fields

        assert log._options == self.log._options
        assert log._options is not self.log._options

        assert log.min_level == self.log.min_level

    def test_trap_msg(self):
        sio = StringIO()

        def cleanup(stderr):
            sys.stderr = stderr
            sio.close()

        self.addCleanup(cleanup, sys.stderr)
        sys.stderr = sio

        def go_boom():
            raise RuntimeError("BOOM")

        self.log.fields(func=go_boom).info('hi')

        assert "BOOM" in sio.getvalue()
        assert "Offending message: None" in sio.getvalue()
        assert "Error in twiggy internal log! Something is seriously broken." in sio.getvalue()
        assert "Traceback" in sio.getvalue()

    def test_trap_output(self):
        class BorkedOutput(outputs.ListOutput):

            def _write(self, x):
                raise RuntimeError("BORK")

        out = BorkedOutput(close_atexit=False)

        sio = StringIO()

        def cleanup(stderr, output):
            sys.stderr = stderr
            sio.close()
            self.log.output = output
            out.close()

        self.addCleanup(cleanup, sys.stderr, self.log.output)
        sys.stderr = sio
        self.log.output = out

        self.log.fields().info('hi')

        assert "BORK" in sio.getvalue()
        assert "Offending message: <twiggy.message.Message object" in sio.getvalue()
        assert "Error in twiggy internal log! Something is seriously broken." in sio.getvalue()
        assert "Traceback" in sio.getvalue()


class LoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.log = logger.Logger()
        self.emitters = self.log._emitters
        self.output = outputs.ListOutput(close_atexit=False)
        self.emitters['*'] = filters.Emitter(levels.DEBUG, None, self.output)
        self.messages = self.output.messages

    def tearDown(self):
        self.output.close()
        self.emitters.clear()

    def test_struct_dict(self):
        d = {42: 42}
        self.log.struct_dict(d)
        assert len(self.messages) == 1
        m = self.messages.pop()
        self.assertDictContainsSubset(d, m.fields)
        assert m.fields is not d
        assert m.text == ""
        assert m.level == levels.INFO
        # we could do the same tests on options/min_level as done
        # in test_clone, but that's starting to get redundant

    def test_fields(self):
        self.log.struct(x=42)
        assert len(self.messages) == 1
        m = self.messages.pop()
        self.assertDictContainsSubset({'x': 42}, m.fields)
        assert m.text == ""
        assert m.level == levels.INFO

    def test_no_emitters(self):
        self.emitters.clear()
        self.log.debug('hi')
        assert len(self.messages) == 0

    def test_min_level_emitters(self):
        self.emitters['*'].min_level = levels.INFO
        self.log.debug('hi')
        assert len(self.messages) == 0

    def test_filter_emitters(self):
        self.emitters['*'].filter = 'pants'
        self.log.debug('hi')
        assert len(self.messages) == 0

    def test_logger_filter(self):
        self.log.filter = lambda fmt_spec: 'pants' in fmt_spec
        self.log.debug('hi')
        assert len(self.messages) == 0

        self.log.filter = lambda fmt_spec: 'hi' in fmt_spec
        self.log.debug('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'


class LoggerTrapTestCase(unittest.TestCase):

    def setUp(self):
        self.internal_output = outputs.ListOutput(close_atexit=False)
        self.internal_messages = self.internal_output.messages
        _twiggy._populate_globals()
        _twiggy.internal_log.output = self.internal_output

        self.log = logger.Logger()
        self.emitters = self.log._emitters
        self.output = outputs.ListOutput(close_atexit=False)
        self.emitters['everything'] = filters.Emitter(levels.DEBUG, None, self.output)
        self.messages = self.output.messages

    def tearDown(self):
        self.internal_output.close()
        _twiggy._del_globals()

        self.output.close()
        self.emitters.clear()

    def test_bad_logger_filter(self):
        def bad_filter(fmt_spec):
            raise RuntimeError("THUNK")

        self.log.filter = bad_filter

        # a bad filter doesn't stop emitting
        self.log.debug('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'

        assert len(self.internal_messages) == 1
        m = self.internal_messages.pop()

        print(m.text)
        print(m.traceback)
        print(_twiggy.internal_log._options)

        assert m.level == levels.INFO
        assert m.name == 'twiggy.internal'
        assert "Traceback" in m.traceback
        assert "THUNK" in m.traceback
        assert "Error in Logger filtering" in m.text
        assert re.search("<function .*bad_filter", m.text)

    def test_trap_bad_msg(self):
        def go_boom():
            raise RuntimeError("BOOM")

        self.log.fields(func=go_boom).info('hi')
        assert len(self.messages) == 0

        assert len(self.internal_messages) == 1
        m = self.internal_messages.pop()

        print(m.text)
        print(m.traceback)
        print(_twiggy.internal_log._options)

        assert m.level == levels.INFO
        assert m.name == 'twiggy.internal'
        assert "Traceback" in m.traceback
        assert "BOOM" in m.traceback
        assert "Error formatting message" in m.text
        assert re.search("<function .*go_boom", m.text)

    def test_trap_output(self):
        class BorkedOutput(outputs.ListOutput):

            def _write(self, x):
                raise RuntimeError("BORK")

        out = BorkedOutput(close_atexit=False)

        def cleanup(output):
            try:
                del self.emitters['before']
            except KeyError:
                pass

            out.close()

        self.addCleanup(cleanup, out)

        self.emitters['before'] = filters.Emitter(levels.DEBUG, None, out)

        self.log.fields().info('hi')

        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == "hi"

        assert len(self.internal_messages) == 1
        m = self.internal_messages.pop()

        print(m.text)
        print(m.traceback)

        assert m.level == levels.WARNING
        assert re.search(
            "Error outputting with <tests.test_logger.*BorkedOutput",
            m.text)
        assert "Traceback" in m.traceback
        assert "BORK" in m.traceback

    def test_trap_filter(self):

        out = outputs.ListOutput(close_atexit=False)

        def cleanup(output):
            try:
                del self.emitters['before']
            except KeyError:
                pass

            out.close()

        self.addCleanup(cleanup, out)

        def go_boom(msg):
            raise RuntimeError("BOOM")

        self.emitters['before'] = filters.Emitter(levels.DEBUG, go_boom, out)

        self.log.fields().info('hi')

        # errors in filtering cause messages to be output anyway
        assert len(out.messages) == 1
        m1 = out.messages.pop()
        assert m1.text == "hi"

        assert len(self.messages) == 1
        m2 = self.messages.pop()
        assert m2.text == "hi"

        assert m1 is m2

        assert len(self.internal_messages) == 1
        m = self.internal_messages.pop()

        print(m.text)
        print(m.traceback)

        assert m.level == levels.INFO
        assert "Error filtering with emitter before" in m.text
        assert re.search("<function .*go_boom", m.text)
        assert "Traceback" in m.traceback
        assert "BOOM" in m.traceback
