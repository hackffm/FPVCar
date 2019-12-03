import tornado.web
import json


class HandlerConfig(tornado.web.RequestHandler):
    def initialize(self, config):
        self.config = self.config
        self.configuration = self.config.configuration

    def get(self):
        self.write(json.dumps(self.configuration))

    def post(self, *args):
        _config = tornado.escape.json_decode(self.request.body)
        if type(_config) == dict:
            self.assign_config(_config)
            self.config.save()
            self.write(json.dumps({'status': 'ok'}))
        else:
            self.write(json.dumps({'status': 'failed'}))
        self.finish()

    def assign_config(self, _config):
        self.config['name'] = _config['name']