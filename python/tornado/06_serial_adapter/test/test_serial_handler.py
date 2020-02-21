import helper_test

from components import *
from resources import *


# resources
config = Config('test')
helper_test.file_delete(config.path_config)
config.load()
cfg = config.cfg()

name = 'test_serial_handler'

# --Labyrinth------------------------------------------------------------------------------
sh = SerialHandler()


def test_config():
    print('>test_config')
    if cfg.debug:
        print('debug is on')


def test_things_serial_add():
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

def test_thingies_not_empty():
    print('>test_thingy_not_empty')
    _thingies = sh.thingies()
    assert len(_thingies) > 0, 'Failed counting thingies'
    for t in _thingies:
        print(t)

def test_talk_to_thingy():
    print('>test_talk_to_thingy')
    sh.thingy_write('r1d1', 'Hello World')


test_debug = True

test_config()
test_things_serial_add()
test_things_exist()
test_thingy_exists()
test_thingies_not_empty()
#test_talk_to_device()


print(name + ' finished')
