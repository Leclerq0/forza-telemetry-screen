import socket
import struct
import tkinter as tk

UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
sock.setblocking(False)

def update_telemetry():
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            max_rpm = struct.unpack_from('<f', data, 8)[0]
            current_rpm = struct.unpack_from('<f', data, 16)[0]

            speed_ms = struct.unpack_from('<f', data, 244)[0]
            speed_kmh = speed_ms * 3.6

            gear = struct.unpack_from('<B', data, 307)[0]
            gear_text = "N/R" if gear == 0 else str(gear)

            slip_fl = struct.unpack_from('<f', data, 180)[0]
            slip_fr = struct.unpack_from('<f', data, 184)[0]
            slip_rl = struct.unpack_from('<f', data, 188)[0]
            slip_rr = struct.unpack_from('<f', data, 192)[0]

            tcs_active = speed_kmh > 5 and any(abs(s) > 1.0 for s in [slip_fl, slip_fr, slip_rl, slip_rr])

            rpm_label.config(text=f"{current_rpm:.0f} RPM")
            speed_label.config(text=f"{speed_kmh:.0f} KM/H")

            gear_label.config(text=f"Gear: {gear_text}")

            if tcs_active:
                tcs_label.config(text="⚠️ TCS ", fg="orange")
            else:
                tcs_label.config(text="• TCS ", fg="#444444")

            if max_rpm > 0 and current_rpm > (max_rpm * 0.93):
                window.config(bg="red")
                rpm_label.config(bg="red", fg="white")
                speed_label.config(bg="red", fg="white")
                gear_label.config(bg="red", fg="white")
                tcs_label.config(bg="red")
                if tcs_active: tcs_label.config(fg="yellow")
            else:
                window.config(bg="#1e1e1e")
                rpm_label.config(bg="#1e1e1e", fg="#00ff00")
                speed_label.config(bg="#1e1e1e", fg="#00ffff")
                gear_label.config(bg="#1e1e1e", fg="orange")
                tcs_label.config(bg="#1e1e1e")
                if not tcs_active: tcs_label.config(fg="#444444")

    except BlockingIOError:
        pass

    window.after(10, update_telemetry)


window = tk.Tk()
window.title("Forza Race Engineer v1.0")
window.geometry("650x500")
window.config(bg="#1e1e1e")

rpm_label = tk.Label(window, text="RPM is waiting...", font=("Helvetica", 50, "bold"), bg="#1e1e1e", fg="white")
rpm_label.pack(pady=20)

speed_label = tk.Label(window, text="0 KM/H", font=("Helvetica", 40, "bold"), bg="#1e1e1e", fg="#00ffff")
speed_label.pack(pady=10)

gear_label = tk.Label(window, text="Gear: -", font=("Helvetica", 35, "bold"), bg="#1e1e1e", fg="orange")
gear_label.pack(pady=10)

tcs_label = tk.Label(window, text="• TCS ", font=("Helvetica", 25, "bold"), bg="#1e1e1e", fg="#444444")
tcs_label.pack(pady=20)

window.after(10, update_telemetry)
window.mainloop()