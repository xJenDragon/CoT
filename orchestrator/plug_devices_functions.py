import time

import tinytuya

# for testing purposes
plug = tinytuya.OutletDevice(
    dev_id='eb1f059adf7874f2acdmzu',
    address='Auto',
    local_key="IX4(6X=&QZck{H@*",
    version=3.3)

plug.set_socketPersistent(True)

# ---------------------------------------- PLUG FUNCTIONS --------------------------------------------------------------

def plug_on():
    plug.turn_on()

def plug_off():
    plug.turn_off()
