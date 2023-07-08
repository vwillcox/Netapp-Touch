#!/usr/bin/env bash
# Network Testing appliance
# uses KIVY, Speedtest.NET

# Installer Script (run as root/sudo please)

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
  function pause(){
   read -p "$*"
}

echo "Welcome to Netapp-Touch Installer"
pause 'Press [Enter] to install the required bits and pieces or CTRL+C to stop...'

apt update
apt install ethtool
if [ "$?" -ne 0 ]; then
  echo "Error while running apt-get (maybe run apt-get update?)";
  exit 1;
fi
echo "Done"
echo "Now installing python modules"
pip3 install -r requirements.txt
echo "Now downloading and installing and pre-running Speedtest.net"
wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz
tar zxvf ookla-speedtest-1.2.0-linux-aarch64.tgz
chmod +x speedtest
sudo -u $USER ./speedtest
echo "All done! Enjoy"
echo "You just need to run python3 main.py"
