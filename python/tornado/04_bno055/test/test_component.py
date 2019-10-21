import helper_test

from components import *

sensor = Bno055()

print(sensor.handleMessage({'sensor': 'acceleration'}))
print(sensor.handleMessage({'sensor': 'temperature'}))
print(sensor.handleMessage({'sensor': 'all'}))
assert sensor.handleMessage({'sensor': 'nono'}) == 'failed', 'Failed handling unknown Sensor request'
