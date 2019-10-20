import helper_test

from components import *

sensor = Bno055()

print(sensor.handleMessage('acceleration'))
print(sensor.handleMessage('temperature'))
print(sensor.handleMessage('all'))
assert sensor.handleMessage('nono') == 'failed', 'Failed handling unknown Sensor request'
