import helper_test

from resources import *

config = Config(debug=True)

configuration = config.configuration
config.configuration['audio'] = 'none'
print(config.configuration)
config.save()
config.load()
config.configuration['audio'] = 'off'
config.configuration['test'] = 'test'
print(config.configuration)
config.save()
cfg = config.cfg()
print(cfg.audio)
print(cfg.baud)
print(cfg.debug)
print(cfg.port)
if cfg.debug:
    print('debug is boolen True')
