import socket
import threading

from packet import Packet

# Function to handle incoming packets
def handle_client(server_socket, stop_event):
    while not stop_event.is_set():
        data, addr = server_socket.recvfrom(2048)
        if data:
            packet = Packet.decode(data)
            if packet.data == b"END":
                print(f"Stream {packet.stream_id}: Received end of transmission signal")
                stop_event.set()
                break
            print(f"Stream {packet.stream_id}: Received message {packet.seq_no} from {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 9999))
    print("UDP server up and listening")

    stop_event = threading.Event()
    server_thread = threading.Thread(target=handle_client, args=(server_socket, stop_event))
    server_thread.start()
    server_thread.join()
    server_socket.close()

if __name__ == '__main__':
    main()
