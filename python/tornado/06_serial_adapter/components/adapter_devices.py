from . import Component


class SerialFake:
    def __init__(self, port, baud, debug=False):
        self.baud = baud
        self.debug = debug
        self.port = port

    def write(self, command):
        if self.debug:
            print('port {}, baud {}, command {}'.format(
                str(self.port), str(self.baud), str(command)
            ))
        return


class Device():
    def __init__(self, name, port, debug=False):
        self.name = name
        self.ser = SerialFake(port, 38400, debug)
        self.debug = debug

    def write(self, command):
        if self.debug:
            print('device {} recieved command {}'.format(
                self.name, str(command)
            ))
        self.ser.write(command)


class AdapterDevices(Component):

    def __init__(self, name, devices, debug=False):
        super().__init__(name)
        self.debug = debug
        self.devices = []
        for device in devices:
            self.devices_add(device)

    def handleMessage(self, message):
        result = 'No Handle found'

        if self.debug:
            print('AD:' +self.name + ' recieved ' + message)

        if message == '?':
            result = self.name
        if message == 'list':
            result = str(self.devices_list())

        return result

    def device_exists(self, name):
        for device in self.devices:
            if device.name == name:
                return True
        return False

    def devices_add(self, _device):
        if 'name' not in _device:
            return False
        if 'debug' in _device:
            self.devices.append((Device(_device['name'], _device['port'], _device['debug'])))
        else:
            self.devices.append((Device(_device['name'], _device['port'], self.debug)))
        return True

    def devices_list(self):
        _dl = []
        if len(self.devices) >= 1:
            for device in self.devices:
                _dl.append(device['id'])
        return _dl

    def write(self,name,  command):
        for device in self.devices:
            if device.name == name:
                device.write(command)
