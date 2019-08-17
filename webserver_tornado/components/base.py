from . import Component

class Base(Component):

    def handleMessage(self, message):
        print("Base.handleMessage")
        
        if "right" in message:
            self.moveRightLeft(message)
        else:
            print("no usefull command found")
    
    def moveRightLeft(self, message):
        cmd = "f" + str(message["left"]) + " " + str(message["right"]) + "\r"
        print("moveRightLeft: " + cmd)
        self.ser.write(cmd.encode())
