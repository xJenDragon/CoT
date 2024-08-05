import tinytuya
import real_time_transcription
from circles_of_trust import CirclesOfTrust
from orchestrator import bulb_devices_functions, plug_devices_functions

light_device = tinytuya.BulbDevice(
    dev_id='eb93fc2a1cc62cb31cpnxj',
    address='Auto',
    local_key="'|}|CS_-2T{rSMY1",
    version=3.3)

light_device.set_socketPersistent(True)

plug_device = tinytuya.OutletDevice(
    dev_id='eb1f059adf7874f2acdmzu',
    address='Auto',
    local_key="IX4(6X=&QZck{H@*",
    version=3.3)

plug_device.set_socketPersistent(True)

# Create access control system
access_control = CirclesOfTrust()

# Define functionalities
functionalities_light = {
    'set_red': bulb_devices_functions.set_red,
    'set_blue': bulb_devices_functions.set_blue,
    'set_green': bulb_devices_functions.set_green,
    'set_yellow': bulb_devices_functions.set_yellow,
    'set_purple': bulb_devices_functions.set_purple,
    'set_orange': bulb_devices_functions.set_orange,
    'set_pink': bulb_devices_functions.set_pink,
    'set_indigo': bulb_devices_functions.set_indigo,
    'set_cyan': bulb_devices_functions.set_cyan,
    'set_magenta': bulb_devices_functions.set_magenta,
    'set_teal': bulb_devices_functions.set_teal,
    'set_lime': bulb_devices_functions.set_lime,
    'set_white_color': bulb_devices_functions.set_white_color,
    'decrease_saturation': bulb_devices_functions.decrease_saturation,
    'increase_saturation': bulb_devices_functions.increase_saturation,
    'increase_brightness': bulb_devices_functions.increase_brightness,
    'decrease_brightness': bulb_devices_functions.decrease_brightness
}

functionalities_plug = {
    'plug_on': plug_devices_functions.plug_on,
    'plug_off': plug_devices_functions.plug_off
}

# Add devices to trust levels
access_control.add_device_to_trust_level('owner', 'light', functionalities_light, light_device)
access_control.add_device_to_trust_level('owner', 'plug', functionalities_plug, plug_device)


while True:
    real_time_transcription.transcribe_audio(access_control)