
# This is the QUIC receiver that listens for incoming UDP packets on port 9999.
import socket
import threading
# Function to handle incoming packets
def handle_client(server_socket, stop_event):
    while not stop_event.is_set():
        data, addr = server_socket.recvfrom(2048)
        if data:
            stream_id, seq_no, message = parse_message(data)
            if message == "END":
                print(f"Stream {stream_id}: Received end of transmission signal")
                stop_event.set()
                break
            print(f"Stream {stream_id}: Received message {seq_no} - {message} from {addr}")
# Function to parse incoming messages
def parse_message(data):
    parts = data.decode('latin-1').split(',')
    stream_id = int(parts[0])
    seq_no = int(parts[1])
    message = ','.join(parts[2:])
    return stream_id, seq_no, message
# Main function
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
