from .ps3_controller import Ps3Controller


ps3 = Ps3Controller()
done = False

while not done:
    ps3.loop()
