#ifndef PROTOCOL_H
#define PROTOCOL_H

bool protocol_init(void);
bool protocol_send(const uint8_t *data, size_t dlen);
size_t protocol_receive(uint8_t *buffer, size_t blen);

#endif