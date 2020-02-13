import helper_test

from resources import *

tc = ThingController()
print(len(tc.things))
for thing in tc.things:
    print(thing.name)
