#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo -e "\033[33m"
    echo "This script must be ran using sudo or as root."
    echo -e "\033[37m"
    exit 1
fi

# Install required Packages
echo -e "\033[92m"
echo "Installing Python3 Pip"
echo -e "\033[37m"
sudo apt install python3-pip -y
echo -e "\033[92m"
echo "Installing GPSD Client (for the GPS Module)"
echo -e "\033[37m"
sudo apt-get install gpsd gpsd-clients -y
echo -e "\033[92m"
echo "Installing Pillow"
echo -e "\033[37m"
python3 -m pip install --upgrade Pillow --break-system-packages
echo -e "\033[92m"
echo "Installing Schedule"
echo -e "\033[37m"
pip install schedule --break-system-packages
echo -e "\033[92m"
echo "Installing Python Dateutil"
echo -e "\033[37m"
pip install python-dateutil --break-system-packages
echo -e "\033[92m"
echo "Installing gps3"
echo -e "\033[37m"
sudo -H pip3 install gps3 --break-system-packages

echo -e "\033[92m"
echo "Setting up Serial and SPI Ports"
echo -e "\033[37m"

# Set up Serial and SPI Communication
sudo raspi-config nonint do_serial_hw 1 
sudo raspi-config nonint do_serial_cons 1
sudo raspi-config nonint do_spi 0

echo -e "\033[92m"
echo "Stoping existing PRDS-ADSB service"
echo -e "\033[37m"

# Remove existing PRDS-ADSB Installation:
sudo systemctl stop PRDS-ADSB.service
sudo systemctl disable PRDS-ADSB.service

echo -e "\033[92m"
echo "Creating PRDS/ADSB directory"
echo -e "\033[37m"

cd /etc/systemd/system
sudo rm -r PRDS-ADSB.service

cd /home/pi
sudo rm -r PRDS

echo -e "\033[92m"
echo "Getting the PRD Software from Github"
echo -e "\033[37m"

# Get new PRDS from Github:
cd /home/pi
git clone --depth 1 --no-checkout https://github.com/JN-Husch/Portable-Receiver-Display.git PRDS
cd PRDS
git sparse-checkout set ADSB
git checkout
cd ADSB

echo -e "\033[92m"
echo "Setting up the PRDS-ADSB.service"
echo -e "\033[37m"

# Set up PRDS-ADSB for automatic start on Pi boot
sudo cp /home/pi/PRDS/ADSB/PRDS-ADSB.service /etc/systemd/system
sudo systemctl enable PRDS-ADSB.service
sudo systemctl start PRDS-ADSB.service

echo -e "\033[92m"
echo "------------------------------------------------"
echo "Installation complete!"
echo -e "\033[37m"
echo "Please re-boot the Pi by running sudo reboot"

