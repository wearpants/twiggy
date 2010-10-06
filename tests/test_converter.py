import unittest2
import doctest

from twiggy.lib.converter import Converter, ConversionTable
import twiggy.lib.converter as twiggy_lib_converter

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(twiggy_lib_converter))
    return tests

def convVal(x):
    return x

def convItem(x, y):
    return x, y

class ConversionTableTestCase(unittest2.TestCase):

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

    def test_get(self):
        c1 = Converter("pants", convVal, convItem)
        c2 = Converter("pants", convVal, convItem)

        ct = ConversionTable([c1, c2])

        assert ct.get('pants') is c1
        l = ct.getAll('pants')
        assert l[0] is c1
        assert l[1] is c2
