#include "protocol.h"

bool serial_init(void) 
{
    Serial.begin(BAUDRATE);
    return Serial; // Check if serial port is initialized
}

bool send_data(const uint8_t* data, size_t dlen) 
{
    return (dlen == Serial.write(data, dlen)); // Return true if all bytes were sent successfully
}

size_t receive_data(uint8_t* buffer, size_t blen) 
{
    while (0 == Serial.available())
    {
        ;   // Wait until data is available
    }
    return Serial.readBytes(buffer, blen); // Return the number of bytes read
}
