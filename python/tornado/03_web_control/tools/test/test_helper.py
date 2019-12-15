import helper_test

from resources import *

helper = Helper()


def test_shutdown():
    while True:
        helper.shutdown(1)
