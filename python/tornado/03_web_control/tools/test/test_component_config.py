import json

import helper_test

from components import ComponentConfig
from resources import *

config = Config(debug=True)

debug = True
components = {
    "config": ComponentConfig(config, debug=debug)
}

m = {'component': 'config', 'load': 'config'}

component = components[m["component"]]
result = component.handleMessage(m)
print(result)

config.configuration['test'] = 'test'
m = {'component': 'config', 'save': config.configuration}
result = component.handleMessage(m)
print(result)

