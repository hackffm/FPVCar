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
        thingies_verified = []
        thingies_not_verified = []
        for ts in self.serial_handler.things_serial:
            if ts.verified:
                for ty in ts.thingies:
                    thingies_verified.append([ts.id, ty.id])
            if not ts.verified:
                for ty in ts.thingies:
                    thingies_not_verified.append([ts.id, ty.id])
        self.render("things.html",
                    ip_first=ip_first,
                    title=self.name,
                    port=self.port,
                    thingies_verified=thingies_verified,
                    thingies_not_verified=thingies_not_verified,
                    thingies_qty=thingies_qty)
