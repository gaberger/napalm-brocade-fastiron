Value Interface (\S+)
Value Admin (\S+)
Value Oper (\S+)
Value LinkLocal (\S+)
Value Speed (\S+)
Value Description (.*)
Value Day (\d+)
Value Hour (\S+)
Value Minute (\d+)
Value Second (\d+)


Start
  ^${Interface} is ${Admin}, line protocol is ${Oper}
  ^ \s+Port (\S+) for ${Day} day\(s\) ${Hour} hour\(s\) ${Minute} minute\(s\) ${Second} second\(s\)
  ^ \s+Hardware is (\S+), address is ${LinkLocal}
  ^ \s+Configured speed (\S+), actual ${Speed}, configured duplex (\S+), actual (\S+)
  ^ \s+Port name is ${Description} 
  ^UC Egress queues:
  ^MC Egress queues:
  ^Queue counters    Queued packets    Dropped Packets -> Record
