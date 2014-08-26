import sys
import ac
import acsys
import time
sys.path.insert(len(sys.path), 'apps/python/odometer/third_party')
from sim_info import info

# Hardcoded for now. However, data is available in /content/tracks/<name>/ui/ui_track.json
tracklength = {'imola': 4.909,
               'magione': 2.507,
               'monza': 5.793,
               'monza66': 5.793,
               'mugello': 5.245,
               'nurburgring': 5.148,
               'silverstone': 5.901,
               'silverstone-international': 3.619,
               'vallelunga': 4.085,
               'vallelunga-club': 1.746}

appWindow = 0
tick = 0
trackname = 0
l_lapcount = 0
l_distance = 0
l_fuel = 0
lapcount = 0
distance = 0
in_tank=0   # Hackity hack
fuel=0

def acMain(ac_version):
    global appWindow, trackname, tracklength, l_lapcount, l_distance, l_fuel

    appWindow = ac.newApp("acOdometer")
    ac.setSize(appWindow, 142, 142)

    l_lapcount = ac.addLabel(appWindow, "Laps: Outlap")
    ac.setPosition(l_lapcount, 3, 30)
    l_distance = ac.addLabel(appWindow, "Kilometers: Outlap")
    ac.setPosition(l_distance, 3, 45)
    l_fuel = ac.addLabel(appWindow, "Fuel used: 0")
    ac.setPosition(l_fuel, 3, 60)

    trackname = ac.getTrackName(0)
    ac.log("*************************** NEW SESSION\n********* " + trackname)
    ac.log("acOdometer loaded, racing {} which has {:.3f} miles per lap".format(trackname, tracklength[trackname]))
    ac.console("acOdometer loaded, racing {} which has {:.3f} kilometers per lap.".format(trackname, tracklength[trackname]))
    return "acOdometer"

def acUpdate(deltaT):
    global tick, trackname, lapcount, l_lapcount, l_distance, l_fuel, distance, in_tank, fuel
    tick += 1

    # info.physics.fuel is 0 until the outlap begins
    if in_tank == 0:
        in_tank = info.physics.fuel

    current_tank = info.physics.fuel
    difference = in_tank - round(current_tank, 2)
    if difference > 0.01:
        in_tank = current_tank
        fuel += difference
        ac.setText(l_fuel, "Fuel used: {:.3f}".format(fuel))

    laps = ac.getCarState(0, acsys.CS.LapCount)
    if laps > lapcount:
        lapcount = laps
        distance += tracklength[trackname]
        ac.log("{} laps of {}. That's {:.3f} kilometers this session".format(lapcount, trackname, distance))
        ac.console("{} laps of {}. That's {:.3f} kilometers this session".format(lapcount, trackname, distance))
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))
        ac.setText(l_distance, "Kilometers: {:.3f}".format(distance))

def acShutdown():
    global distance
    ac.log("Drove {:.3f} kilometers using {:.3f} liters of fuel.".format(distance, fuel))
    ac.log("*************************** END SESSION")

