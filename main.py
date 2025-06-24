import meshtastic
import meshtastic.serial_interface
from meshtastic.util import findPorts
from pubsub import pub
import threading
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
import time

# Default settings
settings = {
    "discord_webhook": "",
    "serial_port": ""
}

running = True
interface = None
log_window = None  # Declare globally

def show_settings_gui():
    def refresh_ports():
        ports = findPorts()
        port_combo['values'] = ports
        if ports:
            port_combo.current(0)

    def save_settings():
        settings["discord_webhook"] = webhook_entry.get()
        settings["serial_port"] = port_combo.get()
        start_bridge()

    global log_window

    root = tk.Tk()
    root.title("Meshtastic Discord Bridge")
    root.geometry("800x600")
    root.configure(bg="black")

    teal = "#00FFFF"
    font_mono = ("Consolas", 10)

    # Layout container
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(fill='both', expand=True)

    # Title
    tk.Label(main_frame, text="Meshtastic Discord Bridge", bg="black", fg=teal, font=("Consolas", 14, "bold")).pack(pady=(10, 10))

    # Webhook input
    tk.Label(main_frame, text="Discord Webhook URL:", bg="black", fg=teal, font=font_mono).pack(anchor='w', padx=10)
    webhook_entry = tk.Entry(main_frame, width=58, bg="gray10", fg=teal, insertbackground=teal, font=font_mono, relief="flat")
    webhook_entry.pack(padx=10, pady=(2, 10), fill='x')

    # Serial port input
    tk.Label(main_frame, text="Serial Port:", bg="black", fg=teal, font=font_mono).pack(anchor='w', padx=10)
    port_combo = ttk.Combobox(main_frame, width=55, font=font_mono)
    port_combo.pack(padx=10, pady=(2, 10), fill='x')

    # Style ttk combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground="black",
                    background="black",
                    foreground=teal,
                    arrowcolor=teal,
                    bordercolor=teal,
                    lightcolor=teal,
                    darkcolor=teal,
                    padding=3)

    tk.Button(main_frame, text="Refresh Ports", command=refresh_ports,
          bg="gray10", fg=teal, activebackground="black", activeforeground=teal,
          font=font_mono, relief="flat", padx=5, pady=2, cursor="hand2").pack(pady=(2, 5))

    tk.Button(main_frame, text="Save and Start", command=save_settings,
          bg="gray10", fg=teal, activebackground="black", activeforeground=teal,
          font=font_mono, relief="flat", padx=5, pady=2, cursor="hand2").pack(pady=(0, 10))



    # Log label
    tk.Label(main_frame, text="Log:", bg="black", fg=teal, font=font_mono).pack(anchor='w', padx=10, pady=(0, 2))

    # Log window (responsive)
    log_window = scrolledtext.ScrolledText(main_frame, bg="gray2", fg=teal, insertbackground=teal,
                                           font=font_mono, relief="flat", state='disabled', cursor="arrow")
    log_window.pack(padx=10, pady=(0, 10), fill='both', expand=True)

    refresh_ports()
    root.mainloop()

# Log function
def log(message):
    print(message)
    log_window.config(state='normal')
    log_window.insert(tk.END, message + '\n')
    log_window.see(tk.END)
    log_window.config(state='disabled')

# Start the bridge with auto-reconnect
def start_bridge():
    bridge_thread = threading.Thread(target=start_meshtastic_bridge, daemon=True)
    bridge_thread.start()

# Meshtastic connection
def start_meshtastic_bridge():
    global running, interface
    while running:
        try:
            log("Attempting to connect to Meshtastic device...")
            interface = meshtastic.serial_interface.SerialInterface(devPath=settings["serial_port"] or None)

            pub.subscribe(on_receive, "meshtastic.receive.text")
            pub.subscribe(on_connect, "meshtastic.connection.established")

            log("Listening for Meshtastic messages...")
            send_to_discord("\U0001F4AC Meshtastic bridge is now online!")

            while running:
                time.sleep(1)

        except Exception as e:
            log(f"Error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

# Handle received messages
def on_receive(packet, interface):
    try:
        if 'decoded' in packet and 'text' in packet['decoded']:
            text = packet['decoded']['text']
            from_id = packet['fromId']
            message = f"\U0001F4E1 Message from {from_id}: {text}"
            log(message)
            send_to_discord(message)
    except Exception as e:
        log(f"Error processing packet: {e}")

# Handle connection event
def on_connect(interface, topic=pub.AUTO_TOPIC):
    log("Connected to Meshtastic device!")
    send_to_discord("\U0001F4AC Meshtastic bridge is now online!")

# Send message to Discord
def send_to_discord(message):
    try:
        data = {"content": message}
        response = requests.post(settings["discord_webhook"], json=data)
        if response.status_code != 204:
            log(f"Failed to send to Discord: {response.status_code} - {response.text}")
    except Exception as e:
        log(f"Error sending to Discord: {e}")

if __name__ == "__main__":
    show_settings_gui()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        log("Shutting down bridge...")
        running = False
        time.sleep(1)
        log("Bridge stopped.")
