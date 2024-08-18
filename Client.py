import threading
import os
import time
import matplotlib.pyplot as plt
from stream import Stream
from connection import Connection
from packet import Packet

# Generating random bytes for data
def generate_random_bytes(size):
    return os.urandom(size)

# Function that send a stream of packets
def send_stream(stream_id, file_path):
    stream = Stream(stream_id, file_path)
    connection = Connection()
    total_bytes_sent = 0
    total_packets_sent = 0
    start_time = time.time()

    try:
        # Iteration over all packets in the stream
        for packet in stream.read_packet():
            connection.send_packet(packet)
            total_bytes_sent += len(packet.data)
            total_packets_sent += 1
        # Send an end packet to indicate completion of the stream
        end_packet = Packet(stream_id, -1, b"END")
        connection.send_packet(end_packet)
        print(f"Stream {stream_id}: Completed sending {file_path}")
    finally:
        # Ensure the connection is closed and calculate the elapsed time
        connection.close()
        elapsed_time = time.time() - start_time
        return total_bytes_sent, total_packets_sent, elapsed_time

# Main function
def main():
    # Input number of streams
    num_of_streams = input("Please enter the number of streams you want: ")
    try:
        num_of_streams = int(num_of_streams)
    except ValueError:
        print("Invalid number of streams. Please enter a valid integer.")
        exit()

    files = []
    data_size = 2 * 1024 * 1024  # Size of each data file in bytes
    for i in range(num_of_streams):
        # Generate random data and save it to a file
        data = generate_random_bytes(data_size)
        file_name = f"stream_data_{i}.bin"
        files.append(file_name)
        with open(file_name, 'wb') as file:
            file.write(data)
        print(f"Data for stream {i} saved to {file_name}")

    threads = []
    results = []

    # Function to be executed in each thread
    def thread_function(i, file):
        result = send_stream(i, file)
        results.append((i, result))
        os.remove(file)  # Remove the file after sending

    # Create and start a thread for each stream
    for i, file in enumerate(files):
        thread = threading.Thread(target=thread_function, args=(i, file))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Sort the results by stream_id before printing
    results.sort(key=lambda x: x[0])

    # Printing Statistics
    total_bytes = 0
    total_packets = 0
    total_time = 0
    print("\nStream Statistics:")
    for stream_id, (bytes_sent, packets_sent, elapsed_time) in results:
        # Calculate data rate and packet rate for each stream
        data_rate = bytes_sent / elapsed_time
        packet_rate = packets_sent / elapsed_time
        total_bytes += bytes_sent
        total_packets += packets_sent
        total_time += elapsed_time
        print(f"Stream {stream_id}:")
        print(f"  Bytes sent: {bytes_sent}")
        print(f"  Packets sent: {packets_sent}")
        print(f"  Data rate: {data_rate:.2f} bytes/second")
        print(f"  Packet rate: {packet_rate:.2f} packets/second")

    # Calculate average data rate and packet rate across all streams
    avg_data_rate = total_bytes / total_time
    avg_packet_rate = total_packets / total_time

    print("\nOverall Statistics:")
    print(f"Total bytes sent: {total_bytes}")
    print(f"Total packets sent: {total_packets}")
    print(f"Average data rate: {avg_data_rate:.2f} bytes/second")
    print(f"Average packet rate: {avg_packet_rate:.2f} packets/second")

    # Prepare data for plotting
    stream_ids = []
    data_rates = []
    packet_rates = []

    for stream_id, (bytes_sent, packets_sent, elapsed_time) in results:
        stream_ids.append(stream_id)
        data_rates.append(bytes_sent / elapsed_time)
        packet_rates.append(packets_sent / elapsed_time)

    # Plotting the Data Rate and Packet Rate
    plt.figure(figsize=(14, 6))

    # Data Rate Plot
    plt.subplot(1, 2, 1)
    plt.vlines(stream_ids, 0, data_rates, color='b', linestyle='-', lw=2)  # Vertical lines
    plt.scatter(stream_ids, data_rates, color='b', s=50)  # Dots at the end of the lines
    plt.xlabel('Stream ID')
    plt.ylabel('Data Rate (bytes/second)')
    plt.title('Average Data Rate per Stream')
    plt.grid(True)
    plt.xticks(ticks=stream_ids)  # Ensure all stream IDs are shown

    # Increase number of ticks and grid lines
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(10))  # Y-axis ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(len(stream_ids)))  # X-axis ticks

    # Packet Rate Plot
    plt.subplot(1, 2, 2)
    plt.vlines(stream_ids, 0, packet_rates, color='g', linestyle='-', lw=2)  # Vertical lines
    plt.scatter(stream_ids, packet_rates, color='g', s=50)  # Dots at the end of the lines
    plt.xlabel('Stream ID')
    plt.ylabel('Packet Rate (packets/second)')
    plt.title('Average Packet Rate per Stream')
    plt.grid(True)
    plt.xticks(ticks=stream_ids)  # Ensure all stream IDs are shown

    # Increase number of ticks and grid lines
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(10))  # Y-axis ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(len(stream_ids)))  # X-axis ticks

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
