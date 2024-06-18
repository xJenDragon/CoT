# device.py

class Device:
    def __init__(self, name, functionalities, device_instance):
        self.name = name
        self.functionalities = functionalities
        self.device_instance = device_instance

    def execute_functionality(self, functionality_name):
        if functionality_name in self.functionalities:
            method_to_call = getattr(self.device_instance, functionality_name, None)
            if method_to_call:
                method_to_call()
            else:
                raise ValueError(f"Functionality {functionality_name} not available for this device.")
        else:
            raise ValueError(f"Functionality {functionality_name} not available for this device.")
