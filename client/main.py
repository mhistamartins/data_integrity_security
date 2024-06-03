import tkinter as tk
from tkinter import ttk
import serial
import time
import struct 
import protocol


SESSION_ESTABLISH = b'\x01'
CLOSE_SESSION = b'\x02'
GET_TEMPERATURE = b'\x03'
TOGGLE_LED = b'\x04'


class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")

        self.session_active = False

        self.selected_port = tk.StringVar()
        self.log_text = tk.StringVar()
    
        self.create_widgets()

    def create_widgets(self):
        # GUI components
        self.port_label = ttk.Label(self.master, text="Select Port:")
        self.port_combobox = ttk.Combobox(self.master, textvariable=self.selected_port)
        self.port_combobox['values'] = protocol.enumerate_serial_ports()

        self.session_button = ttk.Button(self.master, text="Establish Session", command=self.toggle_session)

        self.get_temp_button = ttk.Button(self.master, text="Get Temperature", command=self.get_temperature, state=tk.DISABLED)
        self.toggle_led_button = ttk.Button(self.master, text="Toggle LED", command=self.toggle_led, state=tk.DISABLED)
        self.clear_log_button = ttk.Button(self.master, text="Clear", command=self.clear_log)

        self.log_label = ttk.Label(self.master, text="Log:")
        self.log_textbox = tk.Text(self.master, height=23, width=50)
        self.log_textbox.tag_config("error", foreground="red")
        self.log_textbox.insert(tk.END, "Log messages will appear here.\n")
        self.log_textbox.configure(state='disabled')

        # Layout
        self.port_label.grid(row=0, column=0, padx=5, pady=5)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.session_button.grid(row=0, column=2, padx=5, pady=5)  
        self.get_temp_button.grid(row=0, column=3, padx=5, pady=5)
        self.toggle_led_button.grid(row=0, column=4, padx=5, pady=5)
        self.clear_log_button.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
        self.log_label.grid(row=1, column=0, padx=5, pady=5)
        self.log_textbox.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")


    def toggle_session(self):
        if not self.session_active:
            port = self.selected_port.get()
            if port:
                try:
                    protocol.protocol_init(port)
                    self.session_active = True
                    if True == protocol.protocol_send(SESSION_ESTABLISH):  # Send command to establish session
                        data = protocol.protocol_receive(1)
                        if 1 == len(data):
                            if data[0] == 0x01:
                                self.session_button.configure(text="Close Session")
                                self.log_message("Session established.")
                            else:
                                self.log_message("Failed to establish session.")
                    else:
                        self.log_message("Communication failed.")

                    # Enable the get temp button
                    self.get_temp_button.configure(state="normal")

                    # Enable the Toggle LED button
                    self.toggle_led_button.configure(state="normal")
                except Exception as e:
                    self.log_message(f"Error establishing session: {str(e)}", tag="error")
            else:
                self.log_message("Please select a port.", tag="error")
        else:
            protocol.protocol_send(CLOSE_SESSION)  # Send command to close session
            protocol.ser.close()
            self.session_active = False
            self.session_button.configure(text="Establish Session")
            self.log_message("Session closed.")
            
            # Disable the buttons
            self.get_temp_button.configure(state="disabled")
            self.toggle_led_button.configure(state="disabled")

    def get_temperature(self):
        if self.session_active:
            try:
                if protocol.protocol_send(GET_TEMPERATURE):
                    # Wait and receive the response
                    data = protocol.protocol_receive(4)
                    # Check if the response is received and correct
                    if len(data) == 4:
                        temperature = struct.unpack('f', data)[0]
                        self.log_message(f"Temperature: {temperature:2.2f} °C")
                    else:
                        self.log_message("Error reading temperature. No or incomplete response received.", tag="error")
                else:
                    self.log_message("Failed to send get temperature command.", tag="error")
            except Exception as e:
                self.log_message(f"Error reading temperature: {str(e)}", tag="error")
        else:
            self.log_message("Session is not active. Cannot get temperature.", tag="error")


    def toggle_led(self):
        if self.session_active:
            try:
                # Send the toggle LED command
                if protocol.protocol_send(TOGGLE_LED):
                    # Wait and receive the response
                    data = protocol.protocol_receive(1)
                    # Check if the response is received and correct
                    if len(data) == 1:
                        if data[0] == 0x04:
                            self.log_message("LED toggled successfully.")
                        else:
                            self.log_message("Error toggling LED. Unexpected response.", tag="error")
                    else:
                        self.log_message("Error toggling LED. No or incomplete response received.", tag="error")
                else:
                    self.log_message("Failed to send toggle LED command.", tag="error")
            except Exception as e:
                self.log_message(f"Error toggling LED: {str(e)}", tag="error")
        else:
            self.log_message("Session is not active. Cannot toggle LED.", tag="error")



    def clear_log(self):
        self.log_textbox.configure(state='normal')
        self.log_textbox.delete(1.0, tk.END)
        self.log_textbox.configure(state='disabled')

    def log_message(self, message, tag=None):
        self.log_textbox.configure(state='normal')
        self.log_textbox.insert(tk.END, f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n", tag)
        self.log_textbox.configure(state='disabled')

def main():
    root = tk.Tk()
    root.geometry("730x400")
    app = ClientGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()