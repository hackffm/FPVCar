import serial.tools.list_ports

print('search used serial ports')
ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print('no used ports found')
for p in ports:
    print('thing is ' + p.description + ' on port ' + p.device)

