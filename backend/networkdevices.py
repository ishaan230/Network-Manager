from scapy.all import ARP, Ether, srp

def arp_scan(ip):
    ipsmacss = "<b>Ip Address &nbsp &nbsp Mac Addresses</b><br><br>"
    arp_request = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout=3, verbose=0)[0]
    for sent, received in result:
        ipsmacss += f"{received.psrc}&nbsp &nbsp {received.hwsrc}<br> "    
    return ipsmacss

def detect_devices():
    print("Starting...")
    ipsmacs = arp_scan("192.168.1.0/24")
    return ipsmacs

# a = detect_devices()
# print(a)
