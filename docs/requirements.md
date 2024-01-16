# Client GUI Requirements

[ReqId:01v01]: the GUI shall present a dropdown menu allowing selection of the ESP32-connected serial port.

[ReqId:02v01]: Functional buttons labeled `<Start Session>` and `<End Session>` shall be available on the GUI for session initiation and termination, respectively.

[ReqId:03v01]: the GUI shall contain button labeled `<Get Temperature>` to trigger respective actions with the ESP32.

[ReqId:04v01]: the GUI shall contain button labeled `<Toggle LED>` to turn on/off the led connected to ESP32.

[ReqId:05v01]: it shall be possible to have a functional button in the GUI to display `<log>` of user actions.

[ReqId:06v01]: it shall be possible to have a functional button in the GUI to display `<status>` of user session.

## Server (Serial Communication and Session Management) Requirements

[ReqId:01.1v01]: it shall be possible to have a function to initialize Serial connection between the client and ESP32.

[ReqId:01.2v01]: it shall be possible to configure necessary serial communication settings (baud rate, parity, etc.) for reliable data exchange.

[ReqId:02v01]: it shall be possible to have a function to establish a session between the client and server.

[ReqId:03v01]: it shall be possible to have a function to terminate a session between the client and server.

[ReqId:04v01]: there shall be a function to send temperature requests from the client to the ESP32.

[ReqId:05v01]: it shall be possible to receive and process responses from the ESP32 to user-initiated requests.

[ReqId:06.1v01]: there shall be a function to enable the client to send commands to toggle the LED state on the ESP32.

[ReqId:06.2v01]: there shall be a function to handle and process confirmation or status responses to LED toggle commands.

## Security Requirements
