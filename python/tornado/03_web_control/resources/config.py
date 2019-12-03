import json
import os


class Config:

    def __init__(self, name=False, debug=False):

        if not name:
            name = 'fpvcar'

        self.name = name
        home = os.getenv('HOME')
        self.config_path = home + '/' + self.name + '/config.json'
        self.debug = debug

        self.configuration = self.load()

    def load(self):
        if os.path.exists(self.config_path):
            if self.debug:
                print('load config from', self.config_path)
            with open(self.config_path) as json_data:
                j_config = json.load(json_data)
            return j_config
        else:
            if self.debug:
                print('new config', self.config_path)
            return {'name': self.name}

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
        return
