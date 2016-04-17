from sense_hat import SenseHat
import curses
import math
from datetime import datetime as dt
from multiprocessing import Process
import gps

from acstools import acstools as acs

LABCOL = 3
DATCOL = 23
DATCOL2 = 33
DATCOL3 = 43
UNITCOL = 33

LABCOL2 = 53
DATACOL4 = 63

def update_data(lasttime):
    acsdata = acs.acspacket(sense, gpsrec)
    scr.addstr(2,DATCOL,str(acsdata.time))
    delay = (acsdata.time - lasttime).total_seconds()
    if delay >= .1:
        color = 5
    elif delay >= .08:
        color = 4
    else:
        color = 3
    scr.addstr(3,DATCOL,str(delay),curses.color_pair(color))
    scr.addstr(4,DATCOL,str(acsdata.gpstime))
    scr.addstr(5,DATCOL,str(acsdata.latitude))
    scr.addstr(6,DATCOL,str(acsdata.longitude))
    scr.addstr(7,DATCOL,str(acsdata.latitude))
    scr.addnstr(8,DATCOL,str(acsdata.humidity),8)
    scr.addnstr(9,DATCOL,str(acsdata.pressure),8)
    scr.addnstr(10,DATCOL,str(acsdata.temperature),8)
    scr.addnstr(11,DATCOL,str(acsdata.compass['x']),8)
    scr.addnstr(11,DATCOL2,str(acsdata.compass['y']),8)
    scr.addnstr(11,DATCOL3,str(acsdata.compass['z']),8)
    scr.addnstr(12,DATCOL,str(acsdata.gyroscope['x']),8)
    scr.addnstr(12,DATCOL2,str(acsdata.gyroscope['y']),8)
    scr.addnstr(12,DATCOL3,str(acsdata.gyroscope['z']),8)
    scr.addnstr(13,DATCOL,str(acsdata.accelerometer['x']),8)
    scr.addnstr(13,DATCOL2,str(acsdata.accelerometer['y']),8)
    scr.addnstr(13,DATCOL3,str(acsdata.accelerometer['z']),8)
    accelmag = math.sqrt(acsdata.accelerometer['x']**2 + acsdata.accelerometer['y']**2 + acsdata.accelerometer['z']**2)
    if accelmag > 3:
        color = 5
    elif accelmag > 2:
	color = 4
    else:
        color = 3
    scr.addnstr(13,DATACOL4,str(accelmag),8,curses.color_pair(color))
    curses.curs_set(0)
    scr.refresh()

    return acsdata.time

def update_leds():
    time = dt.now()
    secs = time.second + time.microsecond / 1000000.
    mod = 0.5 + (math.sin((secs % 3) * math.pi / 1.5) / 2)

    X = [0,0,int(255*(1-mod))]
    O = [int(255*mod),int(255*mod),int(255*mod)]

    img = [
        O,O,O,O,O,O,O,O,
        O,O,X,O,O,X,O,O,
        O,O,X,O,X,O,O,O,
        O,O,X,X,O,O,O,O,
        O,O,X,X,O,O,O,O,
        O,O,X,O,X,O,O,O,
        O,O,X,O,O,X,O,O,
        O,O,O,O,O,O,O,O,
        ]

    sense.set_pixels(img)



sense = SenseHat()
sense.clear()
gpsrec = gps.gps(mode=gps.WATCH_ENABLE)

scr = curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_YELLOW, curses.COLOR_BLUE)
curses.init_pair(2,curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(5,curses.COLOR_BLACK, curses.COLOR_RED)
scr.attron(curses.color_pair(1))
scr.border('|','|','-','-','+','+','+','+')
scr.attroff(curses.color_pair(1))

try:
    scr.addstr(2,LABCOL,"Time:",curses.color_pair(2))
    scr.addstr(3,LABCOL,"Delay:",curses.color_pair(2))
    scr.addstr(3,UNITCOL,"sec",curses.color_pair(2))
    scr.addstr(4,LABCOL,"GPS Time:", curses.color_pair(2))
    scr.addstr(5,LABCOL,"Latitude:", curses.color_pair(2))
    scr.addstr(6,LABCOL,"Longitude:", curses.color_pair(2))
    scr.addstr(7,LABCOL,"Altitude:", curses.color_pair(2))
    scr.addstr(8,LABCOL,"Humidity:",curses.color_pair(2))
    scr.addstr(8,UNITCOL,"%",curses.color_pair(2))
    scr.addstr(9,LABCOL,"Pressure:",curses.color_pair(2))
    scr.addstr(9,UNITCOL,"mBar",curses.color_pair(2))
    scr.addstr(10,LABCOL,"Temperature:",curses.color_pair(2))
    scr.addstr(10,UNITCOL,"C",curses.color_pair(2))
    scr.addstr(11,LABCOL,"Compass Raw:",curses.color_pair(2))
    scr.addstr(12,LABCOL,"Gyro Raw:",curses.color_pair(2))
    scr.addstr(13,LABCOL,"Accel Raw:",curses.color_pair(2))
    scr.addstr(13,LABCOL2,"Magn.:",curses.color_pair(2))

    lasttime = dt.now()
    starttime = lasttime
    while ((lasttime - starttime).seconds < 30):
        lasttime = update_data(lasttime)
        update_leds()
        #sense.show_message(str(i))
        #sleep(.500)

except Exception as e:
    print e.__doc__
    print e.message
    sense.clear()
    scr.clear()
    scr.refresh()
    curses.endwin()

sense.clear()
scr.clear()
scr.refresh()
curses.endwin()
