import unittest
import sys
import StringIO

from twiggy import logger, outputs, levels, filters

class LoggerTestBase(object):
    """common tests for loggers"""
    def test_fieldsDict(self):
        d={42:42}
        log = self.log.fieldsDict(d)
        assert log is not self.log
        assert log._fields == d
        assert log._fields is not d

        # we could do the same tests on options/min_level as done
        # in test_clone, but that's starting to get redundant

    def test_fields(self):
        log = self.log.fields(a=42)
        assert log is not self.log
        assert log._fields == {'a':42}

    def test_name(self):
        log = self.log.name('bob')
        assert log is not self.log
        assert log._fields == {'name':'bob'}

    def test_options(self):
        log = self.log.options(suppress_newlines=True)
        assert log is not self.log
        assert log._options['suppress_newlines'] == True

    def test_bad_options(self):
        with self.assertRaises(ValueError):
            log = self.log.options(boom=True)

    def test_trace(self):
        log = self.log.trace('error')
        assert log is not self.log
        assert log._options['trace'] == 'error'

    def test_debug(self):
        self.log.debug('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'
        assert m.fields['level'] == levels.DEBUG

    def test_info(self):
        self.log.info('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'
        assert m.fields['level'] == levels.INFO

    def test_warning(self):
        self.log.warning('hi')
        assert len(self.messages) == 1, self.messages
        m = self.messages.pop()
        assert m.text == 'hi'
        assert m.fields['level'] == levels.WARNING

    def test_error(self):
        self.log.error('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'
        assert m.fields['level'] == levels.ERROR

    def test_critical(self):
        self.log.critical('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'
        assert m.fields['level'] == levels.CRITICAL

    def test_logger_min_level(self):
        log = self.log.name('test_min_level')
        log.min_level = levels.WARNING

        log.warning('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'

        log.error('hi')
        assert len(self.messages) == 1
        m = self.messages.pop()
        assert m.text == 'hi'

        log.info('hi')
        assert len(self.messages) == 0

class InternalLoggerTest(LoggerTestBase, unittest.TestCase):

    def setUp(self):
        self.output = outputs.ListOutput(close_atexit = False)
        self.messages = self.output.messages
        self.log = logger.InternalLogger(output=self.output)

    def tearDown(self):
        self.output.close()

    def test_clone(self):
        log = self.log._clone()
        assert log is not self.log
        assert type(log) is type(self.log)
        assert log.output is self.output

        assert log._fields == self.log._fields
        assert log._fields is not self.log._fields

        assert log._options == self.log._options
        assert log._options is not self.log._options

        assert log.min_level == self.log.min_level

    def test_trap_msg(self):
        sio = StringIO.StringIO()

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
        assert "Error in twiggy internal log! Something is serioulsy broken." in sio.getvalue()
        assert "Traceback" in sio.getvalue()

    def test_trap_output(self):
        class BorkedOutput(outputs.ListOutput):

            def _write(self, x):
                raise RuntimeError("BORK")

        out = BorkedOutput(close_atexit = False)

        sio = StringIO.StringIO()

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
        assert "Error in twiggy internal log! Something is serioulsy broken." in sio.getvalue()
        assert "Traceback" in sio.getvalue()

class LoggerTestCase(LoggerTestBase, unittest.TestCase):

    def setUp(self):
        self.log = logger.Logger()
        self.emitters = self.log._emitters
        self.output = outputs.ListOutput(close_atexit = False)
        self.emitters['*'] = filters.Emitter(levels.DEBUG, None, self.output)
        self.messages = self.output.messages


    def tearDown(self):
        self.output.close()
        self.emitters.clear()
    
    def test_structDict(self):
        d={42:42}
        log = self.log.structDict(d)
        assert len(self.messages) == 1
        m = self.messages.pop()
        self.assertDictContainsSubset(d, m.fields)
        assert m.fields is not d
        assert m.text == ""
        assert m.level == levels.INFO

        # we could do the same tests on options/min_level as done
        # in test_clone, but that's starting to get redundant

    def test_fields(self):
        log = self.log.struct(x=42)
        assert len(self.messages) == 1
        m = self.messages.pop()
        self.assertDictContainsSubset({'x':42}, m.fields)
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
