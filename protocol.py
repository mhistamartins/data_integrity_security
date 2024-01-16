import serial

ser = None  # Serial connection object

def protocol_init(port, baudrate=9600):
    global ser
    ser = serial.Serial(port, baudrate)
    # You might want to add more configuration options here

def protocol_send(data):
    if ser is not None:
        ser.write(data.encode())  # Convert string to bytes and send

def protocol_receive():
    if ser is not None:
        return ser.readline().decode().strip()  # Read a line, decode bytes to string, and strip newline characters
    return None
