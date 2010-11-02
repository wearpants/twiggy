import unittest2
import tempfile
import os

from twiggy import outputs, formats

from . import make_mesg, when

m = make_mesg()

# just stuff time in fields so we can use an existing format object
m.fields['time']=when

# XXX I can't think of a decent way to test Output/AsyncOutput on their own...

class UnlockedFileOutput(outputs.FileOutput):

    use_locks = False

class FileOutputTestCase(unittest2.TestCase):

    def setUp(self):
        self.fname = tempfile.mktemp()
    
    def tearDown(self):
        try:
            os.remove(self.fname)
        except:
            pass
                
        del self.fname
    
    def make_output(self, msg_buffer, locked):
        cls = outputs.FileOutput if locked else UnlockedFileOutput
        
        return cls(name = self.fname, format = formats.shell_format, buffering = 0,
                   msg_buffer = msg_buffer, close_atexit=False)
                                         
    def test_sync(self):
        o = self.make_output(0, True)
        o.output(m)
        o.close()
        s = open(self.fname, 'r').read()
        assert s == "DEBUG:jose:shirt=42:Hello Mister Funnypants\n"

    def test_sync_unlocked(self):
        o = self.make_output(0, False)
        o.output(m)
        o.close()
        s = open(self.fname, 'r').read()
        assert s == "DEBUG:jose:shirt=42:Hello Mister Funnypants\n"

    def test_async(self):
        o = self.make_output(-1, True)
        o.output(m)
        o.close()
        s = open(self.fname, 'r').read()
        assert s == "DEBUG:jose:shirt=42:Hello Mister Funnypants\n"

    def test_async_unlocked(self):
        o = self.make_output(-1, False)
        o.output(m)
        o.close()
        s = open(self.fname, 'r').read()
        assert s == "DEBUG:jose:shirt=42:Hello Mister Funnypants\n"

