import helper_test

from components import *
from resources import *
from things import *

from time import sleep

# resources
config = Config('test')
helper_test.file_delete(config.path_config)
config.load()
cfg = config.cfg()

name = 'test_serial_handler'

# --Labyrinth------------------------------------------------------------------------------
sh = SerialHandler(things_serial=False, debug=True)


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


def test_thing_id_valid():
    print('>test_thing_id_valid')
    assert sh.things_serial_id_valid('A1') == True, 'failed finding Test Adapter'
    assert sh.things_serial_id_valid('A4') == False, 'failed checking non existing adapter'


def test_thingy_id_valid():
    print('>test_thingy_id_valid')
    assert sh.thingy_id_valid('D1') == True, 'Failed finding thingy'
    assert sh.thingy_id_valid('D2') == True, 'Failed finding thingy'
    assert sh.thingy_id_valid('D3') == True, 'Failed finding thingy'
    assert sh.thingy_id_valid('L1') == True, 'Failed finding thingy'
    assert sh.thingy_id_valid('n1') == False, 'failed checking non existing thingy'


def test_thingies_not_empty():
    print('>test_thingies_not_empty')
    _thingies = sh.thingies()
    assert len(_thingies) > 0, 'Failed counting thingies'
    for t in _thingies:
        print(t)


def test_talk_to_thingy():
    print('>test_talk_to_thingy')
    sh.things_serial_verify()
    sh.thingy_write('D3', 'Hello World')
    sleep(1.0)
    result = sh.thingy_read('D3')
    print('result ' + str(result))
    result = sh.thingy_read('D4')
    print('result ' + str(result))
    sh.thingy_write('D4', 'Hello World')
    sleep(1.0)
    result = sh.thingy_read('D4')
    print('result ' + str(result))


test_debug = True

test_config()
test_things_serial_add()
test_thing_id_valid()
test_thingy_id_valid()
test_thingies_not_empty()
test_talk_to_thingy()

print('\n\n' + name + ' finished')
