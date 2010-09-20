import unittest2

from twiggy import Emitter, Message

from . import make_mesg

m = make_mesg()

class msgFilterTestCase(unittest2.TestCase):

    def test_None(self):
        f = Emitter.msgFilter(None)
        assert callable(f)
        assert f(m)

    def test_bool(self):
        f = Emitter.msgFilter(True)
        assert callable(f)
        assert f(m)

        f = Emitter.msgFilter(False)
        assert callable(f)
        assert not f(m)

    def test_basestring(self):
        f = Emitter.msgFilter("^Hello.*$")
        assert callable(f)
        assert f(m)

        f = Emitter.msgFilter("^Goodbye.*$")
        assert callable(f)
        assert not f(m)

    def test_callable(self):
        my_func = lambda mesg: True
        f = Emitter.msgFilter(my_func)
        assert f is my_func

    def test_bad_arg(self):
        with self.assertRaises(ValueError):
            f = Emitter.msgFilter(42)


class namesTestCase(unittest2.TestCase):

    def test_names(self):
        n = Emitter.names("foo", "bar")
        assert n.names == ("foo", "bar")

        assert Emitter.names("jose", "frank")(m)
        assert not Emitter.names("bob", "frank")(m)

    def test_glob_names(self):
        n = Emitter.glob_names("foo", "bar")
        assert n.names == ("foo", "bar")

        assert Emitter.glob_names("jo*", "frank")(m)
        assert not Emitter.glob_names("*bob", "frank")(m)
