import tkinter as tk
from tkinter import ttk
import time
import protocol
from session import Session

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")

        self.session = None
        self.selected_port = tk.StringVar()
        self.log_text = tk.StringVar()
    
        self.create_widgets()

    def create_widgets(self):
        # GUI components
        self.port_label = ttk.Label(self.master, text="Select Port:")
        self.port_combobox = ttk.Combobox(self.master, textvariable=self.selected_port)
        self.port_combobox['values'] = protocol.enumerate_serial_ports()
        self.port_combobox.bind('<<ComboboxSelected>>', self.select_port_establish)

        self.session_button = ttk.Button(self.master, text="Establish Session", command=self.establish_session, state=tk.DISABLED)

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

    def select_port_establish(self, event):
        port = self.selected_port.get()
        if port:
            self.log_message(f"Port selected: {port}")
            try:
                # Initialize a session with the selected port
                self.secure_session = Session(port)
                self.session_button.config(state="normal")
            except Exception as e:
                self.log_message(f"Error during key exchange: {str(e)}", tag="error")

    def establish_session(self):
        try:
            self.secure_session.establish()
            if self.secure_session.state:
                self.session_button.configure(text="Close Session", command=self.close_session)
                self.log_message("Session established.")
                self.get_temp_button.configure(state="normal")
                self.toggle_led_button.configure(state="normal")    
            else:
                self.log_message("Failed to establish a session")
        except Exception as e:
            self.log_message(f"Error establishing session: {str(e)}", tag="error")

    def close_session(self):
        try:
            self.secure_session.state = False
            self.session_button.configure(text="Establish Session", command=self.establish_session)
            self.log_message("Session closed.")
            self.get_temp_button.configure(state="disabled")
            self.toggle_led_button.configure(state="disabled")
        except Exception as e:
            self.log_message(f"Error closing session: {str(e)}", tag="error")


    def get_temperature(self):
        received_bytes = self.secure_session.get_temperature()
        if received_bytes is not None:
            try:
                temperature = received_bytes[0:].decode("utf-8")
                message = f"Temperature: {temperature} °C"
                self.log_message(message)
            except Exception as e:
                self.clear_log()
                self.log_message(f"Error: Unable to get temperature. {str(e)}")
        else:
            self.clear_log()
            self.log_message("Error: Unable to get temperature")

    def toggle_led(self):
        state = self.secure_session.toggle_led()
        if state is not None:
            try:
                state_str = state.decode("utf-8").strip('\x00')
                if state_str == "1":
                    self.log_message("LED State: ON")
                elif state_str == "0":
                    self.log_message("LED State: OFF")
                else:
                    self.log_message("Unexpected LED status response")
            except Exception as e:
                self.log_message(f"Error decoding LED status: {str(e)}")

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
