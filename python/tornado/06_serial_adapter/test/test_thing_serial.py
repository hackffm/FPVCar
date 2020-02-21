import helper_test

from things import *

id = 'test'
ser = None
debug = True
id_thingy = 'door123'

ts = ThingSerial(id, ser, debug)
ts.thingy_add(id_thingy)


def test_thingy_exists():
    print('>test_thingy_exists')
    assert ts.thingy_exists(id_thingy) == True, 'Failed finding thingy'
    assert ts.thingy_exists('nono1') == False, 'failed checking non existing thingy'

def test_thingy_not_empty():
    print('>test_thingy_not_empty')
    _thingies = ts.thingies
    assert len(_thingies) > 0, 'Failed counting thingies'
    for t in _thingies:
        print(t.id)

test_thingy_exists()
test_thingy_not_empty()
