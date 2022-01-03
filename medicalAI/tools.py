import pickle
from datetime import datetime
import time



def createNewPickleFile(name, type):
    pickle_in = open(f'{name}.pickle', 'wb')

    variable = type

    pickle_out = open(f'{name}.pickle', 'wb')
    pickle.dump(variable, pickle_out)
    pickle_out.close()


def openPickleFile(name):
    pickle_in = open(f'{name}.pickle', 'rb')
    variable = pickle.load(pickle_in)

    return variable


def savePickleFile(name, variable):
    pickle_out = open(f'{name}.pickle', 'wb')
    pickle.dump(variable, pickle_out)
    pickle_out.close()



def startTime():
    timeRough = datetime.today()
    startMicros = timeRough.microsecond
    startSeconds = timeRough.second
    startMinutes = timeRough.minute
    startHours = timeRough.hour

    return startMicros, startSeconds, startMinutes, startHours


def endTime():
    timeRough = datetime.today()
    endMicros = timeRough.microsecond
    endSeconds = timeRough.second
    endMinutes = timeRough.minute
    endHours = timeRough.hour

    return endMicros, endSeconds, endMinutes, endHours

def elapsedTime(start, end):
    sMic = start[0]
    sSec = start[1]
    sMin = start[2]
    sH = start[3]

    eMic = end[0]
    eSec = end[1]
    eMin = end[2]
    eH = end[3]

    if eH > sH or eH == sH:
        hours = eH - sH
    else:
        hours = 24 - (sH - eH)

    if eMin > sMin or eMin == sMin:
        minutes = eMin - sMin
    else:
        hours -= 1
        minutes = 60 - (sMin - eMin)

    if eSec > sSec or eSec == sSec:
        seconds = eSec - sSec
    else:
        minutes -= 1
        seconds = 60 - (sSec - eSec)

    if eMic > sMic or eMic == sMic:
        micros = eMic - sMic
    else:
        seconds -= 1
        micros = 100 - (sMic - eMic)

    return hours, minutes, seconds, micros