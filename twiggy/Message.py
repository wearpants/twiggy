__all__ = ['Message']

import sys
import traceback

class Message(object):

    def __init__(self, level, format_spec, fields, options,
                 *args, **kwargs):

        self.format_spec = format_spec
        self.args = args
        self.kwargs = kwargs
        self.fields = fields
        self.suppress_newlines = options['suppress_newlines']
        self.fields['level'] = level

        ## format traceback
        # XXX this needs some cleanup/branch consolidation
        trace = options['trace']
        if isinstance(trace, tuple) and len(trace) == 3:
            self.traceback = "\n".join(traceback.format_exception(trace))
        elif trace == "error":
            tb = sys.exc_info()
            if tb[0] is None:
                self.traceback = None
            else:
                self.traceback = traceback.format_exc()
        elif trace == "always":
            pass
            # XXX build a traceback using getframe
            # XXX maybe an option to just provide current frame info instead of full stack?
        elif trace is not None:
            raise ValueError("bad trace {0!r}".format(trace))
        else:
            self.traceback = None

        self.substitute() # XXX it'd be nice to do this only if we're going to emit

    def substitute(self):
        ## call any callables
        for k, v in self.fields.iteritems():
            if callable(v):
                self.fields[k] = v()

        for k, v in self.kwargs.iteritems():
            if callable(v):
                self.kwargs[k] = v()

        self.args = tuple(v() if callable(v) else v for v in self.args)

        ## substitute
        if self.format_spec == '':
            self.text = ''
            return

        # XXX I doubt this works as intended in all cases
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

    @property
    def level(self):
        return self.fields['level']