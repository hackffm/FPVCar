import board
import busio
import time

import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

while True:
    print('Temperature: {} degrees C'.format(sensor.temperature))
    print('Accelerometer (m/s^2): {}'.format(sensor.acceleration))
    print('Magnetometer (microteslas): {}'.format(sensor.magnetic))
    print('Gyroscope (rad/sec): {}'.format(sensor.gyro))
    print('Euler heading, roll, pitch angle: {}'.format(sensor.euler))
    print('Quaternion x, y, z, w: {}'.format(sensor.quaternion))
    print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
    print('Gravity (m/s^2): {}'.format(sensor.gravity))
    print('Calibration status sys, gyro, accel, mag: {}'.format(sensor.calibration_status))
    print()

    time.sleep(1)
