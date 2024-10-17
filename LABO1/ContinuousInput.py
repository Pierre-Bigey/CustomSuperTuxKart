import math

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


steer = 0
accel = 0


# We don't use the pitch
def callback_pitch(*values):
    return

# yaw will control steering
def callback_yaw(*values):
    global steer
    angle = values[0]
    #The steer value is between -1 and 1 (angle between -80 and 80)
    maximum = 30
    steer = max(min(angle, maximum), -maximum)/maximum


# Roll will control the acceleration
def callback_roll(*values):
    global accel
    angle = values[0]

    offset = -50
    threshold = 30

    #The acceleration value is between -1 and 1 which corresponds to angle between -70 and -30
    accel = angle - offset
    accel = max(min(accel, threshold), -threshold)/threshold



address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)


osc.bind(b'/multisense/orientation/pitch', callback_pitch)
osc.bind(b'/multisense/orientation/yaw', callback_yaw)
osc.bind(b'/multisense/orientation/roll', callback_roll)


loop_time_accel = 10
loop_time_steer = 30

frq = 120

in_loop_position_accel = 0
in_loop_position_steer = 0

while True :

    # print("\n\n\n\n\n\n\n\n\n\n\n\n")
    # print("Steer: ", steer)
    # print("Accel: ", accel)
    steer_time = loop_time_steer - int(abs(steer) * loop_time_steer)
    accel_time = loop_time_accel - int(abs(accel) * loop_time_accel)

    if in_loop_position_steer == steer_time :
        if steer > 0:
            data = b'P_LEFT'
            client_socket.sendto(data, address)
        elif steer < 0:
            data = b'P_RIGHT'
            client_socket.sendto(data, address)

    if in_loop_position_accel == accel_time :
        if accel > 0:
            data = b'P_UP'
            client_socket.sendto(data, address)
        elif accel < 0:
            data = b'P_DOWN'
            client_socket.sendto(data, address)

    sleep(1 / frq)

    in_loop_position_accel += 1
    if in_loop_position_accel >= loop_time_accel:
        data = b'R_UP'
        client_socket.sendto(data, address)
        data = b'R_DOWN'
        client_socket.sendto(data, address)

        in_loop_position_accel = 0

    in_loop_position_steer += 1
    if in_loop_position_steer >= loop_time_steer:
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        data = b'R_RIGHT'
        client_socket.sendto(data, address)

        in_loop_position_steer = 0
