import serial
import serial.tools.list_ports

ser: serial.Serial  # Serial connection object

def enumerate_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def protocol_init(port, baudrate=115200) -> bool:
    global ser
    ser = serial.Serial(port, baudrate)
    return ser.is_open

def protocol_send(data) -> bool:
    global ser
    ret = False
    if ser.is_open == True:
        ret = (len(data) == ser.write(data))  # Send
    return ret
    

def protocol_receive(size: int):
    global ser
    data = bytes()
    if ser.is_open == True:
        data = ser.read(size)
    return data
