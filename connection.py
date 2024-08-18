import socket

# Connection class to send packets to the server
class Connection:
    def __init__(self, server_address=("127.0.0.1", 9999)):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packet(self, packet):
        self.socket.sendto(packet.encode(), self.server_address)

    def close(self):
        self.socket.close()