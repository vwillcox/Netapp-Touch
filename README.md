## Updated 2023
Updated to use the official Speedtest.net CLI.

Please check https://www.speedtest.net/apps/cli for information on installing this version.
You will need to run it once manaully to agree to their Terms and conditions

Network information now shows ALL connected interfaces (Wi-Fi, Wired etc) and displays them all!

# Update September 2019
I had been using the "IPGetter" python library. This has vanished. Thankfully there is a new library called "IPGetter2" and it has a compatiblity mode. So I have updated the code to use this

# Netapp-Touch
Test your networks speed, connectivity, wifi and find what's connected. This project uses KIVY and KIVY KITCHEN code to create a
touch screen interface and QR Codes for quick information transfer to mobile devices.

It also provides information about the Raspberry-Pi's network connection (Internal IP and External IP), with a QR-CODE to quick copy
the information to a mobile device.
#
![NEW Example running on a HyperPixel 4.0 Touch](https://talktech.info/wp-content/uploads/2020/04/2020-04-26-205928_800x480_scrot-1.png)

An example of Netapp-Touch running on a HyperPixel 4.0 Touch
Created by Vincent Willcox AKA TalkTech

# Prerequisite 
- sudo pip3 install Cython
- sudo pip3 install Kivy
- sudo pip3 install ethtool
- sudo pip3 install ipgetter2
- sudo pip3 install kivy-garden.qrcode

# Running
- python3 main.py
