import unittest2
from twiggy.lib import Converter, ConversionTable

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
        