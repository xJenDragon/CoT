class TrustLevel:
    def __init__(self, name):
        self.name = name
        self.devices = {}

    def add_device(self, device_name, functionalities):
        self.devices[device_name] = functionalities

    def remove_device(self, device_name):
        if device_name in self.devices:
            del self.devices[device_name]

    def get_device_functionalities(self, device_name):
        return self.devices.get(device_name, [])