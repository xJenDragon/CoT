from trust_level import TrustLevel

class CirclesOfTrust:
    def __init__(self):
        self.trust_levels = {}

    def add_device_to_trust_level(self, trust_level, device_type, functionalities, device_instance):
        if trust_level not in self.trust_levels:
            self.trust_levels[trust_level] = {}
        self.trust_levels[trust_level][device_type] = {
            'functionalities': functionalities,
            'device_instance': device_instance
        }

    def remove_device_trust_level(self, trust_level, device_type):
        if trust_level in self.trust_levels:
            if device_type in self.trust_levels[trust_level]:
                del self.trust_levels[trust_level][device_type]
                print(f"Device of type '{device_type}' removed from trust level '{trust_level}'.")
            else:
                print(f"No device of type '{device_type}' found in trust level '{trust_level}'.")
        else:
            print(f"Trust level '{trust_level}' does not exist.")

    def execute_device_functionality(self, user, functionality_name, device_type):
        if user in self.trust_levels:
            trust_level = self.trust_levels[user]
            if device_type in trust_level:
                device_info = trust_level[device_type]
                device_instance = device_info['device_instance']
                functionalities = device_info['functionalities']

                if functionality_name in functionalities:
                    # Retrieve the function to call
                    function_to_call = functionalities[functionality_name]

                    if callable(function_to_call):
                        try:
                            # Call the function
                            function_to_call()
                            print(f"Functionality '{functionality_name}' executed for device '{device_type}'.")
                        except Exception as e:
                            print(f"Error while executing functionality '{functionality_name}': {e}")
                    else:
                        raise ValueError(f"Functionality '{functionality_name}' is not callable.")
                else:
                    raise ValueError(f"Functionality '{functionality_name}' not available for this device.")
            else:
                raise ValueError(f"Device type '{device_type}' not available for this user.")
        else:
            raise ValueError(f"User '{user}' not found in trust levels.")
