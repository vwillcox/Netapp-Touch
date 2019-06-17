# Netapp-Touch
Test your networks speed, connectivity, wifi and find what's connected. This project uses KIVY and KIVY KITCHEN code to create a
touch screen interface and QR Codes for quick information transfer to mobile devices.

In the initial version, it will test your internet speed using SPEEDTEST-CLI and provide the details on screen, along with a 
QR-CODE of the shareable results.

It also provides information about the Raspberry-Pi's network connection (Internal IP and External IP), with a QR-CODE to quick copy
the information to a mobile device.
#
![Early Example running on a HyperPixel 4.0 Touch](http://talktech.info/wp-content/uploads/2019/06/net-app.jpg)
An Early example of Netapp-Touch running on a HyperPixel 4.0 Touch
Created by Vincent Willcox AKA TalkTech

# Prerequisite 
- sudo pip3 install -U Cython==0.29.9
- sudo pip3 install git+https://github.com/kivy/kivy.git@master
- pip3 install ethtool
- pip3 install speedtest-cli
- garden install qrcode

# Running
- python3 main.py
