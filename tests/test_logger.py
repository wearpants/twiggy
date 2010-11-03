import unittest

from twiggy import logger, outputs, levels

class InternalLoggerTest(unittest.TestCase):

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
    
    def test_fieldsDict(self):
        d={'a':42}
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
        assert len(self.messages) == 1
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
    
    def test_min_level(self):
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
        
        
        
        
        
        
        
