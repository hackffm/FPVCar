from . import handler_console

class Component(object):
    """docstring for Component."""

    def __init__(self, type, message_handler=handler_console):
        self.type = type
        self.message_handler = message_handler

    def handleMessage(self, message):
        result = self.message_handler.send(message)
        return result

# -- Helper -----------------------
    def is_type(self, _type):
        if self.type == _type:
            return True
        else:
            return False
