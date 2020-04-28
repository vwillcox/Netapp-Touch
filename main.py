import fcntl
import struct
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_garden.qrcode import QRCodeWidget
from kivy.uix.widget import Widget
import socket, os, ctypes, requests, time #remove IPGEtter
from ipgetter2 import ipgetter1 as ipgetter #Now use IPGetter2 Direct replacement library
from threading import Thread
import subprocess, json

import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
os.environ['KIVY_WINDOW'] = 'gl'

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
        results = json.loads(stdoutdata)
        for key in results:
            download = results["download"]["bandwidth"]
            upload = results["upload"]["bandwidth"]
            isp = results["isp"]
            ping = results["ping"]["latency"]
            url = results["result"]["url"]
        down = str(round(download / 125000, 2))
        up =  str(round(upload / 125000, 2))
        ping = str(ping)
        self.display.text = "Download Speed: " + down + "Mbps\nUpload Speed: " + up + "Mbps\nPing: " + ping + "ms\nYour ISP: " + isp
        btn.visible = True
        btn.data = url

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
                    self.display.text = "Internal IP: " + ip +"\nExternal IP: " + myip + "\nInterface: " + ifname
                except IOError:
                    pass

class MainApp(App):

    def build(self):
        self.title = 'Awesome app!!!'
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
