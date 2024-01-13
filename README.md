# Portable Receiver Display Software

Pyhton software for a portable ADS-B (and later VDL2 and ACARS) receiver intended to run on a Raspberry Pi.

![Image of a portable receiver](images/img1.jpeg)

## Hardware Suggestions

The harware below was used for the development build of the portable receiver. Other Hardware might also work...

- Raspberry Pi 3/4/5
- Software Defined Radio (The Nooeelec SDRs fit well into the case)
- Waveshare 2.9inch E-Ink display module (296x128) (https://www.waveshare.com/2.9inch-e-paper-module.htm)
- (optional) GPS Module - Beitian BN-220
- Momentary Toggle Switch (ON)-OFF-(ON), for 6mm hole diameter (https://www.amazon.com/dp/B07PJ577HK?ref_=cm_sw_r_cp_ud_dp_3SB3N0XC1KQG5GVA277V)*
- USB-C Panel Mount (https://www.amazon.com/dp/B0C5D79HXB?ref_=cm_sw_r_cp_ud_dp_ZVZHC8CQEJ09X0SSW703)*
- USB-C to Micro-USB Cable about 30cm long (https://a.co/d/3ogZZP9)*
- USB-A extension about 30cm long (https://www.amazon.com/dp/B08MKW47QD?ref_=cm_sw_r_cp_ud_dp_AZDTF1CSXVHBJWJWEEYY)*
- Power source (either portable battery bank or wallplug) with 5V 2A output.

*The Amazon links are for reference only. Exact product availability and fit may not be guaranteed!


## Wiring Guide

1. Connect the switch and the optional wiring diagramm as shown here:

![Wiring Diagramm](images/wiring.png)
_The GPS receiver is opptional, but highly recommended!_

2. Connect the E-Ink display as explained here: [WaveShare Wiki](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_Manual#Working_With_Raspberry_Pi)

3. Connect the SDR to a free USB port with the USB-A extension cable.

4. Connect the USB-C to Micro-USB cable from the USB-C Panel mount to the Raspberry Pi.


## Software Installation

_Work in Progress, please check again later!_

1. Install Linux Image on Raspberry SD card and boot the Pi.

2. Install readsb + tar1090 on the Pi as explained here: https://github.com/wiedehopf/adsb-scripts/wiki/Automatic-installation-for-readsb
  
3. Connect to your Pi via SSH and run the following commands:
  	3.1 Installation of Pip:
      	```
      	sudo apt install python3-pip
      	```
      
  	3.2 Installation of PIL
     		```
      	python3 -m pip install --upgrade Pillow
      	```
      
  	3.3 Installation of Schedule
      	```
      	pip install schedule
      	```
      
  	3.4 Installation of GPS interfacing software:
      	```
      	sudo -H pip3 install gps3
      	```

4. Enable SPI communication for the E-Ink display:
  	4.1 Run the following command on your Pi:
     	```
     	sudo raspi-config
     	```
     
  	4.2 Navigate to:
     	```
     	Interfacing Options -> SPI
     	```
     
  	4.3 Select Yes Enable SPI Interface
   
  	4.4 Select Finish


6. _(optional)_ Enable Serial communication for the GPS (based on this helpfull guide: https://maker.pro/raspberry-pi/tutorial/how-to-use-a-gps-receiver-with-raspberry-pi-4)
  	5.1 Run the following command on your Pi:
     	```
     	sudo raspi-config
     	```

  	5.2 Navigate to:
     	```
     	Interfacing Options -> Serial
     	```
     
  	5.3 Select Yes Enable Serial Interface
   
  	5.4 Select No if you get asked if you want to allow access to the login-shell via serial connection
   
  	5.5 Select Yes again if you get asked if you want to keep the Serial Interface enabled
   
  	5.6 Select Finish


8. Reboot your Pi by running:
	    ```
     	sudo reboot
     	```
     