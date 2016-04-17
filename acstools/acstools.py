from sense_hat import SenseHat
from datetime import datetime as dt
import gps

class acspacket():
    def __init__(self, sense, gpsrec):
	gpsrec.next()
        self.time = dt.now()
	self.gpstime = gpsrec.fix.time
        self.latitude = gpsrec.fix.latitude
        self.longitude = gpsrec.fix.longitude
        self.altitude = gpsrec.fix.altitude
	self.humidity = sense.get_humidity()
	self.pressure = sense.get_pressure()
        self.temperature = sense.get_temperature()
        self.compass = sense.get_compass_raw()
        self.gyroscope = sense.get_gyroscope_raw()
        self.accelerometer = sense.get_accelerometer_raw()
