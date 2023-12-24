import tkinter as tk
from tkinter import ttk

# Function to toggle session button label
def toggle_session():
    if session_state.get() == "Active":
        session_state.set("Inactive")
        session_button.config(text="Establish Session")
    else:
        session_state.set("Active")
        session_button.config(text="Close Session")

# create root window
root = tk.Tk()

# root window title and dimension
root.title("Client")
root.geometry('630x500')


# Label
ttk.Label(root, text="Serial Ports:",
          font=("Times New Roman", 15)).grid(column=1,
                                             row=0, padx=10, pady=25)

n = tk.StringVar()
portchoosen = ttk.Combobox(root, width=12,
                           textvariable=n)

# Adding combobox drop down list
portchoosen['values'] = ('port1',
                         'port2',
                         'port3')

portchoosen.grid(column=2, row=0)

# Default port
portchoosen.current(1)

# Variable to track session state
session_state = tk.StringVar(root, "Inactive")

# Function to toggle session state and button label
session_button = tk.Button(root, text="Establish Session", command=toggle_session)
session_button.grid(column=3, row=0)

# all widgets will be here
button1 = tk.Button(root, text="Establish Session")
button2 = tk.Button(root, text="Get Temperature")
button3 = tk.Button(root, text="Toggle Led")
button4 = tk.Button(root, text="log:")
button5 = tk.Button(root, text="clear", fg="blue")

# set Button grid
button1.grid(column=3, row=0)
button2.grid(column=4, row=0)
button3.grid(column=5, row=0)
button4.grid(column=1, row=1)
button5.grid(column=5, row=1)

# Frame below the buttons
frame = tk.Frame(root, width=600, height=380, bg="lightgrey")
frame.grid(column=0, row=2, columnspan=25) 

# Execute Tkinter
root.mainloop()
