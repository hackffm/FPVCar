import json

import helper_test

from components import Sound

from resources import *

config = Config(debug=True)
helper = Helper()

components = {
    "sound": Sound(config, helper, debug=True),
}

m = {'component': 'sound', 'play': 'chicken.wav'}
component = components[m["component"]]
result = component.handleMessage(m)
print(result)

m = {'component': 'sound', 'play': 'nono.wav'}
component = components[m["component"]]
result = component.handleMessage(m)
print(result)

m = {'component': 'sound', 'get': 'some'}
component = components[m["component"]]
result = component.handleMessage(m)
print(result)

m = {'component': 'sound', 'get': 'all'}
component = components[m["component"]]
result = component.handleMessage(m)
print(result)