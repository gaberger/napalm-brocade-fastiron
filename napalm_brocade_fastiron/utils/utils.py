import socket
import os

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
    uptime = int(days) * sec_in_day + int(hours) * sec_in_hour + int(minutes) * sec_in_min + int(seconds)
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

def send_command_postprocess(command):
    return command

def send_command(session, command):
    """Wrapper for self.device.send.command().
    If command is a list will iterate through commands until valid command.
    """
    print("DEBUG: Called utils send_command with {} {}".format(session, command))
    try:
        if isinstance(command, list):
            for cmd in command:
                output = session.send_command(cmd)
                # TODO Check exception handling
                if "% Invalid" not in output:
                    break
        else:
            output = session.send_command(command)
        return send_command_postprocess(output)
    except (socket.error, EOFError) as e:
        raise ConnectionClosedException(str(e))