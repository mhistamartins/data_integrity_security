#include <Arduino.h>
#include <esp_system.h>
#include "protocol.h"

// Define the pin for the LED
const int ledPin = 21;

void setup() 
{
    // Initialize serial communication at the defined baud rate
    protocol_init();
    
    // Initialize the LED pin as an output
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);
}

void loop() 
{
    // Buffer to hold incoming data
    uint8_t buffer[64];
    size_t len = protocol_receive(buffer, sizeof(buffer));

    // If data is received
    if (len == 1) 
    {
        switch (buffer[0]) 
        {
            case SESSION_ESTABLISH:
                protocol_send(buffer, 1);
                break;

            case CLOSE_SESSION:
                protocol_send(buffer, 1);
                break;

            case GET_TEMPERATURE:
                {
                    float temperature = temperatureRead();
                    protocol_send((uint8_t*)&temperature, sizeof(temperature));
                }
                break;

            case TOGGLE_LED:
                {
                    digitalWrite(ledPin, !digitalRead(ledPin));
                    uint8_t response[1] = {TOGGLE_LED};
                    protocol_send(response, 1);
                }
                break;

            default:
                // Handle unrecognized command
                protocol_send((uint8_t*)"Unknown command.", 16);
                break;
        }
    }
}
