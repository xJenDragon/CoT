from trust_level import TrustLevel

class CirclesOfTrust:
    def __init__(self):
        self.trust_levels = {
            'owner': TrustLevel('owner'),
            'trusted': TrustLevel('trusted'),
            'partially_trusted': TrustLevel('partially_trusted'),
            'untrusted': TrustLevel('untrusted')
        }
        self.user_to_trust_level = {}

    def add_trust_level(self, name):
        if name not in self.trust_levels:
            self.trust_levels[name] = TrustLevel(name)

    def remove_trust_level(self, name):
        if name in self.trust_levels and name != 'owner':
            del self.trust_levels[name]

    def add_user_to_trust_level(self, user, trust_level_name):
        if trust_level_name in self.trust_levels:
            self.user_to_trust_level[user] = trust_level_name

    def remove_user_from_trust_level(self, user):
        if user in self.user_to_trust_level:
            del self.user_to_trust_level[user]

    def get_trust_level_for_user(self, user):
        return self.user_to_trust_level.get(user, 'untrusted')

    def add_device_to_trust_level(self, trust_level_name, device_name, functionalities, device_instance):
        if trust_level_name in self.trust_levels:
            self.trust_levels[trust_level_name].add_device(device_name, functionalities, device_instance)

    def remove_device_from_trust_level(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            self.trust_levels[trust_level_name].remove_device(device_name)

    def get_functionalities_for_device(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            return self.trust_levels[trust_level_name].get_device_functionalities(device_name)
        return []

    def get_device_instance(self, trust_level_name, device_name):
        if trust_level_name in self.trust_levels:
            return self.trust_levels[trust_level_name].get_device_instance(device_name)
        return None

    def execute_device_functionality(self, user, functionality_name, device_name):
        trust_level_name = self.get_trust_level_for_user(user)
        hierarchy = ['untrusted', 'partially_trusted', 'trusted', 'owner']

        if trust_level_name not in hierarchy:
            raise ValueError(f"Unknown trust level: {trust_level_name}")

        allowed = False
        for level in hierarchy[hierarchy.index(trust_level_name):]:
            if device_name in self.trust_levels[level].devices:
                allowed = True
                device_instance = self.trust_levels[level].get_device_instance(device_name)
                functionalities = self.get_functionalities_for_device(level, device_name)
                if functionality_name in functionalities:
                    try:
                        method_to_call = getattr(device_instance, functionality_name, None)
                        if method_to_call:
                            method_to_call()
                            print(f"Executed {functionality_name} for {trust_level_name}.")
                            return
                        else:
                            raise ValueError(f"Functionality {functionality_name} not available for this device.")
                    except Exception as e:
                        print(f"Failed to execute functionality: {e}")
                        raise
                else:
                    raise ValueError(f"Functionality '{functionality_name}' not available for this device.")
        if not allowed:
            raise ValueError(f"Device '{device_name}' not found for this trust level or higher")
