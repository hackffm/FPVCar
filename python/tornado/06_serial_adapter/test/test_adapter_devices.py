import helper_test

import os

from components import *

ad = AdapterDevices('A1')


def test_who():
    print(ad.handleMessage('?'))


def test_devices_connected():
    print(ad.devices_list())


test_who()
test_devices_connected()