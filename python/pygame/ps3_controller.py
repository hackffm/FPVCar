import pygame
import time
import json
import _thread

class Ps3Controller:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(1)
        joystick.init()

    def loop(self):
        done = False
        while not done:
            for event in pygame.event.get():  # User did something.
                if event.type == pygame.QUIT:  # If user clicked close.
                    done = True  # Flag that we are done so we exit this loop.
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.handleButtons()
                elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                elif event.type == pygame.JOYAXISMOTION:
                    self.handleJoystick()

            time.sleep(0.3)

    def handleButtons(self):
        print("Joystick button pressed.")
        joystick = pygame.joystick.Joystick(1)
        joystick.init()

        m = {}
        btTmp = -1
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            b = joystick.get_button(i)
            if b > 0:
                btTmp = i

            m["bt"] = btTmp

        msg = json.dumps(m)
        print(msg)

    def handleJoystick(self):
        print("Joystick axis motion")
        j = pygame.joystick.Joystick(1)
        j.init()
        xaxis = round(j.get_axis(2), 2)
        yaxis = round(j.get_axis(3), 2)
        print("x: " + str(xaxis) + "   y: " + str(yaxis))
        if (xaxis > 0.01 or xaxis < - 0.01) or (yaxis > 0.01 or yaxis < 0.01):
            left = round(yaxis + xaxis, 2)
            right = round(yaxis - xaxis, 2)
            m = {}
            m["left"] = left
            m["right"] = right
            msg = json.dumps(m)
            print(msg)

if __name__ == "__main__":
    ps3 = Ps3Controller()
    done = False
    _thread.start_new_thread(ps3.loop(), ("test", 1, ))
    while not done:
        time.sleep(0.3)
        print("again")
