import helper_test

from components import *
from resources import *


# resources
config = Config()
config.path_config = config.home + '/' + config.name + '/test.json'
helper_test.file_delete(config.path_config)
config.load()
cfg = config.cfg()


# --Labyrinth------------------------------------------------------------------------------
sh = SerialHandler()


def test_config():
    print('>test_config')
    if cfg.debug:
        print('debug is on')


def test_things_add():
    print('>test_things_add')
    for ts in cfg.things_serial:
        print('add things_serial {} with port {}'.format(str(ts['ID']), str(ts['port'])))
        sh.things_serial_add(ts['ID'], ts['port'], test_debug)
    print('add thingies')
    for ts in cfg.things_serial:
        for t in ts['thingies']:
            print('thing {} thingy_add {}'.format(str(ts['ID']), str(t['ID'])))
            sh.thingy_add(ts['ID'], t['ID'])
# -------------------------------------------------------------------------------------


def test_things_exist():
    print('>test_things_exist')
    assert sh.things_serial_exists('A1') == True, 'failed finding Test Adapter'
    assert sh.things_serial_exists('A4') == False, 'failed checking non existing adapter'


def test_thingy_exists():
    print('>test_thingy_exists')
    assert sh.thingy_exists('D1') == True, 'Failed finding thingy'
    assert sh.thingy_exists('D2') == True, 'Failed finding thingy'
    assert sh.thingy_exists('D3') == True, 'Failed finding thingy'
    assert sh.thingy_exists('L1') == True, 'Failed finding thingy'
    assert sh.thingy_exists('n1') == False, 'failed checking non existing thingy'


def test_talk_to_thingy():
    print('>test_talk_to_thingy')
    sh.thingy_write('r1d1', 'Hello World')


test_debug = True

test_config()
test_things_add()
test_things_exist()
test_thingy_exists()
#test_talk_to_device()


print('test test_adapter_devices finished')
