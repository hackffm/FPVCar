from . import Component


class ComponentConfig(Component):
    """handle config persistence"""

    def __init__(self, config, debug=False):
        name = 'ComponentConfig'
        super().__init__(name)
        self.config = config
        self.debug = debug

    def handleMessage(self, message):
        result = self.failed

        if self.debug:
            print(self.name + ' recieved ' + str(message))

        if "load" in message:
            result = self.config.load()
            return result
        if "save" in message:
            self.config.configuration = message["save"]
            result = self.config.save()
            return result

        return result
