## Manual Software Installation

1. Connect to your Pi via SSH and run the following commands:

   1.1 Installation of Pip:
   
		sudo apt install python3-pip

   1.2 Installation of PIL
   
		python3 -m pip install --upgrade Pillow

   1.3 Installation of Schedule
 
		pip install schedule

   1.4 Installation of Dateutil
 
		pip install python-dateutil

   1.5 Installation of GPS interfacing software (optional):
   
		sudo -H pip3 install gps3


2. Enable SPI communication for the E-Ink display

   2.1 Run the following command on your Pi:
   
		sudo raspi-config

   2.2 Navigate to:
   
		Interfacing Options -> SPI

   2.3 Select Yes Enable SPI Interface

   2.4 Select Finish



3. _(optional if usinga GPS module:)_ Enable Serial communication for the GPS (based on this helpfull guide: https://maker.pro/raspberry-pi/tutorial/how-to-use-a-gps-receiver-with-raspberry-pi-4)

   3.1 Run the following command on your Pi:
   
		sudo raspi-config

   3.2 Navigate to:
   
		Interfacing Options -> Serial

   3.3 Select Yes Enable Serial Interface

   3.4 Select No if you get asked if you want to allow access to the login-shell via serial connection

   3.5 Select Yes again if you get asked if you want to keep the Serial Interface enabled

   3.6 Select Finish
