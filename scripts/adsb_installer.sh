#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo -e "\033[33m"
    echo "This script must be ran using sudo or as root."
    echo -e "\033[37m"
    exit 1
fi



echo -e "\033[92m"
echo "Stoping existing PRDS-ADSB service"
echo -e "\033[37m"

# Remove existing PRDS-ADSB Installation:
sudo systemctl stop PRDS-ADSB.service
sudo systemctl disable PRDS-ADSB.service

cd /etc/systemd/system
sudo rm -r PRDS-ADSB.service

cd /home/pi
sudo rm -r PRDS


# Install required Packages
echo -e "\033[92m"
echo "Installing Python3 Pip"
echo -e "\033[37m"
sudo apt install python3-pip -y
#echo -e "\033[92m"
#echo "Installing GPSD Client (for the GPS Module)"
#echo -e "\033[37m"
#sudo apt-get install gpsd gpsd-clients -y

# Create PRDS directory
echo -e "\033[92m"
echo "Creating PRDS/ADSB directory"
echo -e "\033[37m"

cd /home/pi
mkdir PRDS
cd /home/pi/PRDS

# Install VENV
echo -e "\033[92m"
echo "Setting up VENV"
echo -e "\033[37m"

sudo python3 -m venv .venv
source .venv/bin/activate

echo -e "\033[92m"
echo "Installing Pillow"
echo -e "\033[37m"
python3 -m pip install --upgrade Pillow

echo -e "\033[92m"
echo "Installing Schedule"
echo -e "\033[37m"
pip install schedule

echo -e "\033[92m"
echo "Installing Python Dateutil"
echo -e "\033[37m"
pip install python-dateutil

#echo -e "\033[92m"
#echo "Installing gps3"
#echo -e "\033[37m"
#sudo -H pip3 install gps3

echo -e "\033[92m"
echo "Setting up SPI Communication"
echo -e "\033[37m"

# Set up SPI Communication
sudo raspi-config nonint do_spi 0




echo -e "\033[92m"
echo "Getting the PRD Software from Github"
echo -e "\033[37m"

# Get new PRDS from Github:
cd /home/pi
git clone --depth 1 --no-checkout https://github.com/JN-Husch/Portable-Receiver-Display.git temp
sudo mv temp/.git PRDS/.git
sudo rm -rf temp
cd PRDS
git config --global --add safe.directory /home/pi/PRDS
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
echo "Deactivating VENV"
echo -e "\033[37m"

deactivate

echo -e "\033[92m"
echo "------------------------------------------------"
echo "Installation complete!"
echo -e "\033[37m"
echo "Please re-boot the Pi by running sudo reboot"

