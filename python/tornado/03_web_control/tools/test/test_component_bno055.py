import helper_test

from components import *

sensor = Bno055()

print('quaternion:' + str(sensor.handleMessage({'sensor': 'quaternion'})))
print('temperature:' + str(sensor.handleMessage({'sensor': 'temperature'})))
assert sensor.handleMessage({'sensor': 'nono'}) == {'sensor': 'failed'}, 'Failed handling unknown Sensor request'
sensor_bno_data = sensor.handleMessage({'sensor': 'all'})
print(sensor_bno_data)
