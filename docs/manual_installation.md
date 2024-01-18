## Manual Software Installation

1. Connect to your Pi via SSH and run the following commands:

   1.1 Installation of Pip:
   
		sudo apt install python3-pip -y

   1.2 (Optional - Required if you want to use a GPS Module) Installation of gpsd:
   
		sudo apt-get install gpsd gpsd-clients -y

   1.3 Installation of PIL
   
		python3 -m pip install --upgrade Pillow

   1.4 Installation of Schedule
 
		pip install schedule

   1.5 Installation of Dateutil
 
		pip install python-dateutil

   1.6 Installation of GPS interfacing software (optional):
   
		sudo -H pip3 install gps3

</br>

2. Enable SPI communication for the E-Ink display

   2.1 Run the following command on your Pi:
   
		sudo raspi-config

   2.2 Navigate to:
   
		Interfacing Options -> SPI

   2.3 Select Yes Enable SPI Interface

   2.4 Select Finish

</br>

3. _(optional if usinga GPS module:)_ Enable Serial communication for the GPS (based on this helpfull guide: https://maker.pro/raspberry-pi/tutorial/how-to-use-a-gps-receiver-with-raspberry-pi-4)

   3.1 Run the following command on your Pi:
   
		sudo raspi-config

   3.2 Navigate to:
   
		Interfacing Options -> Serial

   3.3 Select Yes Enable Serial Interface

   3.4 Select No if you get asked if you want to allow access to the login-shell via serial connection

   3.5 Select Yes again if you get asked if you want to keep the Serial Interface enabled

   3.6 Select Finish

</br>

4. Reboot your Pi by running:

		sudo reboot

</br>

5. Copy the contents of the ADSB folder to your Pi, by running the following 6 commands:

		cd /home/pi
		git clone --depth 1 --no-checkout https://github.com/JN-Husch/Portable-Receiver-Display.git PRDS
		cd PRDS
		git sparse-checkout set ADSB
		git checkout
		cd ADSB

</br>

6. You can now test your setup, by starting the PRD Software manually:

  		python3 main.py

	By pressing "Left Ctrl + C" several times, you can exit from the Portable Receiver Display Software.

</br>

7. To automatically start the PRD Software on Pi boot, follow these three steps:

		sudo cp /home/pi/PRDS/ADSB/PRDS-ADSB.service /etc/systemd/system
		sudo systemctl enable PRDS-ADSB.service
		sudo systemctl start PRDS-ADSB.service
