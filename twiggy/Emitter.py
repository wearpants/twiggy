class Emitter(object):
    # XXX ABC me!
    def __init__(self, level):
        self.level = level

    def filter(self, msg):
        return True

    def format(self, msg):
        raise NotImplementedError

    def output(self, msg, fields, text):
        raise NotImplementedError

    def handle(self, msg):
        if self.filter(msg):
            s = self.format(msg)
            self.output(msg, s)

class StandardEmitter(Emitter):

    def __init__(self, level, separator=':', field_separator='=',
                 **kwargs):
        self.separator = separator
        self.field_separtor = field_separator
        super(StandardEmitter, self).__init__(level, **kwargs)

        # XXX entirely insufficient
        self.fields_map = [('time', '{0:f}'.format)]

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
        # XXX this too
        l = [stringify(msg.fields[f]) for (f, stringify) in self.fields_map]
        return self.separator.join(l)

    def output(self, msg, s):
        print s

