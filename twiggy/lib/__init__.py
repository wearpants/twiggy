from collections import namedtuple

# XXX this prolly needs a 'required' field...
Converter = namedtuple('Converter', ['name', 'convertValue', 'convertItem', 'required'])

class ConversionTable(list):

    def __init__(self, seq):
        super(ConversionTable, self).__init__(seq)
        # XXX cache converts & requireds below

    def genericValue(self, value):
        return value

    def genericItem(self, name, value):
        return name, value

    def aggregate(self, converteds):
        return dict(converteds)

    def convert(self, d):
        # XXX I could be much faster & efficient!
        # XXX I have written this pattern at least 10 times
        converts = set(x.name for x in self)
        avail = set(d.iterkeys())
        required = set(x.name for x in self if x.required)
        missing = required - avail

        if missing:
            raise ValueError("Missing fields {0}".format(list(missing)))

        l = []
        for c in self:
            if c.name in d:
                l.append(c.convertItem(c.name, c.convertValue(d[c.name])))

        for name in sorted(avail - converts):
            l.append(self.genericItem(name, self.genericValue(d[name])))

        return self.aggregate(l)

