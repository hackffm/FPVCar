import json

import helper_test

from components import Base
from resources import *

class SerialDummy():
    def send(self, text):
        print('Serial out:' + str(text))

ser = SerialDummy()

debug = True
components = {
    "base": Base(ser, debug=True),
}

m = { "component": "base", "forward": 10 }
component = components[m["component"]]
result = component.handleMessage(m)
print('component base forward 10 caused result:' + str(result))

m = { "component": "base", "right": 10 }
component = components[m["component"]]
result = component.handleMessage(m)
print('component base forward 10 caused result:' + str(result))
