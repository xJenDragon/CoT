import tinytuya
import real_time_transcription
from circles_of_trust import CirclesOfTrust

# update

d = tinytuya.BulbDevice(
    dev_id='eb600ddbcb73cc37f0eigw',
    address='Auto',
    local_key="$NRzp{%1/S4^KW(=",
    version=3.3)

d.set_socketPersistent(True)

# create access control system
access_control = CirclesOfTrust()

# define functionalities
functionalities = [
    'set_red', 'set_blue', 'set_green', 'set_yellow', 'set_purple',
    'set_orange', 'set_pink', 'set_indigo', 'set_cyan', 'set_magenta',
    'set_teal', 'set_lime', 'set_white_color', 'decrease_saturation',
    'increase_saturation', 'increase_brightness', 'decrease_brightness'
]

# create base
access_control.add_device_to_trust_level('owner', 'light', functionalities, d)

while True:
    real_time_transcription.transcribe_audio(access_control)
