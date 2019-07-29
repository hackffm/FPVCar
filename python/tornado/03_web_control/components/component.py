

class Component(object):
    """docstring for Component."""

    def __init__(self, type, message_handler):
        self.type = type
        self.message_handler = message_handler

    def handle_message(self, message):
        result = self.message_handler.send(message)
        return result

