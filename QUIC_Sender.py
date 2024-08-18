import socket
import threading
import random
import os

from stream import Stream

# This class serves as the client
class QUIC_Sender:

    def __init__(self):
        self.streams = []
        self.connection = None


    def generate_random_bytes(self, size):
        return os.urandom(size)

    def random_grill(self):
        return random.randint(1000, 2000)

    def create_streams(self, num_of_streams):
        packet_size = self.random_grill()
        for i in range (num_of_streams):
            stream_id = i
            stream = Stream(stream_id, packet_size)
            self.streams.append(stream)



    # Function that send a stream of packets
    def send_file(self, stream_id, file_path, server_address=("127.0.0.1", 9999)):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with open(file_path, 'rb') as file:
            seq_no = 0
            while True:
                data = file.read(1024)
                if not data:
                    break
                message = f"{stream_id},{seq_no},{data.decode('latin-1')}"
                client_socket.sendto(message.encode('latin-1'), server_address)
                seq_no += 1
        # Send end of transmission message
        end_message = f"{stream_id},-1,END"
        client_socket.sendto(end_message.encode('latin-1'), server_address)
        client_socket.close()
        print(f"Stream {stream_id}: Completed sending {file_path}")

# Main function
def main():
    num_of_streams = input("Please enter the number of streams you want: ")
    try:
        num_of_streams = int(num_of_streams)
    except ValueError:
        print("Invalid number of streams. Please enter a valid integer.")
        exit()

    # Create streams
    files = []
    data_size = 2 * 1024 * 1024
    for i in range(num_of_streams):
        data = generate_random_bytes(data_size)
        file_name = f"stream_data_{i}.bin"
        files.append(file_name)
        with open(file_name, 'wb') as file:
            file.write(data)
        print(f"Data for stream {i} saved to {file_name}")

    threads = []
    for i, file in enumerate(files):
        thread = threading.Thread(target=send_file, args=(i, file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
