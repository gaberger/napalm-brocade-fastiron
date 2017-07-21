Value Required OSVersion (\S+\.\S+\.\S+) 
Value Required Model (\S+)
Value Required Serial_Number (\S+)
Value Day (\d+)
Value Hour (\d+)
Value Minute (\d+)
Value Second (\d+)

Start
  ^\s+SW: Version ${OSVersion}
  ^\s+HW: Stackable ${Model}
  ^\s+Serial  #:${Serial_Number}
  ^STACKID 1  system uptime is ${Day} day\(s\) ${Hour} hour\(s\) ${Minute} minute\(s\) ${Second} second\(s\)
