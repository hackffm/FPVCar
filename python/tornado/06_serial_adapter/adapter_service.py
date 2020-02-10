from components import *
from resources import *


# resources
ac = AdapterController()
config = Config()
#
cfg = config.cfg()
debug = cfg.debug


count = 0
for adapter in cfg.adapters:
    count += 1
    if debug:
        print('add adapter {} to controller as {}'.format(str(count), str(adapter['name'])))
    ac.adapters_add(AdapterDevices(adapter['name'], adapter['devices'], debug))

