import json
import os


class Struct(object):
    def __init__(self, adict):
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)


class Config:

    def __init__(self, name=False, debug=False):

        if not name:
            name = 'fpvcar'

        self.name = name
        home = os.getenv('HOME')
        self.debug = debug

        self.path_config = home + '/' + self.name + '/config.json'
        self.path_fpvcar = home + '/' + self.name
        self.configuration = self.load()

    def cfg(self):
        return Struct(self.configuration)

    def default(self):
        # booleans must be no strings here !
        _config = {
            'serial': {
                'baud': 38400,
                'port': '/dev/ttyS0'
            },
            'camera': {
                'orientation': 'horizontal',
                'resolutionX': 640,
                'resolutionY': 480
            },
            'debug': False,
            'name': self.name,
            'port': 9090,
            'sensors': {
                'bno055': False
            }
        }
        return _config

    def load(self):
        if os.path.exists(self.path_config):
            if self.debug:
                print('load config from', self.path_config)
            with open(self.path_config) as json_data:
                self.configuration = json.load(json_data)
        else:
            if self.debug:
                print('new config', self.path_config)
            self.configuration = self.default()
            self.save()

        return self.configuration

    def save(self):
        data = json.dumps(self.configuration, indent=4)
        _dir = os.path.dirname(self.path_config)
        if not os.path.exists(_dir):
            if self.debug:
                print('create folder ', _dir)
            os.makedirs(_dir)
        with open(self.path_config, 'w') as outfile:
            outfile.write(data)
        if self.debug:
            print('new config saved in', self.path_config)
        return True
