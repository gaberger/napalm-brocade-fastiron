import socket
import os
import re

def read_txt_file(filename):
    """Read a txt file and return its content."""
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    fullpath = os.path.join(path, filename)
    file =  open(fullpath)
    return file

def convert_uptime(days, hours, minutes, seconds):
    sec_in_day = 86400
    sec_in_hour = 3600
    sec_in_min = 60
    uptime = float(days) * sec_in_day + int(hours) * sec_in_hour + int(minutes) * sec_in_min + int(seconds)
    return uptime

def read_txt_file(filename, test=False):
    """Read a txt file and return its content."""
    if test:
            path = os.path.dirname(os.path.abspath(__file__))
            file = "/".join((path,filename))
    else:
            file = filename
    file =  open(file)
    return file


def convert_speed(speed):
    multiplier = {
        "M" : 1,
        "G" : 1000
        }

    pattern= (r'(\d+)(.)bit')
    m = re.match(pattern, speed)
    if m is not None:
        value = m.group(1)
        mult = m.group(2)
        
        speed = int(value) * int(multiplier[mult])
        return speed