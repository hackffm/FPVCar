import board
import busio
import adafruit_bno055

from . import Component

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)


class Bno055(Component):
    """handle adafruit bno055 sensor"""

    def __init__(self, debug=False):
        super().__init__('bno055')
        self.debug = debug
        self.sensors = {"acceleration": self.acceleration(),
                        "calibration_status": self.calibration_status(),
                        "linear_acceleration": self.acceleration_linear(),
                        "euler": self.euler(),
                        "gravity": self.gravity(),
                        "gyro": self.gyro(),
                        "magnetic": self.magnetic(),
                        "quaternion": self.quaternion(),
                        "temperature": self.temperature()}

    def handleMessage(self, message):
        result = {}
        if "sensor" in message:
            m = message['sensor']
            if self.debug:
                print('message to bno055 is ' + str(m))
            if m in self.sensors:
                result[m] = self.handle_sensors(m)
            elif m == 'all':
                for s in self.sensors:
                    result[s] = self.sensors[s]
            else:
                result['sensor'] = self.failed
        return result

    def handle_sensors(self, _message):
        result = self.failed
        if "acceleration" == _message:
            result = self.acceleration()
        elif "calibration_status" == _message:
            result = self.calibration_status()
        elif "linear_acceleration" == _message:
            result = self.acceleration_linear()
        elif "euler" == _message:
            result = self.euler()
        elif "gravity" == _message:
            result = self.gravity()
        elif "gyro" == _message:
            result = self.gyro()
        elif "magnetic" == _message:
            result = self.magnetic()
        elif "quaternion" == _message:
            result = self.quaternion()
        elif "temperature" == _message:
            result = self.temperature()
        return result

# -- sensors----------------------------------

    def acceleration(self):
        return sensor.acceleration

    def acceleration_linear(self):
        return sensor.linear_acceleration

    def calibration_status(self):
        return sensor.calibration_status

    def euler(self):
        return sensor.euler

    def gravity(self):
        return sensor.gravity

    def gyro(self):
        return sensor.gyro

    def magnetic(self):
        return sensor.magnetic

    def quaternion(self):
        return sensor.quaternion

    def temperature(self):
        return sensor.temperature