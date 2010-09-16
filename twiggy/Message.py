__all__ = ['Message']

import sys
import traceback
from string import Template

class Message(object):

    # don't change these!
    _default_options = {'suppress_newlines' : True,
                        'trace' : None,
                        'style': 'braces'}

    # XXX I need a __repr__!

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

        style = options['style']
        ## XXX maybe allow '%', '$', and '{}' as aliases?
        if style not in ('braces', 'percent', 'dollar'):
            raise ValueError("Bad format spec style {0!r}".format(style))
        else:
            self.style = style


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

        if self.style == 'braces':
            s = self.format_spec.format(*self.args, **self.kwargs)
        elif self.style == 'percent':
            # a % style format
            if self.args and self.kwargs:
                raise ValueError("can't have both args & kwargs with % style format specs")
            else:
                s = self.format_spec % (self.args or self.kwargs)
        elif self.style == 'dollar':
            if self.args:
                raise ValueError("can't use args with $ style format specs")
            s = Template(self.format_spec).substitute(self.kwargs)
        else:
            assert False, "impossible style"

        self.text = s

    @property
    def name(self):
        return self.fields.get('name', '')

    @property
    def level(self):
        return self.fields['level']