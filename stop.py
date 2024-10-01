
import socket

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = b'STOPSERVEUR'

client_socket.sendto(data, address)
client_socket.close()