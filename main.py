import fcntl
import struct
import kivy
#from kivy.config import Config
#Config.set("graphics", "fullscreen", "auto")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.garden.qrcode import QRCodeWidget
from kivy.uix.widget import Widget
import socket, os, ctypes, requests, time #remove IPGEtter
from ipgetter2 import ipgetter1 as ipgetter #Now use IPGetter2 Direct replacement library
from threading import Thread
import subprocess, json

from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


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
        btn.visible = False
        pass

    def scan4pi(self, btn):
        btn.visible = False
        self.display.text = "Coming Soon!"


    def please_wait(self):
        
        self.display.text = "Speed Test running\nPlease wait a moment"
    
    def speed_test(self, btn):
        stdoutdata = subprocess.getoutput("speedtest -f json")
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
        myip = ipgetter.myip()
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            for ifname in interfaces:
                try:
                    ip = get_interface_ip(ifname)
                    btn.data = "Internal IP: " + ip +"\nExternal IP: " + myip
                    btn.visible = True
                    self.display.text = "Internal IP: " + ip +"\nExternal IP: " + myip
                except IOError:
                    pass

class MainApp(App):

    def build(self):
        self.title = 'Netapp-Touch'
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
