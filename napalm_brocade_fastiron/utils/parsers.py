import textfsm  
from utils import read_txt_file, convert_uptime
import re
  
def parse_get_facts(text):
    tplt = read_txt_file("napalm_brocade_fastiron/utils/textfsm_templates/fastiron_show_version.template")
    t = textfsm.TextFSM(tplt)
    result = t.ParseText(text)
    if result is not None:
        (os_version, model, serial_no, day, hour, minute, second) = result[0]
        uptime = int(convert_uptime(day, hour, minute, second))
        return {"os_version": os_version, "model": model, "serial_no": serial_no, "uptime": uptime}
    else:
        raise ValueError("show_version parser failed")

