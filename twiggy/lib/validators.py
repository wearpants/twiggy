from collections import Mapping, Sequence

from six import integer_types, string_types
from six.moves import builtins

from .. import formats
from .. import levels


def _import_module(module_name):
    # Python 2.6 compatibility
    fromlist = []
    try:
        fromlist.append(module_name[:module_name.rindex('.')])
    except ValueError:
        pass

    return __import__(module_name, fromlist=fromlist)


try:
    # Python-2.7+
    from importlib import import_module
except ImportError:  # pragma: no cover
    # Only needed on Python 2.6.x
    import_module = _import_module


def _string_to_attribute(value, type_='attribute'):
    """
    Tests whether a string is an importable attribute and returns the attribute

    :arg value: The string naming the attribute
    :returns: The attribute
    :raises ValueError: if the string is not an importable attribute
    """
    # For exception messages
    if type_[0] in ('a', 'e', 'i', 'o', 'u'):
        article = 'an'
    else:
        article = 'a'

    if not isinstance(value, string_types):
        raise ValueError('This value must be a string naming {0} {1}, not {2} of'
                         ' type {3}'.format(article, type_, value, type(value)))
    parts = value.split('.')

    # Test for an attribute in builtins named value
    if len(parts) == 1:
        try:
            attribute = getattr(builtins, value)
        except AttributeError:
            raise ValueError('Could not find {0} {1} named {2}'.format(article, type_, value))

        return attribute

    # Find a module that we can import
    module = None
    for idx in range(len(parts) - 1, 0, -1):
        try:
            module = import_module('.'.join(parts[:idx]))
        except Exception:
            pass
        else:
            remainder = parts[idx:]
            break
    else:  # For-else
        raise ValueError('Could not import a module with {0} {1} named'
                         ' {2}'.format(article, type_, value))

    # Handle both Staticmethod (ClassName.staticmethod) and module global
    # attribute (attributename)
    prev_part = module
    for next_part in remainder:
        try:
            prev_part = getattr(prev_part, next_part)
        except AttributeError:
            raise ValueError('Could not find {0} {1} named {2} in module'
                             ' {3}'.format(article, type_, '.'.join(remainder),
                                           '.'.join(parts[:idx])))
    attribute = prev_part
    return attribute


def _parse_external(value, function=False):
    """
    Check whether a string is marked as being an external resource and return the resource

    This function checks whether a string begins with ``ext://`` and if so it removes the ``ext://``
    and tries to import an attribute with that name.

    :arg value: The string to process
    :kwarg function: If True, make sure that the attribute found is a callable.  This will convert
        a string into a function or fail validation regardless of whether the string starts with
        ``ext://``. (Default False)
    :returns: If ``ext://`` was present or always is True then the imported attribute is returned.
        If not, then ``value`` is returned.
    :raises ValueError: if the string is not importable
    """
    external = False
    if isinstance(value, string_types):
        if value.startswith('ext://'):
            value = value[6:]
            external = True

    if not (external or function):
        return value

    if isinstance(value, string_types):
        attribute = _string_to_attribute(value, type_='function' if function else 'attribute')
    else:
        attribute = value

    if function:
        # Finally check that it is a callable
        if not callable(attribute):
            raise ValueError('Identifier named {0} is not a function'.format(value))
    return attribute


def _validate_config(config):
    """
    Validates and converts a twiggy configuration dictionary

    :arg config: The dictionary to configure twiggy with
    :raises ValueError: If the configuration is not valid
    :returns: A new dictionary with any values that we can automatically convert converted

    .. seealso:: :ref:`twiggy config schema`
    """
    new_cfg = {'outputs': {}, 'emitters': {}}
    if not isinstance(config, Mapping):
        raise ValueError("Configuration must be a dictionary")

    # Version
    if 'version' not in config:
        raise ValueError("Config dict must contain a 'version' key")
    if config['version'] != '1.0':
        raise ValueError("Valid configuration versions are: '1.0'")
    new_cfg['version'] = config['version']

    # Incremental
    if 'incremental' not in config:
        new_cfg['incremental'] = False
    elif isinstance(config['incremental'], bool):
        new_cfg['incremental'] = config['incremental']
    else:
        # Convert from to a bool
        incremental = config['incremental']
        if isinstance(incremental, string_types):
            incremental = incremental.lower()

        if incremental in (0, '0', 'false', 'no', 'off', 'disable'):
            new_cfg['incremental'] = False
        elif incremental in (1, '1', 'true', 'yes', 'on', 'enable'):
            new_cfg['incremental'] = True
        elif isinstance(incremental, integer_types):
            new_cfg['incremental'] = bool(incremental)
        else:
            raise ValueError("Configuration of `incremental` must be True or False")

    # Check whether outputs and emitters are set
    output_null = emitters_null = False
    if 'outputs' not in config or config['outputs'] is None:
        output_null = True
    if 'emitters' not in config or config['emitters'] is None:
        emitters_null = True

    if output_null and emitters_null:
        if new_cfg['incremental'] is False:
            # If neither outputs nor emitters is set, then we'll remove all emitters
            new_cfg['outputs'] = None
            new_cfg['emitters'] = None
            return new_cfg
        else:
            raise ValueError("Removing configuration by specifying no `outputs` and `emitters`"
                             " requires `incremental` to be False")
    if output_null or emitters_null:
        raise ValueError("`outputs` and `emitters` must both be specified or both must be empty")

    # Outputs
    if not isinstance(config['outputs'], Mapping):
        raise ValueError("`outputs` must be a dict mapping output_names to outputs")

    for output_name, output in config['outputs'].items():
        new_output = {'args': [], 'kwargs': {}, 'format': formats.line_format}

        if not isinstance(output, Mapping):
            raise ValueError("`outputs` must be a dict of dicts")

        if 'output' not in output:
            raise ValueError("Every entry in `outputs` must contain an `output` field")
        new_output['output'] = _parse_external(output['output'], function=True)

        if 'args' in output:
            if (not isinstance(output['args'], Sequence) or
                    isinstance(output['args'], string_types)):
                raise ValueError("The `args` entry in `outputs` must be a list")
            new_output['args'] = [_parse_external(s) for s in output['args']]

        if 'kwargs' in output:
            if not isinstance(output['kwargs'], Mapping):
                raise ValueError("The `kwargs` entry in `outputs` must be a dict")
            new_output['kwargs'] = dict((k, _parse_external(v)) for k, v in
                                        output['kwargs'].items())

        if 'format' in output:
            new_output['format'] = _parse_external(output['format'], function=True)

        new_cfg['outputs'][output_name] = new_output

    # Emitters
    if not isinstance(config['emitters'], Mapping):
        raise ValueError("`emitters` must be a dict mapping emitter names to emitters")

    for emitter_name, emitter in config['emitters'].items():
        new_emitter = {'filters': []}

        if not isinstance(emitter_name, string_types):
            raise ValueError("`emitters` keys must be strings")

        if not isinstance(emitter, Mapping):
            raise ValueError("`emitters` must be a dict of dicts")

        if 'level' not in emitter:
            raise ValueError("Every entry in `emitters` must contain a `level` field")
        if isinstance(emitter['level'], string_types):
            try:
                level = levels.name2level(emitter['level'])
            except KeyError:
                raise ValueError("The `level` field of `emitters` must be the string name of"
                                 " a twiggy log level")
        else:
            level = emitter['level']
        if not isinstance(level, levels.LogLevel):
            raise ValueError("The `level` field of `emitters` must be a string naming"
                             " a Twiggy LogLevel")
        new_emitter['level'] = level

        if 'output_name' not in emitter:
            raise ValueError("Every entry in `emitters` must contain an `output_name` field")
        if emitter['output_name'] not in new_cfg['outputs']:
            raise ValueError("`output_name` must match with the name of one of the entries"
                             " in `outputs`")
        new_emitter['output_name'] = emitter['output_name']

        if 'filters' in emitter:
            if (not isinstance(emitter['filters'], Sequence) or
                    isinstance(emitter['filters'], string_types)):
                raise ValueError("The `['emitters']['filters']` entry must be a list")
            for filt in emitter['filters']:
                new_filter = {'args': [], 'kwargs': {}}

                if not isinstance(filt, Mapping):
                    raise ValueError("The entries in `['emitters']['filters']` must be a dict")
                if 'filter' not in filt:
                    raise ValueError("Entries in the `filters` list must contain a filter field")
                new_filter['filter'] = _parse_external(filt['filter'], function=True)

                if 'args' in filt:
                    if (not isinstance(filt['args'], Sequence) or
                            isinstance(filt['args'], string_types)):
                        raise ValueError("The `args` entry in `['emitters']['filters']`"
                                         " must be a list")
                    new_filter['args'] = [_parse_external(s) for s in filt['args']]

                if 'kwargs' in filt:
                    if not isinstance(filt['kwargs'], Mapping):
                        raise ValueError("The `kwargs` entry in `['emitters']['filters']`"
                                         " must be a dict")
                    new_filter['kwargs'] = dict((k, _parse_external(v)) for k, v in
                                                filt['kwargs'].items())

                new_emitter['filters'].append(new_filter)

        new_cfg['emitters'][emitter_name] = new_emitter

    return new_cfg
