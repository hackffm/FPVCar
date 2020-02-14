import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self, things_controller):
        self.name = 'HandlerThings'
        self.things_controller = things_controller
        
    def get(self):
        things_qty = len(self.things_controller.things)
        self.render("things.html", title=self.name, things_qty=things_qty)
