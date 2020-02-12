import sys
import tornado.web


class HandlerThings(tornado.web.RequestHandler):
    def initialize(self, things_controller):
        self.things_controller = things_controller
        self.name = 'things_handler'

    def get(self):
        things = []
        for tc in things_controller:
            things.append(tc.name)
        self.render("things.html", title="Things Controller", items=things_controller)
