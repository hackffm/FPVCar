import helper_test

components = {}
from components.bno055 import Bno055
components["sensor_bno"] = Bno055(debug=True)

sensor = Bno055()

print('quaternion:' + str(sensor.handleMessage({'bno': 'quaternion'})))
print('temperature:' + str(sensor.handleMessage({'bno': 'temperature'})))
assert sensor.handleMessage({'bno': 'nono'}) == {'bno': 'failed'}, 'Failed handling unknown Sensor request'
sensor_bno_data = sensor.handleMessage({'bno': 'all'})
print(sensor_bno_data)
