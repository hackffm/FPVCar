import pygame
import time
import json

pygame.init()
pygame.joystick.init()
done = False

mbutton = -1;

while not done:
    m = {}

    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    joystick = pygame.joystick.Joystick(1)
    joystick.init()
    name = joystick.get_name()
    print("Joystick name: " + name)

    axes = joystick.get_numaxes()
    for i in range(axes):
        axis = joystick.get_axis(i)
        #print("Axis "+str(i)+" value: {:>6.3f}".format(axis))

    btTmp = -1;
    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        b = joystick.get_button(i)
        if b > 0:
            btTmp = i

    if btTmp is not -1 and mbutton is not btTmp:
        m["bt"] = btTmp
        mbutton = btTmp


    msg = json.dumps(m)
    print(msg)

    time.sleep(0.3)



