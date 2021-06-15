import datetime

def typeFloatSafety(element):
    return ((type(element) is str) or (type(element) is int)) and (element != '')

def calculateEndTime(startTime, durationHour):
    return startTime + datetime.timedelta(seconds=3600*durationHour)
