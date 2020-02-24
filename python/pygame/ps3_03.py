import pygame
import time
import json

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()

done = False

def handleButtons():
    print("Joystick button pressed.")
    joystick = pygame.joystick.Joystick(1)
    joystick.init()

    btTmp = -1
    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        b = joystick.get_button(i)
        if b > 0:
            btTmp = i

        m["bt"] = btTmp

    msg = json.dumps(m)
    print(msg)

def handleJoystick():
    print("Joystick axis motion")
    j = pygame.joystick.Joystick(1)
    j.init()
    xaxis = round(j.get_axis(2), 2)
    yaxis = round(j.get_axis(3), 2)
    print("x: " + str(xaxis) + "   y: " + str(yaxis))
    if (xaxis > 0.01 or xaxis < - 0.01) or (yaxis > 0.01 or yaxis < 0.01):
        left = round(yaxis + xaxis, 2)
        right = round(yaxis - xaxis, 2)
        m["left"] = left
        m["right"] = right
        msg = json.dumps(m)
        print(msg)
    #pos.left = Math.round(Math.min(pos.cy + pos.cx, width / 2));
    #pos.right = Math.round(Math.min(pos.cy - pos.cx, height / 2));
    #    print("Axis "+str(i)+" value: {:>6.3f}".format(axis))

while not done:
    m = {}

    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            handleButtons()
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        elif event.type == pygame.JOYAXISMOTION:
            handleJoystick()


    time.sleep(0.3)




