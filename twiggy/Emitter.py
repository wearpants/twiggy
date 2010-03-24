import time
from .lib import ConversionTable, Converter

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

class StandardEmitter(Emitter):

    def __init__(self, min_level, separator=':', traceback_prefix='\nTRACE ', **kwargs):
        self.separator = separator
        self.traceback_prefix = traceback_prefix
        super(StandardEmitter, self).__init__(min_level, **kwargs)

        # XXX entirely insufficient
        self.conversion_table = ConversionTable([
            Converter('time', time.ctime, '{1}'.format, True),
            Converter('name', str, '{1}'.format),
            Converter('level', str, '{1}'.format, True),
        ])

        self.conversion_table.genericValue = str
        self.conversion_table.genericItem = "{0}={1}".format
        self.conversion_table.aggregate = self.separator.join

    def format(self, msg):
        fields = self.format_fields(msg)
        text = self.format_text(msg)
        trace = self.format_traceback(msg)
        return "{fields}{self.separator}{text}{trace}".format(**locals()) # XXX gross?


    def format_text(self, msg):
        if msg.suppress_newlines:
            return msg.text.replace('\n', '\\n')
        else:
            return msg.text

    def format_traceback(self, msg):
        if msg.traceback is not None:
            # XXX this could be faster
            l = msg.traceback.split('\n')
            l = [""] + l[:-1]
            return self.traceback_prefix.join(l)
        else:
            return ""

    def format_fields(self, msg):
        return self.conversion_table.convert(msg.fields)

    def output(self, msg, s):
        print s


