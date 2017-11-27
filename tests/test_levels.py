import pytest

from twiggy import levels


def test_display():
    assert str(levels.DEBUG) == 'DEBUG'
    assert repr(levels.DEBUG) == '<LogLevel DEBUG>'


def test_name2level():
    assert levels.name2level('debug') is levels.DEBUG
    assert levels.name2level('Debug') is levels.DEBUG


def test_less_than():
    assert levels.DEBUG < levels.INFO
    assert levels.INFO < levels.NOTICE
    assert levels.NOTICE < levels.WARNING
    assert levels.WARNING < levels.ERROR
    assert levels.ERROR < levels.CRITICAL
    assert levels.CRITICAL < levels.DISABLED


def test_less_than_equals():
    assert levels.DEBUG <= levels.INFO
    assert levels.INFO <= levels.NOTICE
    assert levels.NOTICE <= levels.WARNING
    assert levels.WARNING <= levels.ERROR
    assert levels.ERROR <= levels.CRITICAL
    assert levels.CRITICAL <= levels.DISABLED


def test_greater_than():
    assert levels.INFO > levels.DEBUG
    assert levels.NOTICE > levels.INFO
    assert levels.WARNING > levels.NOTICE
    assert levels.ERROR > levels.WARNING
    assert levels.CRITICAL > levels.ERROR
    assert levels.DISABLED > levels.CRITICAL


def test_greater_than_equals():
    assert levels.INFO >= levels.DEBUG
    assert levels.NOTICE >= levels.INFO
    assert levels.WARNING >= levels.NOTICE
    assert levels.ERROR >= levels.WARNING
    assert levels.CRITICAL >= levels.ERROR
    assert levels.DISABLED >= levels.CRITICAL


def test_equality():
    assert levels.DEBUG == levels.DEBUG
    assert levels.INFO == levels.INFO
    assert levels.NOTICE == levels.NOTICE
    assert levels.WARNING == levels.WARNING
    assert levels.ERROR == levels.ERROR
    assert levels.CRITICAL == levels.CRITICAL


def test_inequality():
    assert not levels.DEBUG != levels.DEBUG
    assert not levels.INFO != levels.INFO
    assert not levels.NOTICE != levels.NOTICE
    assert not levels.WARNING != levels.WARNING
    assert not levels.ERROR != levels.ERROR
    assert not levels.CRITICAL != levels.CRITICAL

    assert levels.INFO != levels.DEBUG
    assert levels.NOTICE != levels.WARNING
    assert levels.WARNING != levels.NOTICE
    assert levels.ERROR != levels.WARNING
    assert levels.CRITICAL != levels.ERROR
    assert levels.DISABLED != levels.CRITICAL


def test_dict_key():
    d = {levels.DEBUG: 42}
    assert d[levels.DEBUG] == 42


def test_bogus_equals():
    assert not levels.DEBUG == 1


def test_bogus_not_equals():
    assert levels.DEBUG != 1


def test_bogus_less_than():
    with pytest.raises(TypeError):
        levels.DEBUG < 42


def test_bogus_less_than_equals():
    with pytest.raises(TypeError):
        levels.DEBUG <= 42


def test_bogus_greater_than():
    with pytest.raises(TypeError):
        levels.DEBUG > 42


def test_bogus_greater_than_equals():
    with pytest.raises(TypeError):
        levels.DEBUG >= 42
