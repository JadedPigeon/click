from pynput import mouse, keyboard
import threading
import time

class MouseRecorder:
    def __init__(self):
        self.recording = []
        self._mouse_listener = None
        self._keyboard_listener = None
        self._start_time = None
        self._listener_thread = None
        self._stop_event = threading.Event()

    def _on_click(self, x, y, button, pressed):
        if button.name == 'left' and pressed:
            timestamp = time.time() - self._start_time
            self.recording.append({'x': x, 'y': y, 'time': timestamp})
            print(f"Recorded click at ({x}, {y}) at time {timestamp:.2f}")

    def _on_key(self, key):
        if key == keyboard.Key.esc:
            print("Escape pressed. Stopping recording.")
            self.stop()
            return False

    def _run_listeners(self):
        self._mouse_listener = mouse.Listener(on_click=self._on_click)
        self._keyboard_listener = keyboard.Listener(on_press=self._on_key)
        self._mouse_listener.start()
        self._keyboard_listener.start()
        self._mouse_listener.join()
        self._keyboard_listener.join()

    def start(self):
        self.recording = []
        self._start_time = time.time()
        self._stop_event.clear()
        self._listener_thread = threading.Thread(target=self._run_listeners, daemon=True)
        self._listener_thread.start()
        print("Recording started... (Press ESC to stop)")

    def stop(self):
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None
        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None
        print("Recording stopped.")

    def get_recording(self):
        return self.recording