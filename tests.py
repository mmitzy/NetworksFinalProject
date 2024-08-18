import argparse
import subprocess
import time
import constants as const

def runtest(n):
    # Run the reciever
    receiver = subprocess.Popen(["python3", "Server.py"])

    # Run sender with n value
    subprocess.run(["python3", "Client.py", "-t", str(n), "-s", str(delay)])

    # Terminate the receiver
    receiver.terminate()
    receiver.wait()
    time.sleep(const.testingInterval)
    with open("input.txt", "r") as f_random, open("output.txt", "r") as f_output:
        random_data = f_random.read()
        output_data = f_output.read()
        assert abs(len(random_data) - len(output_data)) <= loss


def main():
    arg_parser = argparse.ArgumentParser(description="Receiver for written QUIC packets")
    arg_parser.add_arguement("-d", "--delay", type=float, default=const.defaultDelay, help="Delay in seconds before sending the packets")
    arg_parser.add_arguement("-t", "--threads", type=int, default=const.defaultStreamNumberTester, help="Maximum number of threads to run")
    arg_parser.add_arguement("-l", "--loss", type=int, default=const.defaultLoss, help="Maximum loss in bytes")

    global delay
    delay = arg_parser.parse_args().delay

    global threads
    threads = arg_parser.parse_args().threads

    global loss
    loss = arg_parser.parse_args().loss

    for n in range(1, threads + 1):
        runtest(n)
        print(f"Test {n} passed")

if __name__ == "__main__":
    main()


