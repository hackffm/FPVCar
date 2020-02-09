from . import Component


class SerialFake():
    def __init__(self):
        pass

    def write(self, command):
        if command == '?':
            return 'com1'
        else:
            print('serial:' + str(command))


class AdapterDevices(Component):

    def __init__(self, name):
        super().__init__(name)
        self.ser = SerialFake()
        self.debug = True
        self.devices = []
        self.devices_find()

    def handleMessage(self, message):
        result = 'No Handle found'

        if self.debug:
            print('AD:' +self.name + ' recieved ' + message)

        if message == '?':
            result = self.name
        if message == 'list':
            result = str(self.devices_list())

        return result

    def devices_add(self, _device):
        if not 'id' in _device:
            return
        self.devices.append(_device)

    def devices_find(self):
        # todo find what is connected to serial ports
        t = { 'id': 's1', 'port': '/tty/usb0'}
        self.devices_add(t)

    def devices_list(self):
        _dl = []
        if len(self.devices) >= 1:
            for device in self.devices:
                _dl.append(device['id'])
        return _dl
