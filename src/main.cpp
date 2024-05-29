#include <Arduino.h>
#include <esp_system.h>
#include "protocol.h"

// Define the pin for the LED
const int ledPin = 21;

// Declare the external temperature sensor reading function
extern "C" uint8_t temprature_sens_read();

float read_core_temperature() 
{
    // Read the core temperature of the MCU in degrees Celsius
    uint8_t core_temp = temprature_sens_read();

    // Convert the raw temperature to degrees Celsius (rough conversion)
    float temp_celsius = (core_temp - 32) / 1.8;
    return temp_celsius;
}

void setup() 
{
    // Initialize serial communication at the defined baud rate
    serial_init();
    
    // Initialize the LED pin as an output
    pinMode(ledPin, OUTPUT);
    
    // Ensure the LED is off initially
    digitalWrite(ledPin, LOW);
}

void loop() 
{
    // Buffer to hold incoming data
    uint8_t buffer[64];
    size_t len = receive_data(buffer, sizeof(buffer));

    // If data is received
    if (len > 0) 
    {
        // Null-terminate the received data to make it a valid C string
        buffer[len] = '\0';
        
        // Convert buffer to a string for easier comparison
        String command = String((char*)buffer);
        
        // Handle commands
        if (command == "Establish_Session") 
        {
            // Handle establishing a session
            send_data((const uint8_t*)"Session established\n", 20);
        }
        else if (command == "Close_Session") 
        {
            // Handle closing a session
            send_data((const uint8_t*)"Session closed\n", 15);
        }
        else if (command == "GET_TEMPERATURE") 
        {
            // Read the core temperature
            float temperature = read_core_temperature();
            
            // Prepare the response
            char response[32];
            snprintf(response, sizeof(response), "Temperature: %.2f\n", temperature);
            
            // Send the temperature
            send_data((const uint8_t*)response, strlen(response));
        }
        else if (command == "TOGGLE_LED") 
        {
            // Toggle the LED state
            int ledState = digitalRead(ledPin);
            digitalWrite(ledPin, !ledState);
            
            // Prepare the response
            const char* response = (ledState == LOW) ? "   LED is ON\n" : "   LED is OFF\n";
            
            // Send the response
            send_data((const uint8_t*)response, strlen(response));
        }
        else 
        {
            // Handle unknown command
            send_data((const uint8_t*)"Unknown command\n", 16);
        }

        delay(200);
    }
}
