## Solar eclipse data logger 
# Dr. Clark Hochgraf
# Eclipse date: April 8, 2024
''' 
Overview: measures current reading from a BK Precision 8502B electronic load.
Measurement is in units of amps and timestamped with UTC time.

Requirements:
1) USB adapter to RS-232 at 9600 Baud 8N1
2) 8502B must set the protocol as "SCPI", not "frame"
3) Configure 8502B as constant current mode. Set current to max (12 amps)
'''
