import helper_test

from components import *

sensor = Bno055()

print('quaternion:' + str(sensor.handleMessage({'sensor': 'quaternion'})))
print('temperature:' + str(sensor.handleMessage({'sensor': 'temperature'})))
print(sensor.handleMessage({'sensor': 'all'}))
assert sensor.handleMessage({'sensor': 'nono'}) == {'sensor': 'failed'}, 'Failed handling unknown Sensor request'
