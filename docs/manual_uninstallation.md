## Manual Software Uninstallation

To stop and remove the PRD Software, follow these steps:

1. Connect to your Pi via SSH, and run the following commands.

2. Stop & Disable the PRDS-ADSB.service:

   		sudo systemctl stop PRDS-ADSB.service
   		sudo systemctl disable PRDS-ADSB.service

3. Remove the PRDS-ADSB.service file:

		cd /etc/systemd/system
   		sudo rm -r PRDS-ADSB.service

5. Remove the installation files:

  		cd /home/pi
   		sudo rm -r PRDS
