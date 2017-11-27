import copy

import pytest
from six import StringIO

import twiggy

#
# Tests: dict_config
#

VALID_CONFIG = {
    'version': '1.0',
    'incremental': False,
    'outputs': {
        'out1': {
            'output': 'twiggy.outputs.StreamOutput',
            'kwargs': {'stream': 'testing1'},
        },
        'out2': {
            'output': 'twiggy.outputs.StreamOutput',
            'kwargs': {'stream': 'testing2'},
            'format': 'twiggy.formats.shell_format'
        },
    },
    'emitters': {
        'all': {
            'level': 'DEBUG',
            'output_name': 'out1'
        },
        'some': {
            'level': 'WARNING',
            'filters': [
                {'filter': 'twiggy.filters.names',
                 'args': ['a', 'b'],
                 'kwargs': {}
                 },
                {'filter': 'twiggy.filters.names',
                 'args': ['c', 'd'],
                 'kwargs': {}
                 },
            ],
            'output_name': 'out2'
        },
    }
}


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


def test_dict_config_invalid(internal_log):
    with pytest.raises(ValueError) as excinfo:
        twiggy.dict_config({})
        assert excinfo.value.message == "Config dict must contain a 'version' key"


def test_dict_config_valid(mocker):
    def return_how_called(*args, **kwargs):
        return (args, kwargs)

    cfg = copy.deepcopy(VALID_CONFIG)

    add_emitters = mocker.patch('twiggy.add_emitters')
    mocker.patch('twiggy.emitters')
    emitters_dict_clear = mocker.patch('twiggy.emitters.clear')
    mocker.patch('twiggy.filters.names', return_how_called)

    twiggy.dict_config(cfg)

    assert emitters_dict_clear.call_args_list == [mocker.call()]

    assert len(add_emitters.call_args_list) == 1
    assert len(add_emitters.call_args_list[0][0]) == 2

    # call_args_list is nested like this: [call(positional_args(first_emitter)),]
    # We expect to have called add_emitters once with two positional args which are
    # themselves tuples
    if add_emitters.call_args_list[0][0][0][0] == 'all':
        all_emitter = add_emitters.call_args_list[0][0][0]
        some_emitter = add_emitters.call_args_list[0][0][1]
    else:
        some_emitter = add_emitters.call_args_list[0][0][0]
        all_emitter = add_emitters.call_args_list[0][0][1]

    assert all_emitter[0] == 'all'
    assert all_emitter[1] == twiggy.levels.DEBUG
    assert all_emitter[2] is None
    assert isinstance(all_emitter[3], twiggy.outputs.StreamOutput)
    assert all_emitter[3]._format == twiggy.formats.line_format
    assert all_emitter[3].stream == 'testing1'

    assert some_emitter[0] == 'some'
    assert some_emitter[1] == twiggy.levels.WARNING
    assert some_emitter[2] == [(('a', 'b'), {}), (('c', 'd'), {})]
    assert isinstance(some_emitter[3], twiggy.outputs.StreamOutput)
    assert some_emitter[3]._format == twiggy.formats.shell_format
    assert some_emitter[3].stream == 'testing2'


def test_dict_config_incremental_true(mocker):
    def return_how_called(*args, **kwargs):
        return (args, kwargs)

    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['some']
    cfg['incremental'] = True

    add_emitters = mocker.patch('twiggy.add_emitters')
    mocker.patch('twiggy.emitters')
    emitters_dict_clear = mocker.patch('twiggy.emitters.clear')
    mocker.patch('twiggy.filters.names', return_how_called)

    twiggy.dict_config(cfg)

    assert emitters_dict_clear.call_args_list == []

    assert len(add_emitters.call_args_list) == 1
    assert len(add_emitters.call_args_list[0][0]) == 1

    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['all']
    cfg['incremental'] = True

    twiggy.dict_config(cfg)

    assert emitters_dict_clear.call_args_list == []

    assert len(add_emitters.call_args_list) == 2
    assert len(add_emitters.call_args_list[0][0]) == 1
    assert len(add_emitters.call_args_list[1][0]) == 1

    # call_args_list is nested like this: [call(positional_args(first_emitter)),]
    # We expect to have called add_emitters twice with one positional arg each time
    all_emitter = add_emitters.call_args_list[0][0][0]
    some_emitter = add_emitters.call_args_list[1][0][0]

    assert all_emitter[0] == 'all'
    assert all_emitter[1] == twiggy.levels.DEBUG
    assert all_emitter[2] is None
    assert isinstance(all_emitter[3], twiggy.outputs.StreamOutput)
    assert all_emitter[3]._format == twiggy.formats.line_format
    assert all_emitter[3].stream == 'testing1'

    assert some_emitter[0] == 'some'
    assert some_emitter[1] == twiggy.levels.WARNING
    assert some_emitter[2] == [(('a', 'b'), {}), (('c', 'd'), {})]
    assert isinstance(some_emitter[3], twiggy.outputs.StreamOutput)
    assert some_emitter[3]._format == twiggy.formats.shell_format
    assert some_emitter[3].stream == 'testing2'


def test_dict_config_incremental_false_order(mocker):
    """
    With incremental=false it is important that the dictionary is cleared before the emitter is
    added.  We'll do this by testing the emitters dict instead of a mock
    """
    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['some']

    twiggy.dict_config(cfg)

    assert len(twiggy.emitters) == 1
    assert 'all' in twiggy.emitters

    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['all']

    twiggy.dict_config(cfg)

    assert len(twiggy.emitters) == 1
    assert 'some' in twiggy.emitters


def test_dict_config_incremental_false_contents(mocker):
    def return_how_called(*args, **kwargs):
        return (args, kwargs)

    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['some']

    add_emitters = mocker.patch('twiggy.add_emitters')
    mocker.patch('twiggy.emitters')
    emitters_dict_clear = mocker.patch('twiggy.emitters.clear')
    mocker.patch('twiggy.filters.names', return_how_called)

    twiggy.dict_config(cfg)

    assert emitters_dict_clear.call_args_list == [mocker.call()]

    assert len(add_emitters.call_args_list) == 1
    assert len(add_emitters.call_args_list[0][0]) == 1

    the_emitter = add_emitters.call_args_list[0][0][0]

    assert the_emitter[0] == 'all'
    assert the_emitter[1] == twiggy.levels.DEBUG
    assert the_emitter[2] is None
    assert isinstance(the_emitter[3], twiggy.outputs.StreamOutput)
    assert the_emitter[3]._format == twiggy.formats.line_format
    assert the_emitter[3].stream == 'testing1'

    cfg = copy.deepcopy(VALID_CONFIG)
    del cfg['emitters']['all']

    twiggy.dict_config(cfg)

    # Note: This does not check that the clear call happens before the add_emitters call.
    # The test_dict_config_incremental_false_order() check takes care of that.
    assert emitters_dict_clear.call_args_list == [mocker.call(), mocker.call()]

    assert len(add_emitters.call_args_list) == 2
    assert len(add_emitters.call_args_list[1][0]) == 1

    the_emitter = add_emitters.call_args_list[1][0][0]

    assert the_emitter[0] == 'some'
    assert the_emitter[1] == twiggy.levels.WARNING
    assert the_emitter[2] == [(('a', 'b'), {}), (('c', 'd'), {})]
    assert isinstance(the_emitter[3], twiggy.outputs.StreamOutput)
    assert the_emitter[3]._format == twiggy.formats.shell_format
    assert the_emitter[3].stream == 'testing2'
