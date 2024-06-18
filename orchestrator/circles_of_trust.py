from device import Device


class CirclesOfTrust:
    def __init__(self):
        self.trust_levels = {
            'owner': {},
            'trusted': {},
            'partially_trusted': {},
            'untrusted': {}
        }

    def add_trust_level(self, name):
        if name not in self.trust_levels:
            self.trust_levels[name] = {}

    def remove_trust_level(self, name):
        if name in self.trust_levels and name != 'owner':
            del self.trust_levels[name]

    def add_device(self, trust_level, device_name, functionalities, device_instance):
        if trust_level not in self.trust_levels:
            self.add_trust_level(trust_level)
        device = Device(device_name, functionalities, device_instance)
        self.trust_levels[trust_level][device_name] = device

    def remove_device(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels and device_name in self.trust_levels[trust_level_name]:
            del self.trust_levels[trust_level_name][device_name]

    def get_functionalities_for_device(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels and device_name in self.trust_levels[trust_level_name]:
            return self.trust_levels[trust_level_name][device_name].functionalities
        return []

    def execute_device_functionality(self, trust_level, functionality, device_name):
        hierarchy = ['untrusted', 'partially_trusted', 'trusted', 'owner']
        if trust_level not in hierarchy:
            raise ValueError(f"Unknown trust level: {trust_level}")

        allowed = False
        for level in hierarchy[hierarchy.index(trust_level):]:
            if device_name in self.trust_levels[level]:
                allowed = True
                device = self.trust_levels[level][device_name]
                try:
                    # Check if the functionality exists in the device's functionalities
                    if functionality.__name__ in device.functionalities:
                        functionality()  # Call the function object directly
                        print(f"Executed {functionality.__name__} for {trust_level}.")
                        return  # Exit function after successful execution
                    else:
                        raise ValueError(f"Functionality {functionality.__name__} not available for this device.")
                except Exception as e:
                    print(f"Failed to execute functionality: {e}")
                    raise  # Raise exception if execution fails

        if not allowed:
            raise ValueError(f"Device '{device_name}' not found for this trust level or higher")
