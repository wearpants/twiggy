import datetime
import decimal
import json
import re
import unittest

from twiggy.lib.json import TwiggyJSONEncoder

class TwiggyJSONEncoderTests(unittest.TestCase):
    def test_timedelta(self):
        duration = datetime.timedelta(days=1, hours=2, seconds=3)
        self.assertEqual(
            json.dumps({'duration': duration}, cls=TwiggyJSONEncoder),
            '{"duration": "P1DT02H00M03S"}'
        )
        duration = datetime.timedelta(0)
        self.assertEqual(
            json.dumps({'duration': duration}, cls=TwiggyJSONEncoder),
            '{"duration": "P0DT00H00M00S"}'
        )

