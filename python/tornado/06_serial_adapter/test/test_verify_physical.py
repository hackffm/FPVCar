import helper_test

from components import *
from resources import *
from things import *

# resources
config = Config('labyrinth')
config.load()
cfg = config.cfg()
sh = SerialHandler(cfg.things_serial, debug=True)


def test_things_verify():
    print('>test_things_verify')
    sh.things_serial_verify()
    for thing in sh.things_serial:
        print('thing {} verification is {}'.format(str(thing.id), str(thing.verified)))


test_things_verify()
