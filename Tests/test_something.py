from pytestqt.qt_compat import qt_api

def do_something():
    qt_api.qWarning("this is a WARNING message")

def test_foo():
    do_something()
    assert 1
