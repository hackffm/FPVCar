import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self, helper, port, things_controller):
        self.helper = helper
        self.name = 'HandlerThings'
        self.port = port
        self.things_controller = things_controller

    def get(self):
        ip_first = self.helper.interfaces_first()
        things_qty = len(self.things_controller.things)
        things = []
        for t in self.things_controller.things:
            t = str(t.name)
            t = t.replace(" ", "")
            things.append([t])
        self.render("things.html", ip_first=ip_first, title=self.name, port=self.port, things=things, things_qty=things_qty)
