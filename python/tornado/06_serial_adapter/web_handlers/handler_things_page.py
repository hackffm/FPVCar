import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self, helper, port, serial_handler):
        self.helper = helper
        self.name = 'HandlerThings'
        self.port = port
        self.serial_handler = serial_handler

    def get(self):
        ip_first = self.helper.interfaces_first()
        things_qty = len(self.serial_handler.things_serial)
        things = []
        for thing in self.serial_handler.things_serial:
            t = str(thing.id)
            t = t.replace(" ", "")
            things.append([t])
        self.render("things.html", ip_first=ip_first, title=self.name, port=self.port, things=things, things_qty=things_qty)
