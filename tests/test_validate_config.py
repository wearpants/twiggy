import copy
import pytest

import twiggy
from twiggy.lib.validators import _validate_config


BASE_CONFIG = [[{
    'version': '1.0',
    'incremental': 'faLse',
    'outputs': {
        'out1': {
            'output': 'twiggy.outputs.StreamOutput',
            'args': ['one'],
            'kwargs': {'stream': 'testing1'},
            'format': 'twiggy.formats.shell_format'
        },
    },
    'emitters': {
        'some': {
            'level': 'WARNING',
            'filters': [
                {'filter': 'twiggy.filters.names',
                 'args': ['a', 'b'],
                 'kwargs': {'test': 'case'}
                 },
            ],
            'output_name': 'out1'
        },
    }
},
    {
    'version': '1.0',
    'incremental': False,
    'outputs': {
        'out1': {
            'output': twiggy.outputs.StreamOutput,
            'args': ['one'],
            'kwargs': {'stream': 'testing1'},
            'format': twiggy.formats.shell_format
        },
    },
    'emitters': {
        'some': {
            'level': twiggy.levels.WARNING,
            'filters': [
                {'filter': twiggy.filters.names,
                 'args': ['a', 'b'],
                 'kwargs': {'test': 'case'}
                 },
            ],
            'output_name': 'out1'
        },
    }
}]]


def build_valid_cfg():
    valid_configs = copy.deepcopy(BASE_CONFIG)
    valid_configs[0][1]['outputs']['out1']['format'] = twiggy.formats.shell_format

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['incremental']
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = True
    new_valid[1]['incremental'] = True
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = 1
    new_valid[1]['incremental'] = True
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = 0
    new_valid[1]['incremental'] = False
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = 100
    new_valid[1]['incremental'] = True
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = 'false'
    new_valid[1]['incremental'] = False
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['incremental'] = 'TRue'
    new_valid[1]['incremental'] = True
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['outputs']
    del new_valid[0]['emitters']
    new_valid[1]['outputs'] = None
    new_valid[1]['emitters'] = None
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    new_valid[0]['outputs'] = None
    new_valid[0]['emitters'] = None
    new_valid[1]['outputs'] = None
    new_valid[1]['emitters'] = None
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['outputs']['out1']['args']
    del new_valid[0]['outputs']['out1']['kwargs']
    new_valid[1]['outputs']['out1']['args'] = []
    new_valid[1]['outputs']['out1']['kwargs'] = {}
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    del new_valid[0]['outputs']['out1']['format']
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.line_format
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['emitters']['some']['filters']
    new_valid[1]['emitters']['some']['filters'] = []
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['emitters']['some']['filters'][0]['args']
    new_valid[1]['emitters']['some']['filters'][0]['args'] = []
    valid_configs.append(new_valid)

    new_valid = copy.deepcopy(BASE_CONFIG[0])
    new_valid[1]['outputs']['out1']['format'] = twiggy.formats.shell_format
    del new_valid[0]['emitters']['some']['filters'][0]['kwargs']
    new_valid[1]['emitters']['some']['filters'][0]['kwargs'] = {}
    valid_configs.append(new_valid)

    return valid_configs


def build_invalid_cfg():
    invalid_configs = [({}, r"Config dict must contain a 'version' key"),
                       ([], r"Configuration must be a dictionary"),
                       ]

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid["version"]
    invalid_configs.append((new_invalid, "Config dict must contain a 'version' key"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid.update({"version": "0.2"})
    invalid_configs.append((new_invalid, "Valid configuration versions are: '1.0'"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid.update({"version": 1.0})
    invalid_configs.append((new_invalid, "Valid configuration versions are: '1.0'"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['incremental'] = 'NOT_VALID'
    invalid_configs.append((new_invalid, "Configuration of `incremental` must be True or False"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['emitters']
    del new_invalid['outputs']
    new_invalid['incremental'] = True
    invalid_configs.append((new_invalid, "Removing configuration by specifying no `outputs` and"
                            " `emitters` requires `incremental` to be False"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['outputs']
    invalid_configs.append((new_invalid, "`outputs` and `emitters` must both be specified or both"
                            " must be empty"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['emitters']
    invalid_configs.append((new_invalid, "`outputs` and `emitters` must both be specified or both"
                            " must be empty"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs'] = None
    invalid_configs.append((new_invalid, "`outputs` and `emitters` must both be specified or both"
                            " must be empty"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters'] = None
    invalid_configs.append((new_invalid, "`outputs` and `emitters` must both be specified or both"
                            " must be empty"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs'] = 'INVALID'
    invalid_configs.append((new_invalid, "`outputs` must be a dict mapping output_names"
                            " to outputs"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs']['out1'] = 'INVALID'
    invalid_configs.append((new_invalid, "`outputs` must be a dict of dicts"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['outputs']['out1']['output']
    invalid_configs.append((new_invalid, "Every entry in `outputs` must contain an `output` field"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs']['out1']['output'] = 'not.a.function.name'
    invalid_configs.append((new_invalid, "Could not import a module with a function"
                            " named not.a.function.name"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs']['out1']['args'] = 'string'
    invalid_configs.append((new_invalid, "The `args` entry in `outputs` must be a list"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs']['out1']['kwargs'] = 'string'
    invalid_configs.append((new_invalid, "The `kwargs` entry in `outputs` must be a dict"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['outputs']['out1']['format'] = 'not.a.function.name'
    invalid_configs.append((new_invalid, "Could not import a module with a function"
                            " named not.a.function.name"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters'] = []
    invalid_configs.append((new_invalid, "`emitters` must be a dict mapping emitter names"
                            " to emitters"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    emitter_1 = new_invalid['emitters']['some']
    del new_invalid['emitters']['some']
    new_invalid['emitters'][1] = emitter_1
    invalid_configs.append((new_invalid, "`emitters` keys must be strings"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some'] = []
    invalid_configs.append((new_invalid, "`emitters` must be a dict of dicts"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['emitters']['some']['level']
    invalid_configs.append((new_invalid, "Every entry in `emitters` must contain a `level` field"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['level'] = 'NOT_VALID'
    invalid_configs.append((new_invalid, "The `level` field of `emitters` must be the string"
                            " name of a twiggy log level"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['level'] = object()
    invalid_configs.append((new_invalid, "The `level` field of `emitters` must be a string"
                            " naming a Twiggy LogLevel"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['emitters']['some']['output_name']
    invalid_configs.append((new_invalid, "Every entry in `emitters` must contain an"
                            " `output_name` field"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['output_name'] = 'NOT_VALID'
    invalid_configs.append((new_invalid, "`output_name` must match with the name of one of the"
                            " entries in `outputs`"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['filters'] = 'string'
    invalid_configs.append((new_invalid, "The `['emitters']['filters']` entry must be a list"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['filters'][0] = 'string'
    invalid_configs.append((new_invalid, "The entries in `['emitters']['filters']` must be a dict"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    del new_invalid['emitters']['some']['filters'][0]['filter']
    invalid_configs.append((new_invalid, "Entries in the `filters` list must contain a"
                            " filter field"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['filters'][0]['filter'] = 'not.a.function.name'
    invalid_configs.append((new_invalid, "Could not import a module with a function"
                            " named not.a.function.name"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['filters'][0]['args'] = 'string'
    invalid_configs.append((new_invalid, "The `args` entry in `['emitters']['filters']`"
                            " must be a list"))

    new_invalid = copy.deepcopy(VALID_CONFIGS[0][0])
    new_invalid['emitters']['some']['filters'][0]['kwargs'] = 'string'
    invalid_configs.append((new_invalid, "The `kwargs` entry in `['emitters']['filters']`"
                            " must be a dict"))

    return invalid_configs


VALID_CONFIGS = build_valid_cfg()
INVALID_CONFIGS = build_invalid_cfg()


def test_valid_config_programmatic():
    """When hardcoded in the program, the dict can directly use the twiggy objects."""
    assert _validate_config(VALID_CONFIGS[0][1]) == VALID_CONFIGS[0][1]


@pytest.mark.parametrize('in_cfg, out_cfg', VALID_CONFIGS)
def test_valid_configs(in_cfg, out_cfg):
    assert _validate_config(in_cfg) == out_cfg


@pytest.mark.parametrize('cfg, msg', INVALID_CONFIGS)
def test_invalid_configs(cfg, msg):
    with pytest.raises(ValueError) as err:
        _validate_config(cfg)
    assert err.value.args[0] == msg
