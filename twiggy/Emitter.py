class Emitter(object):
    # XXX ABC me!
    def __init__(self, level):
        self.level = level

    def filter(self, msg):
        return True

    def format(self, msg):
        raise NotImplementedError

    def output(self, msg, s):
        raise NotImplementedError

    def handle(self, msg):
        msg.populate()
        print msg.fields
        if self.filter(msg):
            msg.substitute()
            s = self.format(msg)
            self.output(msg, s)

class StandardEmitter(Emitter):

    fields_order = ['time']

    def __init__(self, level, separator=':', **kwargs):
        self.separator = separator
        super(StandardEmitter, self).__init__(level, **kwargs)

    def format(self, msg):
        if 0:
            import Message
            assert isinstance(msg, Message.Message)

        cols = [msg.fields[f] for f in self.fields_order]
        cols.append(msg.text)
        s = self.separator.join(cols)

    def output(self, msg, s):
        print s

