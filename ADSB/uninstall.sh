#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo -e "\033[33m"
    echo "This script must be ran using sudo or as root."
    echo -e "\033[37m"
    exit 1
fi


# Remove existing PRDS-ADSB Installation:
sudo systemctl stop PRDS-ADSB.service
sudo systemctl disable PRDS-ADSB.service

cd /etc/systemd/system
sudo rm -r PRDS-ADSB.service

cd /home/pi
sudo rm -r PRDS