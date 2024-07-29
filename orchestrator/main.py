import tinytuya
import real_time_transcription
from circles_of_trust import CirclesOfTrust

# update

d = tinytuya.BulbDevice(
    dev_id='eb93fc2a1cc62cb31cpnxj',
    address='Auto',
    local_key=";^y8G]^MVpAMmZry",
    version=3.3)

d.set_socketPersistent(True)

plug = tinytuya.OutletDevice(
    dev_id='eb1f059adf7874f2acdmzu',
    address='Auto',
    local_key="IX4(6X=&QZck{H@*",
    version=3.3)

plug.set_socketPersistent(True)

# Create access control system
access_control = CirclesOfTrust()

# Define functionalities
functionalities_light = [
    'set_red', 'set_blue', 'set_green', 'set_yellow', 'set_purple',
    'set_orange', 'set_pink', 'set_indigo', 'set_cyan', 'set_magenta',
    'set_teal', 'set_lime', 'set_white_color', 'decrease_saturation',
    'increase_saturation', 'increase_brightness', 'decrease_brightness'
]

functionalities_plug = [
    'plug_on', 'plug_off'
]

# Add devices to trust levels
access_control.add_device_to_trust_level('owner', 'light', functionalities_light, d)
access_control.add_device_to_trust_level('owner', 'plug', functionalities_plug, plug)

# Add users to trust levels
access_control.add_user_to_trust_level('owner', 'owner')

while True:
    real_time_transcription.transcribe_audio(access_control)