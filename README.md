# Forza Telemetry Dashboard (Race Engineer)

This project is a Python application that captures live telemetry (vehicle physics) data from Forza Horizon Series and Forza Motorsport via a local network and translates it into a visual "Race Engineer" dashboard. Data from the console (Xbox) is processed asynchronously on a Mac over Wi-Fi.

# Features
* **Real-time Data Stream:** Zero-latency display of RPM, Speed (KM/H), and Gear.
* **Shift Light:** When the engine RPM reaches the most efficient value, the entire screen flashes red to prompt a gear upshift.
* **TCS (Traction Control System) Warning:** If any of the four tires loses traction, an instant "TCS ACTIVE" warning appears on the dashboard.

# What I Learned in This Project?

While developing this project, I gained practical experience in core computer engineering concepts such as hardware communication, network protocols, and memory management:

1. **Network Programming (UDP Sockets & Ports):** 
   * Learned how two different devices (Xbox and Mac) communicate over the same network.
   * Utilized the `socket` library to bind and listen to port `9999`.
   * Implemented **UDP (User Datagram Protocol)** instead of TCP to handle high-frequency data packets sent by the game engine, prioritizing speed over packet loss.

2. **C++ Memory Architecture & Struct Unpacking:**
   * Since the game engine is built with C++, the incoming data is raw binary rather than plain text.
   * Used the Python `struct` module and memory offsets to extract specific values from the massive data packet (example, Speed is at byte 244, Gear is at byte 307).
   * Gained an understanding of how data is laid out in memory (Little-Endian `<` byte order) and handled conversions between integers (`int`/`uint`) and floating-point numbers (`float`).

3. **Asynchronous GUI Programming (Non-blocking):**
   * Configured the UDP socket to `setblocking(False)` to prevent the socket listening process from freezing the GUI loop.
   * Created specific loop mechanics (`window.after()`) to ensure the interface refreshes perfectly at high frame rates.
   * The tkinter library section was created with the help of artificial intelligence.

# How to Use?
1. Launch the Forza game and navigate to `Settings > HUD and Gameplay`.
2. Scroll to the bottom and turn `Data Out` to **ON**.
3. Enter your computer's local IP address and set the port to `9999`. (Data Format: CarDash).
4. Run the command `python3 forza_telemetry.py` in your terminal.
