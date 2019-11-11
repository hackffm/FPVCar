import serial
import time

ser = serial.Serial('/dev/ttyS0', 38400)
print(ser.name)


def serial_read():
    print('serial_read')
    data = b''
    for i in range(ser.inWaiting()):
        b = ser.read(1)
        if b != b'\r':
            if b == b'\n':
                print('msg from arduino: ', data)
                print('msg decoded' + data.decode("utf-8"))
                data = b''
            else:
                data += b


if __name__ == '__main__':
    ser.flushInput()

    cmd = "V\r"
    print("fetch: " + cmd)
    ser.write(cmd.encode())
    time.sleep(1)
    serial_read()

    cmd = "v\r"
    print("fetch: " + cmd)
    ser.write(cmd.encode())
    time.sleep(1)
    serial_read()
