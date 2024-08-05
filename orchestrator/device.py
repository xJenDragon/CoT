# device.py

class Device:
    def __init__(self, name, functionalities, device_instance):
        self.name = name
        self.functionalities = functionalities
        self.device_instance = device_instance

    def execute_functionality(self, functionality_name):
        if functionality_name in self.functionalities:
            func = self.functionalities[functionality_name]
            func()  # Call the function
        else:
            raise ValueError(f"Functionality {functionality_name} not available for this device.")
