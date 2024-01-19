## Manual Software Installation

1. Connect to your Pi via SSH and run the following commands:

   1.1 Installation of Pip:
   
		sudo apt install python3-pip -y

   1.2 Installation of PIL
   
		python3 -m pip install --upgrade Pillow

   1.3 Installation of Schedule
 
		pip install schedule

   1.4 Installation of Dateutil
 
		pip install python-dateutil

</br>

2. Enable SPI communication for the E-Ink display

   2.1 Run the following command on your Pi:
   
		sudo raspi-config

   2.2 Navigate to:
   
		Interfacing Options -> SPI

   2.3 Select Yes Enable SPI Interface

   2.4 Select Finish

</br>

3. Reboot your Pi by running:

		sudo reboot

</br>

4. Copy the contents of the ADSB folder to your Pi, by running the following 6 commands:

		cd /home/pi
		git clone --depth 1 --no-checkout https://github.com/JN-Husch/Portable-Receiver-Display.git PRDS
		cd PRDS
		git sparse-checkout set ADSB
		git checkout
		cd ADSB

</br>

5. You can now test your setup, by starting the PRD Software manually:

  		python3 main.py

	By pressing "Left Ctrl + C" several times, you can exit from the Portable Receiver Display Software.

</br>

6. To automatically start the PRD Software on Pi boot, follow these three steps:

		sudo cp /home/pi/PRDS/ADSB/PRDS-ADSB.service /etc/systemd/system
		sudo systemctl enable PRDS-ADSB.service
		sudo systemctl start PRDS-ADSB.service
