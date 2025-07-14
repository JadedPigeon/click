from pynput.mouse import Controller, Button
from pynput import keyboard
import threading
import time
import random

mouse_controller = Controller()

def play_recording(data, loop=1):
    stop_event = threading.Event()

    def on_key(key):
        if key == keyboard.Key.esc:
            print("Escape pressed. Stopping playback.")
            stop_event.set()
            return False

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    try:
        for _ in range(loop):
            for i, click in enumerate(data):
                if stop_event.is_set():
                    print("Playback stopped by user.")
                    return
                if i > 0:
                    delay = click['time'] - data[i - 1]['time']
                    delay += random.uniform(-0.06, 0.06)
                    delay = max(0, delay)
                    time.sleep(delay)
                mouse_controller.position = (click['x'], click['y'])
                mouse_controller.press(Button.left)
                mouse_controller.release(Button.left)
    finally:
        listener.stop()