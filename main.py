import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from recorder import MouseRecorder
from player import play_recording
from storage import save_to_file, load_from_file

recorder = MouseRecorder()
recorded_data = []

def start_recording():
    global recorded_data
    recorded_data = []
    recorder.start()
    status_label.config(text="Recording...")

def stop_recording():
    global recorded_data
    recorder.stop()
    recorded_data = recorder.get_recording()
    status_label.config(text=f"Recorded {len(recorded_data)} clicks")

def play():
    if not recorded_data:
        messagebox.showerror("Error", "No data to play.")
        return
    try:
        loops = int(loop_entry.get())
    except ValueError:
        loops = 1
    status_label.config(text="Playing...")
    play_recording(recorded_data, loop=loops)
    status_label.config(text="Playback done")

def save():
    if not recorded_data:
        messagebox.showerror("Error", "No data to save.")
        return
    file = filedialog.asksaveasfilename(defaultextension=".json")
    if file:
        save_to_file(file, recorded_data)
        status_label.config(text="Saved")

def load():
    global recorded_data
    file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file:
        recorded_data = load_from_file(file)
        status_label.config(text=f"Loaded {len(recorded_data)} clicks")

# Tkinter setup
root = tk.Tk()
root.title("Autoclicker")

tk.Button(root, text="Start Recording", command=start_recording).pack(pady=5)
tk.Button(root, text="Stop Recording", command=stop_recording).pack(pady=5)
tk.Button(root, text="Play", command=play).pack(pady=5)

tk.Label(root, text="Loops:").pack()
loop_entry = tk.Entry(root)
loop_entry.insert(0, "1")
loop_entry.pack(pady=5)

tk.Button(root, text="Save", command=save).pack(pady=5)
tk.Button(root, text="Load", command=load).pack(pady=5)

status_label = tk.Label(root, text="Idle")
status_label.pack(pady=10)

root.mainloop()
