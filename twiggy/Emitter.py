class Emitter(object):
    # XXX ABC me!
    def __init__(self, level):
        self.level = level

    def filter(self, msg):
        pass

    def format(self, msg):
        pass

    def output(self, msg, s):
        pass

    def handle(self, msg):
        if self.filter(msg):
            s = self.format(msg)
            self.output(msg, s)
