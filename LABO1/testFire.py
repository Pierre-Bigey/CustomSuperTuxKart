import time

from oscpy.server import OSCThreadServer
from time import sleep
import socket



def dump(address, *values):
    print(u'{}: {}'.format(
        address.decode('utf8'),
        ', '.join(
            '{}'.format(
                v.decode(options.encoding or 'utf8')
                if isinstance(v, bytes)
                else v
            )
            for v in values if values
        )
    ))


time_of_last_touch_up = time.time()

def callback_pad_x(*values):
    return

def callback_pad_y(*values):
    return

def callback_touchup(*values):
    global time_of_last_touch_up

    threshold_thouch_up = 0.5
    if time.time() - time_of_last_touch_up < threshold_thouch_up:
        print("FIRE")
    time_of_last_touch_up = time.time()


address = ('localhost', 6006)

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/pad/x', callback_pad_x)
osc.bind(b'/multisense/pad/y', callback_pad_y)
osc.bind(b'/multisense/pad/touchUP', callback_touchup)

sleep(1000)
osc.stop()  # Stop the default socket


