import os
import shutil
import sys
import tempfile
import warnings

import pytest
from six import StringIO

import twiggy


DEPRECATED_FUNCS = (
    (twiggy.quickSetup, 'twiggy.quickSetup is deprecated in favor of twiggy.quick_setup'),
    (twiggy.addEmitters, 'twiggy.addEmitters is deprecated in favor of twiggy.add_emitters'),
)


#
# Fixtures
#


@pytest.fixture(autouse=True)
def twiggy_globals():
    twiggy._populate_globals()
    yield
    twiggy._del_globals()


@pytest.fixture
def internal_log():
    output = twiggy.internal_log.output

    buf = StringIO()
    new_output = twiggy.outputs.StreamOutput(format=output._format, stream=buf)

    twiggy.internal_log.output = new_output
    yield buf
    twiggy.internal_log.output = output


@pytest.fixture
def deprecations_error(*args):
    for module in sys.modules.values():
        if hasattr(module, '__warningregistry__'):
            del module.__warningregistry__
    warnings.simplefilter('error', DeprecationWarning)

    yield

    warnings.simplefilter('ignore', DeprecationWarning)


@pytest.fixture
def twiggy_output():
    out = twiggy.outputs.ListOutput(close_atexit=False)
    yield out
    out.close()


@pytest.fixture
def setup_emitters(twiggy_output):
    def myfilt(msg):
        return True

    twiggy.add_emitters(('test', twiggy.levels.INFO, myfilt, twiggy_output))
    twiggy.add_emitters(('second', twiggy.levels.INFO, myfilt, twiggy_output))
    twiggy.add_emitters(('*', twiggy.levels.INFO, myfilt, twiggy_output))


@pytest.fixture
def tmp_dir():
    new_dir = tempfile.mkdtemp()
    yield new_dir
    shutil.rmtree(new_dir)


#
# Tests: Globals
#


def test_populate_globals_twice():
    with pytest.raises(RuntimeError):
        twiggy._populate_globals()


def test_globals():
    assert isinstance(twiggy.log, twiggy.logger.Logger)
    assert isinstance(twiggy.emitters, dict)
    assert twiggy.emitters is twiggy.log._emitters

    assert isinstance(twiggy.internal_log, twiggy.logger.InternalLogger)
    assert twiggy.internal_log._fields['name'] == 'twiggy.internal'
    assert twiggy.internal_log._options['trace'] == 'error'

    assert isinstance(twiggy.devel_log, twiggy.logger.InternalLogger)
    assert twiggy.devel_log._fields['name'] == 'twiggy.devel'
    assert isinstance(twiggy.devel_log.output, twiggy.outputs.NullOutput)


#
# Tests: quick_setup
#


def test_quick_setup_None():
    twiggy.quick_setup(file=None)
    assert len(twiggy.emitters) == 1
    e = twiggy.emitters['*']
    assert isinstance(e, twiggy.filters.Emitter)
    assert isinstance(e._output, twiggy.outputs.StreamOutput)
    assert e._output.stream is sys.stderr


def test_quick_setup_stdout():
    twiggy.quick_setup(file=sys.stdout)
    assert len(twiggy.emitters) == 1
    e = twiggy.emitters['*']
    assert isinstance(e, twiggy.filters.Emitter)
    assert isinstance(e._output, twiggy.outputs.StreamOutput)
    assert e._output.stream is sys.stdout


def test_quick_setup_file(tmp_dir):
    print(tmp_dir)

    logfile = os.path.join(tmp_dir, 'log')
    twiggy.quick_setup(file=logfile)

    assert len(twiggy.emitters) == 1
    e = twiggy.emitters['*']
    assert isinstance(e, twiggy.filters.Emitter)
    assert isinstance(e._output, twiggy.outputs.FileOutput)
    assert os.path.exists(logfile)


def test_quickSetup(mocker):
    mocker.patch('twiggy.quick_setup')

    def myfilt(msg):
        return True

    twiggy.quickSetup()
    twiggy.quickSetup(file=None)
    twiggy.quickSetup(file=sys.stdout)

    assert twiggy.quick_setup.call_args_list == [mocker.call(), mocker.call(file=None),
                                                 mocker.call(file=sys.stdout)]


#
# Tests: add_emitters
#


def test_add_emitters(twiggy_output):
    def myfilt(msg):
        return True

    twiggy.add_emitters(('test', twiggy.levels.INFO, myfilt, twiggy_output))

    assert len(twiggy.emitters) == 1
    e = twiggy.emitters['test']
    assert isinstance(e, twiggy.filters.Emitter)
    assert e.min_level == twiggy.levels.INFO
    assert e.filter is myfilt
    assert e._output is twiggy_output


def test_addEmitters(twiggy_output, mocker):
    mocker.patch('twiggy.add_emitters')

    def myfilt(msg):
        return True

    emitters = ('test', twiggy.levels.INFO, myfilt, twiggy_output)
    twiggy.addEmitters(emitters)

    assert twiggy.add_emitters.call_args_list == [mocker.call(emitters)]


#
# Test that functions emit deprecation messages
#

@pytest.mark.usefixtures("deprecations_error")
@pytest.mark.parametrize('function, message', DEPRECATED_FUNCS)
def test_deprecated(function, message):
    with pytest.raises(DeprecationWarning) as exc:
        function()

    assert exc.value.args[0] == message
