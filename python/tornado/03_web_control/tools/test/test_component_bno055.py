import helper_test

components = {}

from components.bno055 import Bno055
components["sensor_bno"] = Bno055(debug=True)

component = components["sensor_bno"]

print('quaternion:' + str(component.handleMessage({'bno055': 'quaternion'})))
print('temperature:' + str(component.handleMessage({'bno055': 'temperature'})))
print('euler:' + str(component.handleMessage({'bno055': 'euler'})))

assert component.handleMessage({'bno055': 'nono'}) == {'bno055': 'failed'}, 'Failed handling unknown Sensor request'

sensor_bno_data = component.handleMessage({'bno055': 'all'})
print(sensor_bno_data)
print(sensor_bno_data['euler'])
