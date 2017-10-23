import sys
import re

from twiggy import filters, levels

from . import make_mesg

if sys.version_info >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise RuntimeError("unittest2 is required for Python < 2.7")


m = make_mesg()


class MsgFilterTestCase(unittest.TestCase):
    # XXX more robust testing of the exact type/func.__name__ of the returned f
    # might be nice (instead of just callable), but eh.

    def test_None(self):
        f = filters.msg_filter(None)
        assert callable(f)
        assert f(m)

    def test_bool(self):
        f = filters.msg_filter(True)
        assert callable(f)
        assert f(m)

        f = filters.msg_filter(False)
        assert callable(f)
        assert not f(m)

    def test_basestring(self):
        f = filters.msg_filter("^Hello.*$")
        assert callable(f)
        assert f(m)

        f = filters.msg_filter("^Goodbye.*$")
        assert callable(f)
        assert not f(m)

    def test_regex(self):
        f = filters.msg_filter(re.compile("^Hello.*$"))
        assert callable(f)
        assert f(m)

        f = filters.msg_filter(re.compile("^Goodbye.*$"))
        assert callable(f)
        assert not f(m)

    @staticmethod
    def _always_true(mesg):
        return True

    def test_callable(self):
        f = filters.msg_filter(self._always_true)
        assert f is self._always_true

    def test_bad_arg(self):
        with self.assertRaises(ValueError):
            filters.msg_filter(42)

    def test_list(self):
        re1 = "^Hello.*$"
        re2 = "^.*Funnypants$"
        filter_list = [re1, re2]
        f = filters.msg_filter(filter_list)
        assert callable(f)
        assert f(m)

        re3 = "^.*Sillyhead$"
        filter_tuple = (re1, re3)
        f = filters.msg_filter(filter_tuple)
        assert callable(f)
        assert not f(m)

    def test_nested_list(self):
        # not encouraged as it's equivalent, but let's support it anyway
        re1 = "^Hello.*$"
        re2 = "^.*Funnypants$"
        filter_list = [re1, [re2]]
        f = filters.msg_filter(filter_list)
        assert callable(f)
        assert f(m)

    def test_single_list(self):
        re1 = "^Hello.*$"
        filter_list = [re1]
        f = filters.msg_filter(filter_list)
        assert callable(f)
        assert f(m)


class namesTestCase(unittest.TestCase):

    def test_names(self):
        n = filters.names("foo", "bar")
        assert n.names == ("foo", "bar")

        assert filters.names("jose", "frank")(m)
        assert not filters.names("bob", "frank")(m)

    def test_glob_names(self):
        n = filters.glob_names("foo", "bar")
        assert n.names == ("foo", "bar")

        assert filters.glob_names("jo*", "frank")(m)
        assert not filters.glob_names("*bob", "frank")(m)


class EmitterTestCase(unittest.TestCase):

    def test_bad_min_level(self):
        with self.assertRaises(ValueError):
            filters.Emitter(42, None, None)

    def test_filter_property(self):
        # XXX we really should mock & test that msg_filter is being called. eh.

        e = filters.Emitter(levels.INFO, "^Hello.*$", 'output-unused')

        f = e.filter
        assert callable(f)
        assert f(m)

        e.filter = "^Goodbye.*$"
        f = e.filter
        assert callable(f)
        assert not f(m)
