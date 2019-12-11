import json

import helper_test

from components import ComponentConfig
from resources import *

config = Config(debug=True)

debug = True
components = {
    "config": ComponentConfig(config, debug=debug)
}

m = {'component': 'config', 'load': 'configuration'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component load configuration\n' + str(result))

m = {'component': 'config', 'load': 'baud'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component load baud\n' + str(result))

m = {'component': 'config', 'get': 'camera'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component get camera\n' + str(result))


config.configuration['test'] = 'test'
m = {'component': 'config', 'save': config.configuration}
result = component.handleMessage(m)
print('component save\n' + str(result))

