import pygame

class Component:

    def __init__(self, ser):
        self.ser = ser

    def handleMessage(self, message):
        print(message)
        
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
        
class Sound(Component):

    def __init__(self, ser):
        self.ser = ser
        pygame.mixer.init(44100, -16, 1, 1024)

    def playSound(self, name):
        if name == "chicken":
            pygame.mixer.music.load("sound/chicken.wav")
            pygame.mixer.music.play()
        elif name == "sheep":
            pygame.mixer.music.load("sound/sheep.wav")
            pygame.mixer.music.play()
        elif name == "cat":
            pygame.mixer.music.load("sound/cat.wav")
            pygame.mixer.music.play()
        else:
            print("no sound found for " + name)

    def handleMessage(self, message):
        print("Sound.handleMessage")
        if "sound" in message:
            self.playSound(message["sound"])