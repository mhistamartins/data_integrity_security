#include <Arduino.h>
#include "session.h"

// Define the pin number for the LED
#define LED_PIN 21

// Variable to keep track of the LED state (LOW for off, HIGH for on)
int ledState = LOW;

// Function to toggle the state of the LED
static void toggle_led(void)
{
  // Toggle the LED state
  ledState = !ledState;
  // Write the new state to the LED pin
  digitalWrite(LED_PIN, ledState);
}

// Arduino setup function, runs once at startup
void setup()
{
  // Set the LED pin as an output
  pinMode(LED_PIN, OUTPUT);
  // Set GPIO pin 21 as an output (redundant since LED_PIN is also 21)
  pinMode(GPIO_NUM_21, OUTPUT);
  // Delay for 100 milliseconds
  delay(100);
  // Initialize the session
  session_init();
}

// Arduino loop function, runs repeatedly after setup
void loop()
{
  // Initialize a response structure
  response_t respond = {0};

  // Get the current session request
  int request = session_request();

  // Set GPIO pin 32 to LOW
  digitalWrite(GPIO_NUM_32, LOW);

  // Check if the request is to get the temperature
  if (request == SESSION_TEMPERATURE)
  {
    // Indicate a successful response
    respond.data[0] = SESSION_OKAY;
    // Read the temperature and store it in the response data
    sprintf((char *)&respond.data[1], "%2.2f", temperatureRead());

    // Send the response
    request = session_response(&respond);
  }
  // Check if the request is to toggle the LED
  else if (request == SESSION_TOGGLE_LED)
  {
    // Indicate a successful response
    respond.data[0] = SESSION_OKAY;
    // Toggle the LED
    toggle_led();

    // Store the new LED state in the response data
    sprintf((char *)&respond.data[1], "%d", ledState);
    // Send the response
    request = session_response(&respond);
  }

  // Check if there was an error in the session
  if (request == SESSION_ERROR)
  {
    // Set GPIO pin 32 to HIGH to indicate an error
    digitalWrite(GPIO_NUM_32, HIGH);
  }
}
