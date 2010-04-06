class Converter(object):
    __slots__ = ['key', 'convertValue', 'convertItem', 'required']

    def __init__(self, key, convertValue, convertItem, required = False):
        self.key = key
        self.convertValue = convertValue
        self.convertItem = convertItem
        self.required = required

class ConversionTable(list):

    def __init__(self, seq):
        l = []
        for i in seq:
            if isinstance(i, Converter):
                l.append(i)
            elif isinstance(i, (tuple, list)) and len(i) in (3, 4):
                l.append(Converter(*i))
            elif isinstance(i, dict):
                l.append(Converter(**i))
            else:
                raise ValueError("Bad converter: {0!r}".format(i))

        super(ConversionTable, self).__init__(l)
        # XXX cache converts & requireds below

    def genericValue(self, value):
        return value

    def genericItem(self, key, value):
        return key, value

    def aggregate(self, converteds):
        return dict(converteds)

    def convert(self, d):
        # XXX I could be much faster & efficient!
        # XXX I have written this pattern at least 10 times
        converts = set(x.key for x in self)
        avail = set(d.iterkeys())
        required = set(x.key for x in self if x.required)
        missing = required - avail

        if missing:
            raise ValueError("Missing fields {0}".format(list(missing)))

        l = []
        for c in self:
            if c.key in d:
                item = c.convertItem(c.key, c.convertValue(d[c.key]))
                if item is not None:
                    l.append(item)

        for key in sorted(avail - converts):
            item = self.genericItem(key, self.genericValue(d[key]))
            if item is not None:
                l.append(item)

        return self.aggregate(l)

