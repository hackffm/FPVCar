from components import *

class AdapterController:
    def __init__(self):
        self.adapters = []

    def adapter_exists(self, name):
        for adapter in self.adapters:
            if adapter.name == name:
                return True
        return False

    def adapters_add(self, adapter):
        if type(adapter) != AdapterDevices:
            print('error:unexpected type')
            return
        self.adapters.append(adapter)

    def device_exists(self, name):
        for adapter in self.adapters:
            if adapter.device_exists(name):
                return True
        return False

    def device_write(self, device_name, command):
        if self.device_exists(device_name):
            for adapter in self.adapters:
                if adapter.device_exists(device_name):
                    adapter.write(device_name, command)