import helper_test

from bno055 import Bno055

sensor = Bno055()

print(sensor.handleMessage('acceleration'))
print(sensor.handleMessage('temperature'))
assert sensor.handleMessage('nono') == 'failed', 'Failed handling unknown Sensor request'
