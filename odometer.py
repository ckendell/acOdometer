import sys
import ac
import acsys

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
lapcount = 0
distance = 0

def acMain(ac_version):
    global appWindow, trackname, tracklength, l_lapcount, l_distance

    appWindow = ac.newApp("acOdometer")
    ac.setSize(appWindow, 142, 142)

    l_lapcount = ac.addLabel(appWindow, "Laps: Outlap")
    ac.setPosition(l_lapcount, 3, 30)
    l_distance = ac.addLabel(appWindow, "Kilometers: Outlap")
    ac.setPosition(l_distance, 3, 45)

    trackname = ac.getTrackName(0)
    ac.log("*************************** NEW SESSION\n********* " + trackname)
    ac.log("acOdometer loaded, racing {} which has {:.3f} miles per lap".format(trackname, tracklength[trackname]))
    ac.console("acOdometer loaded, racing {} which has {:.3f} kilometers per lap.".format(trackname, tracklength[trackname]))
    return "acOdometer"

def acUpdate(deltaT):
    global tick, trackname, lapcount, l_lapcount, l_distance, distance
    tick += 1

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
    ac.log("Drove {:.3f} kilometers this session.".format(distance))
    ac.log("*************************** END SESSION")

