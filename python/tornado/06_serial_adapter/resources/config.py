import json
import os


class Struct(object):
    def __init__(self, adict):
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

    def items(self):
        return self.__dict__.items()

    def __iter__(self):
        return self.__dict__.__iter__()


class Config:

    def __init__(self, name=False, debug=False):

        if not name:
            name = 'labyrinth'

        self.name = name
        home = os.getenv('HOME')
        self.debug = debug

        self.path_config = home + '/' + self.name + '/' + self.name + '.json'
        self.configuration = self.load()

    def cfg(self):
        return Struct(self.configuration)

    def default(self):
        # booleans must be no strings here !
        _config = {
            self.name: {
                'port': 9000,
            },
            'adapters': [
                {
                    'name': 'A1',
                    'devices': [
                        {'name': 'r1d1', 'port': '/dev/ttyS0'},
                        {'name': 'r1d2', 'port': '/dev/ttyS1'}
                    ]
                },
                {
                    'name': 'A2',
                    'devices': [
                        {'name': 'r1d3', 'port': '/dev/ttyS0'},
                        {'name': 'r2d1', 'port': '/dev/ttyS1'}
                    ]
                },
                {
                    'name': 'A3',
                    'devices': [
                        {'name': 'r2d2', 'port': '/dev/ttyS0'},
                    ]
                },
            ],
            'debug': True,
            'default': {
                "log_file": self.name + ".log",
                "log_location": "/home/lxwork/Things/log",
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
