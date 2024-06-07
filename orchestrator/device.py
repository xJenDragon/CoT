class Device:
    def __init__(self, name, functionalities, device_instance):
        self.name = name
        self.functionalities = functionalities
        self.device_instance = device_instance

    def execute_functionality(self, functionality):
        if functionality in self.functionalities:
            func = getattr(self.device_instance, functionality)()
            func()
        else:
            raise ValueError(f"Functionality {functionality} not available for this device.")
