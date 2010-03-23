__all__ = ['Message']

import sys

class Message(object):

    def __init__(self, level, format_spec, fields,
                 suppress_newlines = True, trace = None,
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
            pass
            # XXX build a traceback using getframe
            # XXX maybe an option to just provide current frame info instead of full stack?
        elif trace is not None:
            raise ValueError("bad trace %r"%trace)

        def doit(d):
            for k, v in d.iteritems():
                if callable(v):
                    d[k] = v()

        doit(self.fields)
        doit(self.kwargs)

        self.args = tuple(v() if callable(v) else v for v in self.args)

        if self.format_spec == '':
            s.text = ''
            return

        s = self.format_spec.format(*self.args, **self.kwargs)
        if s == self.format_spec:
            # a % style format
            if self.args and self.kwargs:
                raise ValueError("can't have both args & kwargs with % style format specs")
            else:
                s = self.format_spec % (self.args or self.kwargs)

        self.text = s

    @property
    def name(self):
        return self.fields.get('name', '')