# Meshtastic Discord Bridge

A Python application that bridges Meshtastic mesh network messages to Discord using webhooks. This tool allows you to receive and forward messages from your Meshtastic network directly to a Discord channel.

<img src="screenshots/img1.png" alt="Meshtastic Discord Bridge GUI" width="500"/> <img src="screenshots/img2.png" alt="Meshtastic Discord Bridge GUI" width="500"/>

## Features

- 🔗 **Real-time bridging**: Forwards Meshtastic messages to Discord in real-time
- 🖥️ **GUI Interface**: User-friendly graphical interface for configuration
- 🔄 **Auto-reconnect**: Automatically reconnects if the connection is lost
- 📡 **Serial Port Detection**: Automatically detects available serial ports
- 📝 **Live Logging**: Real-time log display in the GUI
- 🎨 **Dark Theme**: Modern dark interface with teal accents

## Prerequisites

- Python 3.7 or higher
- A Meshtastic device
- A Discord webhook URL
- USB connection to your Meshtastic device

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/luckypines/Meshtastic-to-Discord-bridge.git
   cd meshtastic-to-discord-bridge
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### Discord Webhook Setup

1. Go to your Discord server settings
2. Navigate to Integrations → Webhooks
3. Create a new webhook or use an existing one
4. Copy the webhook URL

### Meshtastic Device Setup

1. Connect your Meshtastic device to your computer via USB
2. Ensure your device is powered on and in range of the mesh network
3. Note the serial port your device is connected to (the application will help detect this)

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Configure the bridge:**
   - Enter your Discord webhook URL
   - Select the appropriate serial port for your Meshtastic device
   - Click "Refresh Ports" if your device isn't detected
   - Click "Save and Start" to begin bridging

3. **Monitor the logs:**
   - The application will display connection status and incoming messages
   - Messages from the mesh network will be forwarded to Discord
   - The bridge will automatically reconnect if the connection is lost

## How It Works

The application creates a bridge between your Meshtastic mesh network and Discord:

1. **Connection**: Establishes a serial connection to your Meshtastic device
2. **Message Reception**: Listens for incoming text messages from the mesh network
3. **Forwarding**: Sends received messages to Discord via webhook
4. **Status Updates**: Sends connection status updates to Discord

## Message Format

Messages sent to Discord include:
- 📡 **Connection status**: When the bridge comes online
- 📨 **Incoming messages**: Format: "📡 Message from [node_id]: [message_text]"

## Troubleshooting

### Common Issues

**Device not detected:**
- Ensure your Meshtastic device is properly connected
- Try clicking "Refresh Ports"
- Check if your device drivers are installed

**Connection errors:**
- Verify the serial port is correct
- Ensure no other application is using the port
- Check that your device is powered on

**Discord webhook issues:**
- Verify the webhook URL is correct
- Check that the webhook is still active in Discord
- Ensure the webhook has permission to send messages

### Log Messages

- `"Attempting to connect to Meshtastic device..."` - Connection attempt
- `"Connected to Meshtastic device!"` - Successful connection
- `"Listening for Meshtastic messages..."` - Ready to receive messages
- `"Error: [error message]"` - Connection or processing error

## Dependencies

- **meshtastic**: Python library for Meshtastic devices
- **requests**: HTTP library for Discord webhook communication
- **PyPubSub**: Event-driven messaging library
- **tkinter**: GUI framework (included with Python)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note:**  This bridge **requires a physical Meshtastic device** to function. Please ensure you have the necessary hardware before attempting to use this software.
I am **not affiliated with the Meshtastic project or its developers**. This is an independent project created for personal and community use.

