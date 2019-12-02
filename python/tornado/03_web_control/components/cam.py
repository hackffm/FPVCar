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
        self.pid = 0

    def handleMessage(self, message):
        result = ''

        if self.debug:
            print(self.name + ' recieved ' + str(message))

        if "action" in message:
            if(message["action"] == "start"):
                subprocess.call(['/home/pi/git/FPVCar/webserver_tornado/mjpg-streamer/cam.sh'], shell=True)
                result = 'cam started'

            if(message["action"] == "stop"):
                try:
                    pid = subprocess.check_output("ps -ef | grep [m]jpg | awk '{print $2}'", shell=True)
                    os.kill(int(pid), signal.SIGTERM)
                    result = "Killed pid: " + str(pid)
                except Exception as e:
                    result = str(e)
            return result
