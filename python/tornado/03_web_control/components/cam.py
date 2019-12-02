from . import Component
import os
import subprocess
import signal
from subprocess import check_output


class Cam(Component):

    def __init__(self, ser, debug=False):
        name = 'cam'
        super(Cam, self).__init__(name)
        self.debug = debug
        self.name = name
        self.pid = 0

    def handleMessage(self, message):
        result = {}

        if self.debug:
            print(self.name + ' recieved ' + message["action"])

        if not self.is_valid(message):
            result[self.name] = self.failed
            return result

        if "action" in message:
            if(message["action"] == "start"):
                subprocess.call(['/home/pi/git/FPVCar/webserver_tornado/mjpg-streamer/cam.sh'], shell=True)
                result[self.name] = 'cam started'

            if(message["action"] == "stop"):
                pid = subprocess.check_output("ps -ef | grep [m]jpg | awk '{print $2}'", shell=True)
                os.kill(int(pid), signal.SIGTERM)
                result[self.name] = "Killed pid: " + str(pid)

            return result
