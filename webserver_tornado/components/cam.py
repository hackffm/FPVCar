from . import Component
import os
import subprocess

class Cam(Component):

    def handleMessage(self, message):
        print("Cam.handleMessage")
        
        if "action" in message:
            if(message["action"] == "start"):
                print(message["action"])
                #os.system("~/git/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o \"output_http.so -w ./www\" -i \"input_raspicam.so\"")
                subprocess.call(['/home/pi/git/mjpg-streamer/mjpg-streamer-experimental/cam.sh'])