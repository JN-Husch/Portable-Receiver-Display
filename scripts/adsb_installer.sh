#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo -e "\033[33m"
    echo "This script must be ran using sudo or as root."
    echo -e "\033[37m"
    exit 1
fi

# Install required Packages
sudo apt install python3-pip
python3 -m pip install --upgrade Pillow --break-system-packages
pip install schedule --break-system-packages
pip install python-dateutil --break-system-packages
sudo -H pip3 install gps3 --break-system-packages

# Set up Serial and SPI Communication
sudo raspi-config nonint do_serial_hw 1 
sudo raspi-config nonint do_serial_cons 1
sudo raspi-config nonint do_serial 2
sudo raspi-config nonint do_spi 0

# Remove existing PRDS-ADSB Installation:
sudo systemctl stop PRDS-ADSB.service
sudo systemctl disable PRDS-ADSB.service

cd /etc/systemd/system
sudo rm -r PRDS-ADSB.service

cd /home/pi
sudo rm -r PRDS

# Get new PRDS from Github:
cd /home/pi
git clone --depth 1 --no-checkout https://github.com/JN-Husch/Portable-Receiver-Display.git PRDS
cd PRDS
git sparse-checkout set ADSB
git checkout
cd ADSB

# Set up PRDS-ADSB for automatic start on Pi boot
sudo cp /home/pi/PRDS/ADSB/PRDS-ADSB.service /etc/systemd/system
sudo systemctl enable PRDS-ADSB.service
sudo systemctl start PRDS-ADSB.service

