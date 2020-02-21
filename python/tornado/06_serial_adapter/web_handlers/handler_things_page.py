import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self, helper, port, serial_handler):
        self.helper = helper
        self.name = 'HandlerThings'
        self.port = port
        self.serial_handler = serial_handler

    def get(self):
        ip_first = self.helper.interfaces_first()
        thingies_qty = len(self.serial_handler.thingies())
        thingies = []
        for t in self.serial_handler.thingies():
            thingies.append([t])
        self.render("things.html", ip_first=ip_first, title=self.name, port=self.port, thingies=thingies, thingies_qty=thingies_qty)
