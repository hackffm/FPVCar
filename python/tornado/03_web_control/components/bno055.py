import board
import busio
import adafruit_bno055

from . import Component

i2c = busio.I2C(board.SCL, board.SDA)
bno = adafruit_bno055.BNO055(i2c)


class Bno055(Component):

    def __init__(self, debug=False):
        name = 'bno'
        super(Bno055, self).__init__(name)
        self.debug = debug
        self.bnos = {"acceleration": self.acceleration(),
                     "calibration_status": self.calibration_status(),
                     "euler": self.euler(),
                     "gravity": self.gravity(),
                     "gyro": self.gyro(),
                     "heading": self.heading(),
                     "linear_acceleration": self.acceleration_linear(),
                     "magnetic": self.magnetic(),
                     "quaternion": self.quaternion(),
                     "temperature": self.temperature()}

    def handleMessage(self, message):
        result = {}

        if self.debug:
            pass
            #print(self.name + ' recieved ' + str(message))

        if "bno" in message:
            m = message['bno']
            if m in self.bnos:
                result[m] = self.bnos[m]
            elif m == 'all':
                for s in self.bnos:
                    result[s] = self.bnos[s]
            else:
                result = {'bno': 'failed'}

        return result

# -- bnos----------------------------------

    def acceleration(self):
        return bno.acceleration

    def acceleration_linear(self):
        return bno.linear_acceleration

    def calibration_status(self):
        return bno.calibration_status

    def euler(self):
        return bno.euler

    def gravity(self):
        return bno.gravity

    def gyro(self):
        return bno.gyro

    def heading(self):
       heading, roll, pitch = self.euler()
       return heading

    def magnetic(self):
        return bno.magnetic

    def quaternion(self):
        return bno.quaternion

    def temperature(self):
        return bno.temperature
