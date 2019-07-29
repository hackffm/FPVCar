import tornado.web
import json


class HandlerBase(tornado.web.RequestHandler):
    def initialize(self):
        self.base = {'component': 'base', 'stop': 0 }

    def get(self):
        self.write(json.dumps(self.base))

    def post(self, *args):
        # todo check if valid
        self.base = tornado.escape.json_decode(self.request.body)
        self.write(json.dumps(self.base))
        self.finish()
