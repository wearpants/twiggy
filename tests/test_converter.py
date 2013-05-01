import sys
if sys.version_info >= (2, 7):
    import unittest
else:
    try: 
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")
        
from twiggy.lib.converter import Converter, ConversionTable, same_item, same_value, drop

def conv_val(x):
    return x

def conv_item(x, y):
    return x, y

class HelperTestCase(unittest.TestCase):

    def test_drop(self):
        assert drop(1, 2) is None

    def test_same_value(self):
        o = object()
        assert same_value(o) is o

    def test_same_item(self):
        o1 = object()
        o2 = object()
        
        x1, x2 = same_item(o1, o2) 
        assert o1 is x1
        assert o2 is x2

class ConverterTestCase(unittest.TestCase):

    def test_repr(self):
        c = Converter("pants", conv_val, conv_item)
        assert repr(c) == "<Converter('pants')>"

class ConversionTableTestCase(unittest.TestCase):

    def test_init_None(self):
        ct = ConversionTable()
        assert len(ct) == 0

    def test_init_simple(self):
        c = Converter("pants", conv_val, conv_item)
        ct = ConversionTable([c])
        assert ct[0] is c

    def test_init_tuple(self):
        ct = ConversionTable([("pants", conv_val, conv_item),
                              ("shirt", conv_val, conv_item, True)])

        assert ct[0].key == 'pants'
        assert ct[0].convert_value is conv_val
        assert ct[0].convert_item is conv_item
        assert not ct[0].required

        assert ct[1].key == 'shirt'
        assert ct[1].convert_value is conv_val
        assert ct[1].convert_item is conv_item
        assert ct[1].required

    def test_init_dict(self):
        d = dict(key='pants', convert_value=conv_val, convert_item=conv_item)

        ct = ConversionTable([d])

        assert ct[0].key == 'pants'
        assert ct[0].convert_value is conv_val
        assert ct[0].convert_item is conv_item
        assert not ct[0].required

    def test_init_bad(self):
        with self.assertRaises(ValueError):
            ct = ConversionTable(['oops'])

    def test_copy(self):
        ct = ConversionTable([("pants", conv_val, conv_item),
                              ("shirt", conv_val, conv_item, True)])

        ct2 = ct.copy()

        assert ct is not ct2
        assert ct[0] is not ct2[0]
        assert ct[1] is not ct2[1]

        assert ct[0].key == ct2[0].key
        assert ct[0].convert_value is ct2[0].convert_value
        assert ct[0].convert_item is ct2[0].convert_item
        assert ct[0].required == ct2[0].required

    def test_duplicate(self):
        c1 = Converter("pants", conv_val, conv_item)
        c2 = Converter("pants", conv_val, conv_item)
        c3 = Converter("shirt", conv_val, conv_item)

        ct = ConversionTable([c1, c2, c3])

        assert ct.get('pants') is c1
        l = ct.get_all('pants')
        assert l[0] is c1
        assert l[1] is c2

        ct.delete('pants')
        l = ct.get_all('pants')
        assert not l
        assert len(ct) == 1
        assert ct[0] is c3

    def test_get(self):
        c = Converter("pants", conv_val, conv_item)
        
        ct = ConversionTable([c,
                              ("shirt", conv_val, conv_item, True)])

        assert ct.get("belt") is None
        assert ct.get("pants") is c


    def test_get_all_no_match(self):
        ct = ConversionTable([("pants", conv_val, conv_item),
                              ("shirt", conv_val, conv_item, True)])

        l = ct.get_all("belt")
        assert isinstance(l, list)
        assert not l

    def test_convert(self):
        ct = ConversionTable([
            ("joe", "I wear {0}".format, conv_item),
            ("frank", "You wear {0}".format, conv_item)])
        
        ct.generic_value = "Someone wears {0}".format
        
        d = ct.convert({'joe':'pants', 'frank':'shirt', 'bob':'shoes'})
        self.assertDictEqual(d, {'joe': "I wear pants", 'frank': "You wear shirt", 'bob': "Someone wears shoes"})

    def test_drop(self):
        ct = ConversionTable([
            ("joe", "I wear {0}".format, conv_item),
            ("frank", "You wear {0}".format, lambda k, v: None)])
        
        ct.generic_item = drop
        
        d = ct.convert({'joe':'pants', 'frank':'shirt', 'bob':'shoes'})
        assert d == {'joe': "I wear pants"}


    def test_generic(self):
        c = Converter("pants", conv_val, conv_item)
        ct = ConversionTable([c])
        assert ct.convert({'shirt':42}) == {'shirt':42}

    def test_missing(self):
        c = Converter("pants", conv_val, conv_item, True)
        ct = ConversionTable([c])
        with self.assertRaises(ValueError):
            ct.convert({'shirt':42}) == {'shirt':42}
