from . import Component


class ComponentConfig(Component):
    """handle config persistence"""

    def __init__(self, config, debug=False):
        name = 'ComponentConfig'
        super().__init__(name)
        self.config = config
        self.debug = debug

    def handleMessage(self, message):
        result = {}

        try:
            if self.debug:
                print(self.name + ' received ' + str(message))

            if "get" in message:
                result[self.name] = self.get(message["get"])

            if "load" in message:
                what = message['load']
                if "configuration" == what:
                    result[self.name] =  self.config.load()
                else:
                    result[self.name] = self.get(what)

            if "save" in message:
                self.config.configuration = message["save"]
                result[self.name] = self.save()

            if "set" in message:
                data = message['set']
                for k in data:
                    self.config.configuration[k] = data[k]
                result[self.name] = self.save()
        except Exception as e:
            result[self.name] =  'failed with ' + str(e)
        #
        if self.debug:
            print(self.name + ' result is ' + str(result))
        return result

    # ---------------------------------------------------
    def get(self, what):
        found = ''
        data = self.config.load()
        if what in data:
            found = data[what]
        return found

    def save(self):
        result = self.config.save()
        return result
