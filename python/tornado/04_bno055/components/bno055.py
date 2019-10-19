import board
import busio
import adafruit_bno055

from component import Component

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)


class Bno055(Component):

    def handleMessage(self, message):
        result = ''

        if "acceleration" in message:
            result = self.acceleration()
        elif "linear_acceleration" in message:
            result = self.acceleration_linear()
        elif "euler" in message:
            result = self.euler()
        elif "gravity" in message:
            result = self.gravity()
        elif "gyro" in message:
            result = self.gyro()
        elif "magnetic" in message:
            result = self.magnetic()
        elif "quternation" in message:
            result = self.quternation()
        elif "temperature" in message:
            result = self.temperature()
        else:
            result = self.failed

        return result

    def acceleration(self):
        return sensor.acceleration

    def acceleration_linear(self):
        return sensor.linear_acceleration

    def euler(self):
        return sensor.euler

    def gravity(self):
        return sensor.gravity

    def gyro(self):
        return sensor.gyro

    def magnetic(self):
        return sensor.magnetic

    def quternation(self):
        return sensor.quaternion

    def temperature(self):
        return sensor.temperature