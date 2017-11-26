import re
import sys

import pytest

from twiggy.lib.validators import (_import_module, _string_to_attribute, _parse_external)


INVALID_ATTRIBUTES = (
    (5, "This value must be a string naming {0}, not 5 of type <(class|type) 'int'>"),
    ('nonexistent', 'Could not find {0} named nonexistent'),
    ('does.not.exist', 'Could not import a module with {0} named does.not.exist'),
    ('itertools.does.not.exist', 'Could not find {0} named does.not.exist in module'
        ' itertools'),
    ('os.nonexistent', 'Could not find {0} named nonexistent in module os'),
)

INVALID_FUNCTIONS = INVALID_ATTRIBUTES[1:] + (
    (5, "Identifier named 5 is not a function"),
    ('os.F_OK', 'Identifier named os.F_OK is not a function'),
)


def function_for_testing(value):
    pass


def test_import_module_backport():
    os_via_import_module = _import_module('os')
    import os
    assert os_via_import_module == os

    os_path_via_import_module = _import_module('os.path')
    import os.path
    assert os_path_via_import_module == os.path


class TestStringToAttribute(object):
    def test_valid_builtin(self):

        # A toplevel function
        assert _string_to_attribute('dir', type_='function') == dir

    def test_valid_attribute_pre_import(self):
        f_ok_via_validator = _string_to_attribute('os.F_OK')
        from os import F_OK
        assert f_ok_via_validator == F_OK

    def test_valid_attribute_post_import(self):
        from os import F_OK
        f_ok_via_validator = _string_to_attribute('os.F_OK')
        assert f_ok_via_validator == F_OK

    def test_valid_function_pre_import(self):
        # A function inside a module
        chain_via_validator = _string_to_attribute('itertools.chain', type_='function')
        from itertools import chain
        assert chain_via_validator == chain

    def test_valid_function_post_import(self):
        # A function from inside a module after the module has been imported
        from itertools import chain
        chain_via_validator = _string_to_attribute('itertools.chain', type_='function')
        assert chain_via_validator == chain

    def test_valid_method_pre_import(self):
        # Test that it returns a classmethod
        from_file_via_validator = _string_to_attribute('tarfile.TarInfo.frombuf', type_='function')
        from tarfile import TarInfo
        assert from_file_via_validator == TarInfo.frombuf

    def test_valid_method_post_import(self):
        # Test that it returns a classmethod after the module has been imported
        from tarfile import TarInfo
        from_file_via_validator = _string_to_attribute('tarfile.TarInfo.frombuf', type_='function')
        assert from_file_via_validator == TarInfo.frombuf

    @pytest.mark.parametrize("value, message", INVALID_ATTRIBUTES)
    def test_invalid_attributes(self, value, message):
        with pytest.raises(ValueError) as exc:
            _string_to_attribute(value, type_='attribute')
        assert re.search(message.format('an attribute'), exc.value.args[0])

    @pytest.mark.parametrize("value, message", INVALID_ATTRIBUTES)
    def test_invalid_functions(self, value, message):
        with pytest.raises(ValueError) as exc:
            _string_to_attribute(value, type_='function')
        assert re.search(message.format('a function'), exc.value.args[0])


class TestParseExternal(object):
    def test_not_external_string(self):
        assert _parse_external('normal string') == 'normal string'

    def test_not_external_function(self):
        assert _parse_external(function_for_testing) == function_for_testing

    def test_not_external_function_requested(self):
        assert _parse_external(function_for_testing, function=True) == function_for_testing

    def test_explicit_external_attribute(self):
        assert _parse_external('ext://sys.stdin') == sys.stdin

    def test_explicit_external_function(self):
        import itertools
        assert _parse_external('ext://itertools.chain') == itertools.chain

    def test_external_function(self):
        import itertools
        assert _parse_external('itertools.chain', function=True) == itertools.chain

    def test_both_explicit_and_external_function(self):
        import itertools
        assert _parse_external('ext://itertools.chain', function=True) == itertools.chain

    @pytest.mark.parametrize("value, message", INVALID_FUNCTIONS)
    def test_invalid_functions(self, value, message):
        with pytest.raises(ValueError) as exc:
            _parse_external(value, function=True)
        assert re.search(message.format('a function'), exc.value.args[0])
