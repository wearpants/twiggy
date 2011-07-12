import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
        
from twiggy.lib.converter import Converter, ConversionTable

def convVal(x):
    return x

def convItem(x, y):
    return x, y

class ConverterTestCase(unittest.TestCase):

    def test_repr(self):
        c = Converter("pants", convVal, convItem)
        assert repr(c) == "<Converter('pants')>"

class ConversionTableTestCase(unittest.TestCase):

    def test_init_None(self):
        ct = ConversionTable()
        assert len(ct) == 0

    def test_init_simple(self):
        c = Converter("pants", convVal, convItem)
        ct = ConversionTable([c])
        assert ct[0] is c

    def test_init_tuple(self):
        ct = ConversionTable([("pants", convVal, convItem),
                              ("shirt", convVal, convItem, True)])

        assert ct[0].key == 'pants'
        assert ct[0].convertValue is convVal
        assert ct[0].convertItem is convItem
        assert not ct[0].required

        assert ct[1].key == 'shirt'
        assert ct[1].convertValue is convVal
        assert ct[1].convertItem is convItem
        assert ct[1].required

    def test_init_dict(self):
        d = dict(key='pants', convertValue=convVal, convertItem=convItem)

        ct = ConversionTable([d])

        assert ct[0].key == 'pants'
        assert ct[0].convertValue is convVal
        assert ct[0].convertItem is convItem
        assert not ct[0].required

    def test_init_bad(self):
        with self.assertRaises(ValueError):
            ct = ConversionTable(['oops'])

    def test_copy(self):
        ct = ConversionTable([("pants", convVal, convItem),
                              ("shirt", convVal, convItem, True)])

        ct2 = ct.copy()

        assert ct is not ct2
        assert ct[0] is not ct2[0]
        assert ct[1] is not ct2[1]

        assert ct[0].key == ct2[0].key
        assert ct[0].convertValue is ct2[0].convertValue
        assert ct[0].convertItem is ct2[0].convertItem
        assert ct[0].required == ct2[0].required

    def test_duplicate(self):
        c1 = Converter("pants", convVal, convItem)
        c2 = Converter("pants", convVal, convItem)
        c3 = Converter("shirt", convVal, convItem)

        ct = ConversionTable([c1, c2, c3])

        assert ct.get('pants') is c1
        l = ct.getAll('pants')
        assert l[0] is c1
        assert l[1] is c2

        ct.delete('pants')
        l = ct.getAll('pants')
        assert not l
        assert len(ct) == 1
        assert ct[0] is c3

    def test_get(self):
        c = Converter("pants", convVal, convItem)
        
        ct = ConversionTable([c,
                              ("shirt", convVal, convItem, True)])

        assert ct.get("belt") is None
        assert ct.get("pants") is c


    def test_getAll_no_match(self):
        ct = ConversionTable([("pants", convVal, convItem),
                              ("shirt", convVal, convItem, True)])

        l = ct.getAll("belt")
        assert isinstance(l, list)
        assert not l

    def test_convert(self):
        ct = ConversionTable([
            ("joe", "I wear {0}".format, convItem),
            ("frank", "You wear {0}".format, convItem)])
        
        ct.genericValue = "Someone wears {0}".format
        
        d = ct.convert({'joe':'pants', 'frank':'shirt', 'bob':'shoes'})
        assert d == {'joe': "I wear pants", 'frank': "You wear shirt", 'bob': "Someone wears shoes"}

    def test_drop(self):
        ct = ConversionTable([
            ("joe", "I wear {0}".format, convItem),
            ("frank", "You wear {0}".format, lambda k, v: None)])
        
        ct.genericItem = lambda k, v: None
        
        d = ct.convert({'joe':'pants', 'frank':'shirt', 'bob':'shoes'})
        assert d == {'joe': "I wear pants"}


    def test_generic(self):
        c = Converter("pants", convVal, convItem)
        ct = ConversionTable([c])
        assert ct.convert({'shirt':42}) == {'shirt':42}

    def test_missing(self):
        c = Converter("pants", convVal, convItem, True)
        ct = ConversionTable([c])
        with self.assertRaises(ValueError):
            ct.convert({'shirt':42}) == {'shirt':42}
