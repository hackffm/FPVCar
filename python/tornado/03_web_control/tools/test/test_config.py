import helper_test

from resources import *

config = Config(debug=True)

configuration = config.configuration
config.configuration['audio'] = 'none'
print(config.configuration)
config.save()
config.load()
config.configuration['audio'] = 'off'
print(config.configuration)
config.save()
