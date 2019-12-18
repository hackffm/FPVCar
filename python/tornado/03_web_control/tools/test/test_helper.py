import helper_test

import os

from resources import *

helper = Helper()


def test_shutdown():
    while True:
        helper.shutdown(1)

def test_file_delete():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(helper.file_delete(current_dir + '/test.txt'))

test_file_delete()