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

        self.configuration = ''
        self.debug = debug
        self.home = os.getenv('HOME')
        self.name = name

        self.path_config = self.home + '/labyrinth/' + self.name + '.json'
        self.load()

    def cfg(self):
        return Struct(self.configuration)

    def default(self):
        # booleans must be no strings here !
        _config = {
            self.name: {
                'port': 9000,
            },
            'things_serial': [
                {
                    'ID': 'A1',
                    'port': '/dev/ttyS0',
                    'thingies': [
                        {'ID': 'D1'},
                        {'ID': 'L1'}
                    ]
                },
                {
                    'ID': 'A2',
                    'port': '/dev/ttyS1',
                    'thingies': [
                        {'ID': 'D2'},
                        {'ID': 'D3'}
                    ]
                },
                {
                    'ID': 'VK',
                    'port': '/dev/ttyACM0',
                    'thingies': [
                        {'ID': 'D4'}
                    ]
                },
            ],
            'debug': True,
            'default': {
                "log_file": self.name + ".log",
                "log_location": self.home + "/labyrinth/log",
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
        return

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
