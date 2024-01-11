from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print(data_stream.TPV)
        print('Altitude = ', data_stream.TPV['alt'])
        print('Latitude = ', data_stream.TPV['lat'])
        print('Time = ', data_stream.TPV['time'])
        
