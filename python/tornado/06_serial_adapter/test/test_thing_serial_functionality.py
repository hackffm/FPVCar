import helper_test

from things import *

import serial

from time import sleep


id = 'test'
debug = True
id_thingy = 'door123'

# update serial port and make sure thing is attached before test !!!!
ser = serial.Serial('/dev/ttyACM0', 38400)
ts = ThingSerial(id, ser, debug)


def test_thing_id_direct(serial_thing):
    print('>test_thing_id_direct')

    serial_thing.write('?')
    sleep(1.0)
    name = serial_thing.read()
    print('found ' + name)


def test_thing_id_update(serial_thing):
    print('>test_thing_id_update')

    print('currently id is ' + str(serial_thing.id))
    serial_thing.verify()
    print('id is now ' + str(serial_thing.id))
    print('thing serial verification is ' + str(serial_thing.verified))


def test_thingy_active(serial_thing):
    print('>test_thingy_active')
    for t in serial_thing.thingies:
        if serial_thing.verified:
            print(t.id + ' is active')
        else:
            print(t.id + ' is not active')


def test_thingy_write(serial_thing, thingy_id, command):
    print('>test_thingy_write')
    serial_thing.write(thingy_id + command)
    sleep(1.0)
    result = serial_thing.read()
    print(result)


test_thing_id_direct(ts)
test_thing_id_update(ts)
test_thing_id_direct(ts)
ts.thingy_add(id_thingy)
test_thingy_active(ts)
test_thingy_write(ts, id_thingy, 'Hello World')
