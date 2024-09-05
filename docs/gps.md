## GPS

To use a GPS module, you have to follow these steps:

1. Connect to your Pi via SSH.

</br>

2. Enable the Serial Interface:

    2.1 Run the following command on your Pi:
   
	    sudo raspi-config
  
    2.2 Navigate to:
   
	    Interfacing Options -> Serial

    2.3 Select "No" when asked to allow the "login shell" via serial

    2.4 Select "Yes" when asked to enable the serial port hardware

</br>

3. Install the gpsd client (this talks to the GPS):

        sudo apt-get install gpsd gpsd-clients -y

</br>

4. Set up the gpsd client to listen on Serial Port 0:

   4.1 Open the gpsd configuration with a text-editor:

       sudo nano /etc/default/gpsd

   4.2 Edit the line "DEVICES" to look like this:

        DEVICES="/dev/ttyAMA0"

    (Note: If you are using a different GPS (for example a USB dongle), make sure to set the correct port here)

   4.3 Save the file and close the editor (Ctrl + X)

</br>

5. On some Pis the Bluetooth module uses the same serial port as the GPS, therfore it needs to be disabled:

    5.1 Open the /boot/config.txt with a text-editor:

       sudo nano /boot/config.txt

   5.2 At the bottom of the file, add the following line:

       dtoverlay=disable-bt

   5.3 Save the file and close the editor (Ctrl + X)

</br>

6. Reboot the Pi for the changes to have an effect

</br>

7. Connect to your device via SSH again.

</br>

8. Test your GPS by running the following command:

        cgps -s

   The interface should show basic GPS information, like time, 3D position and received satellites. 

</br>

10. Install the Python GPS interfacing software:
   
		sudo -H pip3 install gps3 --break-system-packages

</br>

11. To enable the GPS position on TAR1090 and GRAPHS1090 (if installed), add the stream to the readsb configuration file:

	11.1 Open the readsb configuration file with the text editor:
		
  		sudo nano /etc/default/readsb

	11.2 Find the following line:

      		NET_OPTIONS="--net ......"

	11.3 At the end, ahead of the ending ", add the following:

  		--net-connector localhost,2947,gpsd_in
      		
	11.4 Save the file and close the editor (Ctrl + X)

 	11.5 Reboot one final time.

</br>

All done!
