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
        self.config_path = home + '/' + self.name + '/config.json'
        self.debug = debug

        self.configuration = self.load()

    def cfg(self):
        return Struct(self.configuration)

    def default(self):
        # booleans must be no strings here !
        _config = {
            'baud': 38400,
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
        if os.path.exists(self.config_path):
            if self.debug:
                print('load config from', self.config_path)
            with open(self.config_path) as json_data:
                self.configuration = json.load(json_data)
        else:
            if self.debug:
                print('new config', self.config_path)
            self.configuration = self.default()
            self.save()

        return self.configuration

    def save(self):
        data = json.dumps(self.configuration, indent=4)
        _dir = os.path.dirname(self.config_path)
        if not os.path.exists(_dir):
            if self.debug:
                print('create folder ', _dir)
            os.makedirs(_dir)
        with open(self.config_path, 'w') as outfile:
            outfile.write(data)
        if self.debug:
            print('new config saved in', self.config_path)
        return True
