import json
import tornado.web

from time import sleep

class HandlerManageSounds(tornado.web.RequestHandler):
    def initialize(self, debug, helper, path_sound):
        self.debug = debug
        self.helper = helper
        self.name = 'HandlerManageSounds'
        self.path_sound = path_sound

    def show_ip(self):
        remote_ip = self.request.headers.get("X-Real-IP") or \
                    self.request.headers.get("X-Forwarded-For") or \
                    self.request.remote_ip
        print(self.name + ' was called by ' + remote_ip)

    # handler methods-------------------------------------------------------------
    def delete(self):
        result = 'none'
        if self.request.headers['Content-Type'] == 'application/json':
            deletion =  tornado.escape.json_decode(self.request.body)
            if 'delete' in deletion:
                _del = deletion['delete']
                result = self.helper.file_delete(self.path_sound + '/' + _del)
                if self.debug:
                    print('deletion result of ' + _del + ' was ' + result)
            self.write(json.dumps({'delete': str(result)}))
            self.finish()

    def get(self):
        if self.debug:
            self.show_ip()
        sound_files = self.helper.files_in_path(self.path_sound)
        self.render("manage_sounds.html", title="Manage Sounds", sound_files=sound_files)

    def post(self):
        if self.debug:
            self.show_ip()
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
                    self.write(str(e))
        self.redirect('/manage_sounds', permanent=False)
