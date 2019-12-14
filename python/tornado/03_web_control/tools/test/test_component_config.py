import json

import helper_test

from components import ComponentConfig
from resources import *

config = Config(debug=True)

debug = True
components = {
    "config": ComponentConfig(config, debug=debug)
}


def valid_jasonparse(text):
    text = text.replace('\'','\\"')
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    return text


m = {'component': 'config', 'load': 'configuration'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component load configuration result is' + str(result))
print(valid_jasonparse(str(result)))

m = {'component': 'config', 'load': 'baud'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component load baud result is' + str(result))

m = {'component': 'config', 'get': 'camera'}
component = components[m["component"]]
result = component.handleMessage(m)
print('component get camera result is' + str(result))

config.configuration['test'] = 'test'
m = {'component': 'config', 'save': config.configuration}
result = component.handleMessage(m)
print('component save result is ' + str(result))

_set = {'debug' : True}
m = {'component': 'config', 'set': _set}
result = component.handleMessage(m)
print('component set debug result is ' + str (result))

print(valid_jasonparse(str(result)))

_set = {'port' : 8080}
m = {'component': 'config', 'set': _set}
result = component.handleMessage(m)
print('component set port result is ' + str (result))

_set = {'sensors' : {'bno055': True}}
m = {'component': 'config', 'set': _set}
result = component.handleMessage(m)
print('component set bno055 result is ' + str (result))

