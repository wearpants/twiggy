from collections import namedtuple
import time

class Emitter(object):
    # XXX ABC me!
    def __init__(self, min_level):
        self.min_level = min_level

    def filter(self, msg):
        return True

    def format(self, msg):
        raise NotImplementedError

    def output(self, msg, fields, text):
        raise NotImplementedError

    def emit(self, msg):
        if self.filter(msg):
            s = self.format(msg)
            self.output(msg, s)

# XXX this prolly needs a 'required' field...
FieldConverter = namedtuple('FieldConverter', ['name', 'toString', 'toColumn'])

class StandardEmitter(Emitter):

    def __init__(self, min_level, separator=':', **kwargs):
        self.separator = separator
        super(StandardEmitter, self).__init__(min_level, **kwargs)

        # XXX entirely insufficient
        self.converters = [
            FieldConverter('time', time.ctime, '{1}'.format),
            FieldConverter('name', str, '{1}'.format),
            FieldConverter('level', str, '{1}'.format),
        ]

    @staticmethod
    def unknown_toString(x):
        return str(x)

    @staticmethod
    def unknown_toColumn(name, value):
        return "{0}={1}".format(name, value)

    def format(self, msg):
        fields = self.format_fields(msg)
        text = self.format_text(msg)
        return self.separator.join((fields, text))

    def format_text(self, msg):
        if msg.suppress_newlines:
            return msg.text.replace('\n', '\\n')
        else:
            return msg.text

    def format_fields(self, msg):
        # XXX I could be much faster & efficient!
        # XXX needs to deal with required fields
        # XXX I have written this pattern at least 10 times
        converts = set(x.name for x in self.converters)
        fields = set(msg.fields.iterkeys())

        unknowns = fields - converts
        knowns = fields & converts

        l = []
        for name, toString, toColumn in self.converters:
            if name in knowns:
                l.append(toColumn(name, toString(msg.fields[name])))

        for name in sorted(unknowns):
            l.append(self.unknown_toColumn(self.unknown_toString(msg.fields[name])))

        return self.separator.join(l)

    def output(self, msg, s):
        print s


