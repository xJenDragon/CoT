from trust_level import TrustLevel

class CirclesOfTrust:

    def __init__(self):
        self.trust_levels = {
            'owner': TrustLevel('owner'),
            'trusted': TrustLevel('trusted'),
            'partially_trusted': TrustLevel('partially_trusted'),
            'untrusted': TrustLevel('untrusted')
        }

    def add_trust_level(self, name):
        if name not in self.trust_levels:
            self.trust_levels[name] = TrustLevel(name)

    def remove_trust_level(self, name):
        if name in self.trust_levels and name != 'owner':
            del self.trust_levels[name]

    def add_device_to_trust_level(self, trust_level_name, device):
        if trust_level_name in self.trust_levels:
            self.trust_levels[trust_level_name].add_device(device.name, device.functionalities)

    def remove_device_from_trust_level(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            self.trust_levels[trust_level_name].remove_device(device_name)

    def get_functionalities_for_device(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            return self.trust_levels[trust_level_name].get_device_functionalities(device_name)
        return []

    def get_device_instance(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            return self.trust_levels[trust_level_name].devices.get(device_name)
        return None
