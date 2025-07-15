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
            prev_time = 0
            for i, click in enumerate(data):
                if stop_event.is_set():
                    print("Playback stopped by user.")
                    return
                delay = click['time'] - prev_time
                delay += random.uniform(-0.06, 0.06)
                delay = max(0, delay)
                # Move mouse to position 60ms before click
                if delay > 0.06:
                    time.sleep(delay - 0.06)
                    mouse_controller.position = (click['x'], click['y'])
                    time.sleep(0.06)
                else:
                    mouse_controller.position = (click['x'], click['y'])
                    time.sleep(delay)
                mouse_controller.press(Button.left)
                mouse_controller.release(Button.left)
                prev_time = click['time']
    finally:
        listener.stop()