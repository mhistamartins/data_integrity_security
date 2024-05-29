#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <Arduino.h>
#define BAUDRATE 9600

bool serial_init(void);
bool send_data(const uint8_t* data, size_t dlen);
size_t receive_data(uint8_t* buffer, size_t blen);
#endif