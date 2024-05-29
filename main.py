import tkinter as tk
from tkinter import ttk
import serial
import time
import protocol


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

        self.get_temp_button = ttk.Button(self.master, text="Get Temperature", command=self.get_temperature)
        self.toggle_led_button = ttk.Button(self.master, text="Toggle LED", command=self.toggle_led)
        self.clear_log_button = ttk.Button(self.master, text="Clear", command=self.clear_log)

        self.log_label = ttk.Label(self.master, text="Log:")
        self.log_textbox = tk.Text(self.master, height=23, width=50)
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
                    protocol.protocol_send("Establish_Session")  # Send command to establish session
                    self.session_button.configure(text="Close Session")
                    self.log_message("Session established.")

                    # Enable the get temp button
                    self.get_temp_button.configure(state="normal")

                    # Enable the Toggle LED button
                    self.toggle_led_button.configure(state="normal")
                except Exception as e:
                    self.log_message(f"Error establishing session: {str(e)}")
            else:
                self.log_message("Please select a port.")
        else:
            protocol.protocol_send("Close_Session")  # Send command to close session
            protocol.ser.close()
            self.session_active = False
            self.session_button.configure(text="Establish Session")
            self.log_message("Session closed.")


    def get_temperature(self):
        if self.session_active:
            # Send command to server to get temperature
            protocol.protocol_send("GET_TEMPERATURE")

            # Receive temperature value from server
            temperature_response = protocol.protocol_receive()
            if temperature_response.startswith("Temperature:"):
                temperature_value = temperature_response.split(":")[1].strip()
                self.log_message(f"Temperature: {temperature_value} ˚C")  # Display temperature in log message box
            else:
                self.log_message("Failed to retrieve temperature data from server.")
        else:
            self.get_temp_button.configure(state="disabled")
            self.log_message("No active session.")

    def toggle_led(self):
        if self.session_active:
            protocol.protocol_send("TOGGLE_LED")

            # Receive Toggle led message
            led_response = protocol.protocol_receive()

            # Update the log message box
            self.log_message(led_response.strip())
        else:
            self.log_message("No active session.")
            self.toggle_led_button.configure(state="disabled")

    def clear_log(self):
        self.log_textbox.configure(state='normal')
        self.log_textbox.delete(1.0, tk.END)
        self.log_textbox.configure(state='disabled')

    def log_message(self, message):
        self.log_textbox.configure(state='normal')
        self.log_textbox.insert(tk.END, f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        self.log_textbox.configure(state='disabled')


def main():
    root = tk.Tk()
    root.geometry("730x400")
    app = ClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
