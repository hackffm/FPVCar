import tornado.web


class HandlerThingsPage(tornado.web.RequestHandler):
    def initialize(self):
        self.name = 'HandlerThings'
        
    def get(self):
        print('......')
        self.render("things.html", title=self.name)
