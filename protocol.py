import serial
import serial.tools.list_ports

ser = None  # Serial connection object

def enumerate_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def protocol_init(port, baudrate=115200):
    global ser
    ser = serial.Serial(port, baudrate)


def protocol_send(data):
    if ser is not None:
        ser.write(data.encode())  # Convert string to bytes and send

def protocol_receive():
    if ser is not None:
        return ser.readline().decode().strip()  # Read a line, decode bytes to string, and strip newline characters
    return None


    #so basically the python script is meant to send ech func as a string and then serial decodes it as a byte