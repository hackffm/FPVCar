import tornado.web


class HandlerIndexPage(tornado.web.RequestHandler):
    def initialize(self):
        self.name = 'index page'

    def get(self):
        self.render("index.html")
