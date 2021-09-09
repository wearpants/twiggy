import copy
import json

from .lib.converter import ConversionTable, Converter
from .lib.json import TwiggyJSONEncoder
from .lib import iso8601time

#: a default line-oriented converter
line_conversion = ConversionTable([
    Converter(key='time',
              # ISO 8601 - it sucks less!
              convert_value=iso8601time,
              convert_item='{1}'.format,
              required=True),
    ('level', str, '{1}'.format, True),
    ('name', str, '{1}'.format),
])

line_conversion.generic_value = str
line_conversion.generic_item = "{0}={1}".format
line_conversion.aggregate = ':'.join


class LineFormat(object):
    """format a message for text-oriented output. Returns a string."""

    def __init__(self, separator='|', traceback_prefix='\nTRACE ', conversion=line_conversion):
        self.separator = separator
        self.traceback_prefix = traceback_prefix
        self.conversion = conversion

    # XXX test this!
    def __copy__(self):
        return self.__class__(self.separator, self.traceback_prefix, self.conversion.copy())

    def __call__(self, msg):
        fields = self.format_fields(msg)
        text = self.format_text(msg)
        trace = self.format_traceback(msg)
        return "{fields}{self.separator}{text}{trace}\n".format(**locals())  # XXX gross?

    def format_text(self, msg):
        """format the text part of a message"""
        if msg.suppress_newlines:
            return msg.text.replace('\n', '\\n')
        else:
            return msg.text

    def format_traceback(self, msg):
        """format the traceback part of a message"""
        if msg.traceback is not None:
            # XXX this could be faster
            lines = msg.traceback.split('\n')
            lines = [""] + lines[:-1]
            return self.traceback_prefix.join(lines)
        else:
            return ""

    def format_fields(self, msg):
        """format the fields of a message"""
        fields_text = self.conversion.convert(msg.fields)
        if msg.suppress_newlines:
            fields_text = fields_text.replace('\n', '\\n')
        return fields_text


#
# some useful default objects
#

#: a decent-looking format for line-oriented output
line_format = LineFormat(conversion=line_conversion)

#: a format for use in the shell - no timestamp
shell_format = copy.copy(line_format)
shell_format.conversion.get('time').convert_item = lambda k, v: None

import json

class JSONFormat(object):
    """format messages to JSON. Returns a string.

    The resulting JSON will have keys: `text`, `traceback` (possibly null) and `fields`.
    Set `inline_fields` to True to include fields directly instead.

    :ivar bool inline_fields: hoist individual fields to top-level keys. Defaults to False.
    :ivar dict kwargs: extra keyword arguments to pass to `json.dumps()`
    """

    def __init__(self, inline_fields=False, **kwargs):
        self.inline_fields = inline_fields
        self.kwargs = kwargs

    def __call__(self, msg):
        # XXX this ignores msg.suppress_newlines. Hmm.
        return json.dumps(
            {'text': msg.text,
             'traceback': msg.traceback,
             **(msg.fields if self.inline_fields else {'fields': msg.fields})},
            cls=TwiggyJSONEncoder, **self.kwargs)
