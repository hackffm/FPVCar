

class Component(object):
    """docstring for Component."""

    def __init__(self, name, debug=False):
        self.debug = debug
        self.name = name

    def handle_message(self, message):
        print(message)

    def is_valid(self, message):
        if self.name in message:
            return True
        return False