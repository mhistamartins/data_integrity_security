import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

# Function to toggle session button label
def toggle_session():
    if session_state.get() == "Active":
        session_state.set("Inactive")
        session_button.config(text="Establish Session")
    else:
        session_state.set("Active")
        session_button.config(text="Close Session")

# Function to get available serial ports
def get_serial_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return ports

# create root window
root = tk.Tk()

# root window title and dimension
root.title("Client")
root.geometry('630x500')


# Label
ttk.Label(root, text="Serial Ports:", font=("Times New Roman", 15)).grid(column=1, row=0, padx=10, pady=25)

n = tk.StringVar()
portchoosen = ttk.Combobox(root, width=12,textvariable=n)

# Get available serial ports dynamically
serial_ports = get_serial_ports()
portchoosen['values'] = tuple(serial_ports)  # Set values to available ports

# If no ports are available, set default value
if serial_ports:
    portchoosen.current(0)  # Set default to the first port

portchoosen.grid(column=2, row=0)

# Variable to track session state
session_state = tk.StringVar(root, "Inactive")

# Function to toggle session state and button label
session_button = tk.Button(root, text="Establish Session", command=toggle_session)
session_button.grid(column=3, row=0)

# all widgets will be here
button1 = tk.Button(root, text="Establish Session")
button2 = tk.Button(root, text="Get Temperature")
button3 = tk.Button(root, text="Toggle Led")
button4 = tk.Button(root, text="clear", fg="blue")

# set Button grid
button1.grid(column=3, row=0)
button2.grid(column=4, row=0)
button3.grid(column=5, row=0)
button4.grid(column=5, row=1)

#labels
label1 = tk.Label(root, text="log:")

# Grid labels in the root window
label1.grid(column=1, row=1)


# Frame below the buttons
frame = tk.Frame(root, width=600, height=380, bg="lightgrey")
frame.grid(column=0, row=2, columnspan=25) 

# Execute Tkinter
root.mainloop()
