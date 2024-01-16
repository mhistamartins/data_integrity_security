import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from protocol import protocol_init, protocol_send, protocol_receive

# Function to get a list of available serial ports
def get_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

# Function to update the log in the GUI
def update_log(message):
    log_text.config(state=tk.NORMAL)         # Enable text widget for editing
    log_text.insert(tk.END, message + "\n")  # Insert the message at the end of the log
    log_text.config(state=tk.DISABLED)       # Disable text widget for read-only

# Function to toggle the session state
def toggle_session():
    new_state = "Inactive" if session_state.get() == "Active" else "Active"
    session_state.set(new_state)
    
    session_button.config(text="Close Session" if new_state == "Active" else "Establish Session")

    # Enable/Disable buttons based on the session state
    button2.config(state=tk.NORMAL if new_state == "Active" else tk.DISABLED)
    button3.config(state=tk.NORMAL if new_state == "Active" else tk.DISABLED)

    update_log("Session {}.".format("closed" if new_state == "Inactive" else "established"))

# Function to establish a session
def establish_session(session_state, portchoosen, button2, button3):
    if session_state.get() == "Inactive":
        protocol_init(portchoosen.get())    # Initialize with the selected serial port
        protocol_send("ESTABLISH_SESSION")  # Send a command to establish the session
        response = protocol_receive()       # Receive the response from the protocol

        if response == "SESSION_ESTABLISHED":
            update_log("Session established successfully.")
        else:
            update_log("Failed to establish session. {}".format(response))

# Function to toggle the LED
def toggle_led(session_state):
    if session_state.get() == "Active":
        protocol_send("TOGGLE_LED")        # Send a command to toggle the LED
        response = protocol_receive()       # Receive the response from the protocol

        if response == "LED_TOGGLED":
            update_log("LED toggled successfully.")
        else:
            update_log("Failed to toggle LED. {}".format(response))

# Function to get the temperature
def get_temperature(session_state):
    if session_state.get() == "Active":
        protocol_send("GET_TEMPERATURE")   # Send a command to get the temperature
        response = protocol_receive()       # Receive the response from the protocol

        if response.startswith("TEMPERATURE:"):
            temperature_value = response.split(":")[1]
            update_log("Temperature: {} °C".format(temperature_value))
        else:
            update_log("Failed to get temperature. {}".format(response))


def setup_gui():
    global session_state, session_button, button2, button3, log_text
    root = tk.Tk()
    root.title("Client")
    root.geometry('630x500')

    # Serial Ports
    ttk.Label(root, text="Serial Ports:", font=("Times New Roman", 15)).grid(column=1, row=0, padx=10, pady=25)

    n = tk.StringVar()
    portchoosen = ttk.Combobox(root, width=12, textvariable=n)
    serial_ports = get_serial_ports()
    portchoosen['values'] = tuple(serial_ports)
    portchoosen.current(0) if serial_ports else None
    portchoosen.grid(column=2, row=0)

    # Session
    session_state = tk.StringVar(root, "Inactive")
    session_button = tk.Button(root, text="Establish Session", command=toggle_session)
    session_button.grid(column=3, row=0)

    # Buttons
    button1 = tk.Button(root, text="Establish Session", command=establish_session)
    button2 = tk.Button(root, text="Get Temperature", state=tk.DISABLED, command=get_temperature)
    button3 = tk.Button(root, text="Toggle LED", state=tk.DISABLED, command=toggle_led)
    button4 = tk.Button(root, text="clear", fg="blue")


    # set Button grid
    button1.grid(column=3, row=0)
    button2.grid(column=4, row=0)
    button3.grid(column=5, row=0)
    button4.grid(column=5, row=1)

    # Labels
    ttk.Label(root, text="log:", font=("Times New Roman", 15)).grid(column=1, row=1)

    # Frame below the buttons
    frame = tk.Frame(root, width=600, height=380, bg="lightgrey")
    frame.grid(column=0, row=2, columnspan=25)

    return root

# Execute Tkinter
if __name__ == "__main__":
    root = setup_gui()
    root.mainloop()

