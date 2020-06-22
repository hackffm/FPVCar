from .thing import Thing

class Thingy(Thing):
    def __init__(self, id, debug=False):
        super().__init__(id)
        self.debug = debug

    def handleMessage(self, message):
        result = ''
