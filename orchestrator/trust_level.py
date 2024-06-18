class TrustLevel:
    def __init__(self, name):
        self.name = name
        self.devices = {}

    def add_device(self, device_name, functionalities, device_instance):
        self.devices[device_name] = {
            'functionalities': functionalities,
            'device_instance': device_instance
        }

    def remove_device(self, device_name):
        if device_name in self.devices:
            del self.devices[device_name]

    def get_device_functionalities(self, device_name):
        if device_name in self.devices:
            return self.devices[device_name]['functionalities']
        return []

    def get_device_instance(self, device_name):
        if device_name in self.devices:
            return self.devices[device_name]['device_instance']
        return None