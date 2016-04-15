from sense_hat import SenseHat
from datetime import datetime as dt

class acspacket():
    def __init__(self, sense):
        self.time = dt.now()
        self.humidity = sense.get_humidity()
        self.pressure = sense.get_pressure()
        self.temperature1 = sense.get_temperature()
        self.temperature2 = sense.get_temperature_from_pressure()
        self.compass = sense.get_compass_raw()
        self.gyroscope = sense.get_gyroscope_raw()
        self.accelerometer = sense.get_accelerometer_raw()
