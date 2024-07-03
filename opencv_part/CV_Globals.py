from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

capture=False
timepath=""
timepathlist=[]
year=2024
month=1
day=1
hour=1
minute=1
second=1
def getTimePath():
    global timepath
    global year
    global month



def set_capture_val(a):
    global capture
    capture=a

def set_timepath_val(b):
    global timepath
    timepath=b

def get_capture_val():
    global capture
    return capture

def get_timepath_val():
    global timepath
    print("timepath=",timepath)
    return timepath

def get_timepathlist_val():
    global timepathlist
    return timepathlist

def set_timepathlist_val(list):
    global timepathlist
    timepathlist=list