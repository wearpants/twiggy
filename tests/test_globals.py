import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
import sys
import os
import tempfile

import twiggy


class GlobalsTestCase(unittest.TestCase):

    def setUp(self):
        twiggy._populate_globals()
    
    def tearDown(self):
        twiggy._del_globals()
    
    def test_populate_globals_twice(self):
    
        with self.assertRaises(RuntimeError):
            twiggy._populate_globals()
    
    def test_globals(self):
        assert isinstance(twiggy.log, twiggy.logger.Logger)
        assert isinstance(twiggy.emitters, dict)
        assert twiggy.emitters is twiggy.log._emitters
        
        assert isinstance(twiggy.internal_log, twiggy.logger.InternalLogger)
        assert twiggy.internal_log._fields['name'] == 'twiggy.internal'
        assert twiggy.internal_log._options['trace'] == 'error'
        
        assert isinstance(twiggy.devel_log, twiggy.logger.InternalLogger)
        assert twiggy.devel_log._fields['name'] == 'twiggy.devel'
        assert isinstance(twiggy.devel_log.output, twiggy.outputs.NullOutput)
    
    def test_add_emitters(self):
        
        out = twiggy.outputs.ListOutput(close_atexit = False)
        
        def cleanup(out):
            out.close()
        
        self.addCleanup(cleanup, out)
        
        def myfilt(msg):
            return True
        
        twiggy.add_emitters(('test', twiggy.levels.INFO, myfilt, out))
        
        assert len(twiggy.emitters) == 1
        e = twiggy.emitters['test']
        assert isinstance(e, twiggy.filters.Emitter)
        assert e.min_level == twiggy.levels.INFO
        assert e.filter is myfilt
        assert e._output is out
        
    def test_quick_setup_None(self):
        twiggy.quick_setup(file=None)
        assert len(twiggy.emitters) == 1
        e = twiggy.emitters['*']
        assert isinstance(e, twiggy.filters.Emitter)
        assert isinstance(e._output, twiggy.outputs.StreamOutput)
        assert e._output.stream is sys.stderr

    def test_quick_setup_stdout(self):
        twiggy.quick_setup(file=sys.stdout)
        assert len(twiggy.emitters) == 1
        e = twiggy.emitters['*']
        assert isinstance(e, twiggy.filters.Emitter)
        assert isinstance(e._output, twiggy.outputs.StreamOutput)
        assert e._output.stream is sys.stdout
    
        
    def test_quick_setup_file(self):

        fname = tempfile.mktemp()
        print(fname)
        
        @self.addCleanup      
        def cleanup():
            os.remove(fname)

        twiggy.quick_setup(file=fname)
        assert len(twiggy.emitters) == 1
        e = twiggy.emitters['*']
        assert isinstance(e, twiggy.filters.Emitter)
        assert isinstance(e._output, twiggy.outputs.FileOutput)
        assert os.path.exists(fname)

        
                


