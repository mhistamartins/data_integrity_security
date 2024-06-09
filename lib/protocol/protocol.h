#ifndef PROTOCOL_H
#define PROTOCOL_H

// Define command constants using enum
enum Command 
{
    SESSION_ESTABLISH = 0x01,
    CLOSE_SESSION = 0x02,
    GET_TEMPERATURE = 0x03,
    TOGGLE_LED = 0x04
};

bool protocol_init(void);
bool protocol_send(const uint8_t *data, size_t dlen);
size_t protocol_receive(uint8_t *buffer, size_t blen);

#endif