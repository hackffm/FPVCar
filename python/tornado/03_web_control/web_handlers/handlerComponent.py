import tornado.web
import json


class HandlerComponent(tornado.web.RequestHandler):
    def initialize(self, components, debug):
        self.components = components
        self.debug = debug
        self.result = 'I can not do that !'

    def get(self):
        self.write(self.result)

    def post(self, *args):
        # todo check if valid
        requested = tornado.escape.json_decode(self.request.body)
        if self.debug:
            print('message_component received:' + str(requested))
        if 'component' not in requested:
            return self.result
        if requested['component'] in self.components:
            component = self.components[requested['component']]
            self.result = component.handle_message(requested)
        if self.debug:
            print('[message_component]result:' + str(self.result))
        self.write(json.dumps(self.result))
        self.finish()
