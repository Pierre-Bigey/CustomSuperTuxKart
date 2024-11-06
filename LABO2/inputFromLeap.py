import time
from enum import Enum

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

address = ('localhost', 6006)

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='127.0.0.1', port=7000, default=True)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class STEER(Enum):
    LEFT = 1
    NEUTRAL = 2
    RIGHT = 3

class ACCEL(Enum):
    UP = 1
    NEUTRAL = 2
    DOWN = 3

#The minimum distance to steer
STEER_DIST_THRES = 0.05
#The minimum distance to accelerate
ACCEL_DIST_THRES = 0.05
#The idle distance (in cm)
IDLE_DIST = 0.15

current_steering = STEER.NEUTRAL
current_accel = ACCEL.NEUTRAL

def callback_tracker_header(*values):
    print("x : "+str(values[0])+ "y : "+str(values[1])+ "z : "+str(values[2]))

    steering = STEER.NEUTRAL

    x = values[0]

    if x < - STEER_DIST_THRES:
        steering = STEER.LEFT
    elif x > STEER_DIST_THRES:
        steering = STEER.RIGHT
    process_steering(steering)

    acceleration = ACCEL.NEUTRAL

    z = values[2] - IDLE_DIST

    if z < - ACCEL_DIST_THRES:
        acceleration = ACCEL.DOWN
    elif z > ACCEL_DIST_THRES:
        acceleration = ACCEL.UP

    process_acceleration(acceleration)


osc.bind(b'/tracker/head/pos_xyz', callback_tracker_header)


def process_acceleration(acceleration):
    data = b''

    global current_accel

    if current_accel != ACCEL.NEUTRAL and acceleration == ACCEL.NEUTRAL:
        if current_accel == ACCEL.UP:
            data = b'R_UP'
        elif current_accel == ACCEL.DOWN:
            data = b'R_DOWN'



    if current_accel == ACCEL.NEUTRAL and acceleration != ACCEL.NEUTRAL:
        if acceleration == ACCEL.UP:
            data = b'P_UP'
        elif acceleration == ACCEL.DOWN:
            data = b'P_DOWN'

    if len(data) > 0:
        client_socket.sendto(data, address)

    current_accel = acceleration

def process_steering(steering):
    global current_steering

    data = b''

    if current_steering != STEER.NEUTRAL and steering == STEER.NEUTRAL:
        if current_steering == STEER.LEFT:
            data = b'R_LEFT'
        elif current_steering == STEER.RIGHT:
            data = b'R_RIGHT'

    if current_steering == STEER.NEUTRAL and steering != STEER.NEUTRAL:
        if steering == STEER.LEFT:
            data = b'P_LEFT'
        elif steering == STEER.RIGHT:
            data = b'P_RIGHT'

    if len(data) > 0:
        client_socket.sendto(data, address)

    current_steering = steering

sleep(1000)
osc.stop()  # Stop the default socket
