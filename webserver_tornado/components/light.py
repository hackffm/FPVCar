from . import Component

class Light(Component):

    def handleMessage(self, message):
        print("Light.handleMessage")
    
        if(message["type"] == "white"):
            cmd = "Tw" + str(message["intensity"]) + "\r"
            print("white: " + cmd)
            self.ser.write(cmd.encode())
        elif(message["type"] == "uv"):
            cmd = "Tu" + str(message["intensity"]) + "\r"
            print("uv: " + cmd)
            self.ser.write(cmd.encode())