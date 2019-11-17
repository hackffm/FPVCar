

class Component(object):
    """docstring for Component."""

    def __init__(self, name, debug=False):
        self.debug = debug
        self.name = name

    def handle_message(self, message):
        print(message)
