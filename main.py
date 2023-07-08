import fcntl, struct, subprocess, json, nmap, socket, os, ctypes, requests, time
import kivy
from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_garden.qrcode import QRCodeWidget
from kivy.uix.widget import Widget
from ipgetter2 import ipgetter1 as ipgetter #Now use IPGetter2 Direct replacement library
from threading import Thread
from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


def decode_flags(flags):
    flag_mapping = {
        0x1: "\nUp",
        0x2: "\nBroadcast",
        0x4: "\nMulticast",
        0x8: "\nLoopback",
        0x10: "\nLower Up",
        0x20: "\nNo ARP",
        0x40: "\nPromiscuous",
        0x80: "\nAll Multicast",
        0x100: "\nDynamically Assigned",
        0x200: "\nMaster",
        0x400: "\nSlave"
    }
    decoded_flags = []
    for flag, description in flag_mapping.items():
        if flags & flag:
            decoded_flags.append(description)
    return decoded_flags

def get_network_speed(interface):
    try:
        cmd = f"cat /sys/class/net/{interface}/speed"
        speed = subprocess.check_output(cmd, shell=True).decode().strip()
        return f"{interface}: {speed} Mbps"
    except subprocess.CalledProcessError:
        return f"Interface '{interface}' not found."

def get_mac_address(interface):
    try:
        cmd = f"cat /sys/class/net/{interface}/address"
        mac_address = subprocess.check_output(cmd, shell=True).decode().strip()
        return f"{interface}: {mac_address}"
    except subprocess.CalledProcessError:
        return f"Interface '{interface}' not found."

def get_interface_flags(interface):
    try:
        cmd = f"cat /sys/class/net/{interface}/flags"
        flags = int(subprocess.check_output(cmd, shell=True).decode().strip(), 16)
        decoded_flags = decode_flags(flags)
        return f"{', '.join(decoded_flags)}"
    except subprocess.CalledProcessError:
        return f"Interface '{interface}' not found."



def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])

class SpeedtestButton(Button):
    pass


class NetworkButton(Button):
    pass

class ExitButton(Button):
    pass

class ScanButton(Button):
    pass


class Container(GridLayout):
    display = ObjectProperty()
    
    def scan(self, btn):
        text = ''
        scanner = nmap.PortScanner()
        scanner.scan("192.168.50.0/24", arguments="-sS")
        for host in scanner.all_hosts():
            #text = text + "\n" + f"host is {host} {scanner[host].state()}"
            if scanner[host].hostname():
                text = text + '\n' + f"{host} {scanner[host].hostname()}"
            try:
                #text = text + '\n' + f"{host} {scanner[host]['addresses']['mac']}"
                if "vendor" in scanner[host]:
                    text = text + '\n' + f"{host} {scanner[host]['vendor'][scanner[host]['addresses']['mac']]}"
            except KeyError:
                pass
        print(text)
        self.display.text = text
        #btn.visible = True
        pass

    def scan4pi(self, btn):
        btn.visible = False
        #self.display.text = "Coming Soon!"


    def please_wait(self):
        self.display.text = "Speed Test running\nPlease wait a moment"
    
    def speed_test(self, btn):
        stdoutdata = subprocess.getoutput("./speedtest -f json")
        try:
            results = json.loads(stdoutdata)
        except ValueError:
            pass

        download_result = results["download"]["bandwidth"]
        upload_result = results["upload"]["bandwidth"]
        download_result = str(round(download_result / 125000, 2))
        upload_result = str(round(upload_result / 125000, 2))
        ping_result = results["ping"]["high"]
        ping = str(round(ping_result, 0))
        your_isp = results["isp"]
        share_link = results["result"]["url"]
        self.display.text = "Download Speed: " + download_result + "Mbs\nUpload Speed: " + upload_result + "Mbs\nPing: " + ping + "ms\nYour ISP: " + your_isp
        btn.visible = True
        btn.data = share_link

    def show_allips(self, btn):
        btn.visible = False
        myip = ipgetter.myip()
        lines = ''
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            for ifname in interfaces:
                try:
                    if ("eth" in ifname):
                        cmd = "sudo ethtool "+ifname+" |grep -i speed"
                        re = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
                        res = re.stdout.decode('utf-8').strip()
                        ips = get_interface_ip(ifname)
                        lines = lines + ifname +": " + ips + "\nLink " + res+"\n"
                    else:
                       res =""
                       ips = get_interface_ip(ifname)
                       lines = lines + ifname +": " + ips +"\n"
                except IOError:
                    pass
        lines1 = []
        output = subprocess.check_output("ip link show", shell=True).decode()
        lines1 = output.strip().split("\n")
        interfaces = []
        for stuff in lines1:
            if "UP" in stuff and "LOOPBACK" not in stuff:
                interface = stuff.split(":")[1].strip()
                if not interface.startswith("veth"):
                    interfaces.append(interface)

       # Process each network interface
        for interface_name in interfaces:
            speed_info = get_network_speed(interface_name)
            mac_address_info = get_mac_address(interface_name)
            flags_info = get_interface_flags(interface_name)

        self.display.text = lines + "\nExternal IP: " + myip + "\nMAC: " + mac_address_info + "\nConnection Flags:\n " + flags_info
        #btn.data = lines + "\nExternal IP: " + myip
        #btn.visible = True

class MainApp(App):

    def build(self):
        self.title = 'Netapp-Touch'
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
