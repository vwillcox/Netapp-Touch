import struct
from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import socket, os, ctypes, requests, time #remove IPGEtter
from ipgetter2 import ipgetter1 as ipgetter #Now use IPGetter2 Direct replacement library
from threading import Thread
import subprocess, json, os, nmap, fcntl


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

class ScrollableBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ScrollableBoxLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Create the left fixed button layout
        button_layout = BoxLayout(orientation='vertical')
        button_layout.add_widget(Button(text='Speed Test', on_release=lambda btn: self.speed_test(btn.text)))
        button_layout.add_widget(Button(text='Network Scanner', on_release=lambda btn: self.network_scan(btn.text)))
        button_layout.add_widget(Button(text='Device Information', on_release=lambda btn: self.device_scan(btn.text)))
        button_layout.add_widget(Button(text='Exit', on_release=lambda btn: self.quitting_time(btn.text)))

        # Create the right scrolling layout
        scroll_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=600)
        scroll_view = ScrollView(do_scroll_x=False)

        self.content_layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        scroll_view.add_widget(self.content_layout)
        scroll_layout.add_widget(scroll_view)

        # Add the left and right layouts to the main layout
        self.add_widget(button_layout)
        self.add_widget(scroll_layout)
        self.scroll_view = scroll_view

    def button_pressed(self, button_text):
        self.content_layout.clear_widgets()
        print(f"Button {button_text} pressed.")

        # Create a new label
        new_label = Label(text=f'Label {len(self.content_layout.children) + 1}',
                          size_hint=(1, None), height=50)
        self.content_layout.add_widget(new_label)
    
    def quitting_time(self, button_text):
        App.get_running_app().stop()
    
    def speed_test(self, button_text):
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

        self.content_layout.clear_widgets();
        download_label = Label(text=f'Download Speed: ' + download_result + 'Mbps',size_hint=(1, None), height=50, halign='left', text_size=(470, None))
        upload_label = Label(text=f'Upload Speed: ' + upload_result +'Mbs',size_hint=(1, None), height=50, halign='left', text_size=(470, None))
        ping_label = Label(text=f'Ping: '+ ping+'ms',size_hint=(1, None), height=50, halign='left', text_size=(470, None))
        self.content_layout.add_widget(download_label)
        self.content_layout.add_widget(upload_label)
        self.content_layout.add_widget(ping_label)
        self.scroll_view.scroll_y=1

    def network_scan(self, button_text):
        self.content_layout.clear_widgets();
        scanner = nmap.PortScanner()
        scanner.scan("192.168.50.0/24", arguments="-sS")
        for host in scanner.all_hosts():
            label = Label(text=f'{host} {scanner[host].state()}', size_hint=(1, None), height=25, halign='left', text_size=(470, None))
            self.content_layout.add_widget(label)
            if scanner[host].hostname():
                label = Label(text=f'{host} {scanner[host].hostname()}', size_hint=(1, None), height=25, halign='left', text_size=(470, None))
                self.content_layout.add_widget(label)
            try:
                label = Label(text=f'{host} {scanner[host]["addresses"]["mac"]}', size_hint=(1, None), height=25, halign='left', text_size=(470, None))
                self.content_layout.add_widget(label)
                if "vendor" in scanner[host]:
                    label = Label(text=f'{host} {scanner[host]["vendor"][scanner[host]["addresses"]["mac"]]}', size_hint=(1, None), height=25, halign='left', text_size=(470, None))
                    self.content_layout.add_widget(label)
            except KeyError:
                pass
        
    def device_scan(self, button_text):
        self.content_layout.clear_widgets();
        myip = ipgetter.myip()
        ip = socket.gethostbyname(socket.gethostname())
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
                        interface_label = Label(text=f''+ifname+": "+ ips, size_hint=(1, None), height=25, halign='left', text_size=(470, None))
                        self.content_layout.add_widget(interface_label)
                        link_speed = Label(text=f'Link'+res, size_hint=(1, None), height=25, halign='left', text_size=(470, None))
                        self.content_layout.add_widget(link_speed)
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
            #speed_info = get_network_speed(interface_name)
            mac_address_info = get_mac_address(interface_name)
            flags_info = get_interface_flags(interface_name)

        #self.display.text = lines + "\nExternal IP: " + myip + "\nMAC: " + mac_address_info + "\nConnection Flags:\n " + flags_info
        external_ip_label = Label(text=f'External IP: '+ myip, size_hint=(1, None), height=25, halign='left', text_size=(470, None))
        self.content_layout.add_widget(external_ip_label)
        mac_address_label = Label(text=f'MAC: '+ mac_address_info, size_hint=(1, None), height=25, halign='left', text_size=(470, None))
        self.content_layout.add_widget(mac_address_label)
        connection_flag_label = Label(text=f'Connection Flags: '+ flags_info, size_hint=(1, None), height=25, halign='left', text_size=(470, None))
        self.content_layout.add_widget(connection_flag_label)
        self.scroll_view.scroll_y=1


class MyApp(App):
    def build(self):
        layout = ScrollableBoxLayout()
        # Set the app to full screen
        # Enable touch mode
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        return layout


if __name__ == '__main__':
    MyApp().run()
