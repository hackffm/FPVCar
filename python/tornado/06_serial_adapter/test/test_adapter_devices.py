import helper_test

from components import *
from resources import *


# resources
config = Config()
cfg = config.cfg()


# --Labyrinth------------------------------------------------------------------------------

def test_config():
    if cfg.debug:
        print('debug is on')


def test_adapters_add():
    count = 0
    for adapter in cfg.adapters:
        count += 1
        print('add adapter {} to controller as {}'.format(str(count), str(adapter['name'])))
        ac.adapters_add(AdapterDevices(adapter['name'], adapter['devices'], test_debug))


ac = AdapterController()


# -------------------------------------------------------------------------------------


def test_adapter_in_list():
    assert ac.adapter_exists('A1') == True, 'failed finding Test Adapter'
    assert ac.adapter_exists('A4') == False, 'failed checking non existing adapter'


def test_device_in_adapters_list():
    assert ac.device_exists('r1d1') == True, 'Failed finding Device'
    assert ac.device_exists('r1d2') == True, 'Failed finding Device'
    assert ac.device_exists('r1d3') == True, 'Failed finding Device'
    assert ac.device_exists('r2d1') == True, 'Failed finding Device'
    assert ac.device_exists('r2d2') == True, 'Failed finding Device'
    assert ac.device_exists('r4d1') == False, 'failed checking non existing Device'


def test_talk_to_device():
    ac.device_write('r1d1', 'Hello World')


test_debug = True

test_config()
test_adapters_add()
test_adapter_in_list()
test_device_in_adapters_list()
test_talk_to_device()


print('test test_adapter_devices finished')
