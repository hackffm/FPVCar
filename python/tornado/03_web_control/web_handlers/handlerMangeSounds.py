import sys
import tornado.web


class HandlerManageSounds(tornado.web.RequestHandler):
    def initialize(self, debug,path_sound):
        self.debug = debug
        self.name = 'shutdown'
        self.path_sound = path_sound

    def get(self):
        self.render("manage_sounds.html", title="Manage Sounds")
        sys.exit(0)

    def post(self):
        result = 'ok'
        for field_name, files in self.request.files.items():
            for file in files:
                try:
                    filename, content_type = file["filename"], file["content_type"]
                    body = file["body"]
                    if self.debug:
                        print('POST {0} {1} {2} bytes'.format(filename, content_type, len(body)))
                    f = open(self.path_sound + '/' + filename, 'w+b')
                    f.write(body)
                    f.close()
                except Exception as e:
                    result = str(e)
        self.write(result)