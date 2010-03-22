__all__ = ['Message']

import sys

class Message(object):

    def __init__(self, level, format_spec, fields,
                 suppress_newlines = True, trace = None, source = False,
                 *args, **kwargs):

        self.level = level
        self.format_spec = format_spec
        self.args = args
        self.kwargs = kwargs
        self.fields = fields
        self.suppress_newlines = suppress_newlines

        if isinstance(trace, tuple):
            assert len(trace) == 3
            self.traceback = trace
        elif trace == "error":
            tb = sys.exc_info()
            if tb[0] is None:
                self.traceback = None
            else:
                self.traceback = tb
        elif trace == "always":
            # XXX build a traceback using getframe
        elif trace is not None:
            raise ValueError("bad trace %r"%trace)

        if source:
            # XXX calculate source line & module
            pass

    def substitute(self):
        s = self.format_spec.format(*self.args, **self.kwargs)
        if s == self.format_spec:
            # a % style format
            if args and kwargs:
                raise ValueError("can't have both args & kwargs with % style format specs")
            else:
                s = self.format_spec % (args or kwargs)

        if self.suppress_newlines:
            s = s.replace('\n', '\\n')

        self.text = s

    @property
    def name(self):
        try:
            return self.fields['name']
        except KeyError:
            raise AttributeError