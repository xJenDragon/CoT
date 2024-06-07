from circles_of_trust import CirclesOfTrust
from device import Device


class AccessControl:
    def __init__(self):
        self.circles_of_trust = CirclesOfTrust()
        self.devices = {}

    def get_access(self, trust_level_name, device_name):
        return self.circles_of_trust.get_functionalities_for_device(trust_level_name, device_name)

    def add_trust_level(self, name):
        self.circles_of_trust.add_trust_level(name)

    def remove_trust_level(self, name):
        self.circles_of_trust.remove_trust_level(name)

    def add_device(self, trust_level, device_name, functionalities, device_instance):
        if trust_level not in self.devices:
            self.devices[trust_level] = {}
        device = Device(device_name, functionalities, device_instance)
        self.devices[trust_level][device_name] = device
        self.circles_of_trust.add_device_to_trust_level(trust_level, device)

    def remove_device(self, trust_level_name, device_name):
        self.circles_of_trust.remove_device(trust_level_name, device_name)

    def execute_device_functionality(self, trust_level, functionality, device_name):
        if trust_level in self.devices and device_name in self.devices[trust_level]:
            device = self.devices[trust_level][device_name]
            device.execute_functionality(functionality)
        else:
            raise ValueError(f"Device '{device_name}' not found for this trust level")