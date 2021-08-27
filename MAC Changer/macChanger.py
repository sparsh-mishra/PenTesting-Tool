import subprocess


def macChanger():
    subprocess.call(["ifconfig"])
    interface = input('Interface name: ')
    macAdd = input("MAC Address: ")

    print("\n [+] Changing MAC Address of interface "+interface+" to: "+macAdd + "\n")

    try:
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", macAdd])
        subprocess.call(["ifconfig", interface, "up"])
    except:
        print("please enter valid details")

    subprocess.call(["ifconfig"])

macChanger()
