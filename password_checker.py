import re
import tkinter as tk
from tkinter import messagebox, font
import random
import string

# Function to evaluate password strength
def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    return score

# Function to update feedback and bar in real-time
def update_feedback(event=None):
    password = entry.get()
    score = check_password_strength(password)
    colors = ["#ff4d4d", "#ff944d", "#ffff4d", "#b3ff66", "#33cc33"] 
    messages = [
        "Very Weak", "Weak", "Moderate", "Strong", "Very Strong"
    ]
    theme = current_theme()
    bar_canvas.config(bg=colors[score-1] if score else theme['canvas_bg'])
    bar_canvas.coords(bar, 0, 0, score * 60, 20)
    result_label.config(text=messages[score-1] if score else "Too Short")

# Save password if strong
def save_password():
    password = entry.get()
    if check_password_strength(password) >= 4:
        with open("strong_passwords.txt", "a") as f:
            f.write(password + "\n")
        messagebox.showinfo("Saved", "Password saved to file.")
    else:
        messagebox.showwarning("Not Strong Enough", "Improve password strength before saving.")

# Toggle password visibility
def toggle_visibility():
    if entry.cget('show') == '':
        entry.config(show='*')
        toggle_btn.config(text="Show")
    else:
        entry.config(show='')
        toggle_btn.config(text="Hide")

# Password generator
def generate_password():
    length = 12
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_chars) for _ in range(length))
    entry.delete(0, tk.END)
    entry.insert(0, password)
    update_feedback()

# Dark mode theme
def enable_dark_mode():
    apply_theme(dark_mode)

# Light mode theme
def enable_light_mode():
    apply_theme(light_mode)

# Theme switcher logic
def toggle_theme():
    global is_dark
    is_dark = not is_dark
    if is_dark:
        enable_dark_mode()
        theme_btn.config(text="Light Mode")
    else:
        enable_light_mode()
        theme_btn.config(text="Dark Mode")

def apply_theme(theme):
    root.configure(bg=theme['bg'])
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type in ['Label', 'Button', 'Frame', 'Canvas']:
            widget.configure(bg=theme['bg'], fg=theme['fg'])
        if widget_type == 'Entry':
            widget.configure(bg=theme['entry_bg'], fg=theme['fg'], insertbackground=theme['fg'])
    result_label.configure(bg=theme['bg'])
    bar_canvas.configure(bg=theme['canvas_bg'])

def current_theme():
    return dark_mode if is_dark else light_mode

# Themes
dark_mode = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "entry_bg": "#2e2e2e",
    "canvas_bg": "#3e3e3e"
}

light_mode = {
    "bg": "#ffffff",
    "fg": "#000000",
    "entry_bg": "#f0f0f0",
    "canvas_bg": "#dddddd"
}

# Initial GUI setup
is_dark = True
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x380")

label_font = font.Font(family="Segoe UI", size=11)
title_font = font.Font(family="Helvetica", size=16, weight="bold")

# Widgets
theme = current_theme()
root.configure(bg=theme['bg'])

header = tk.Label(root, text="Password Strength Checker", font=title_font, bg=theme['bg'], fg=theme['fg'])
header.pack(pady=10)

entry_frame = tk.Frame(root, bg=theme['bg'])
entry_frame.pack()

entry = tk.Entry(entry_frame, font=("Consolas", 12), show='*', width=25, bg=theme['entry_bg'], fg=theme['fg'], insertbackground=theme['fg'])
entry.pack(side='left', padx=(10,0))
entry.bind("<KeyRelease>", update_feedback)

toggle_btn = tk.Button(entry_frame, text="Show", command=toggle_visibility, bg=theme['bg'], fg=theme['fg'])
toggle_btn.pack(side='left', padx=10)

generate_btn = tk.Button(root, text="Generate Password", command=generate_password, bg="#607D8B", fg="white")
generate_btn.pack(pady=5)

bar_canvas = tk.Canvas(root, width=300, height=20, bg=theme['canvas_bg'], highlightthickness=0)
bar_canvas.pack(pady=10)
bar = bar_canvas.create_rectangle(0, 0, 0, 20, fill="")

result_label = tk.Label(root, text="", font=label_font, bg=theme['bg'], fg=theme['fg'])
result_label.pack(pady=5)

save_btn = tk.Button(root, text="Save Password", bg="#4CAF50", fg="white", command=save_password)
save_btn.pack(pady=5)

theme_btn = tk.Button(root, text="Light Mode", bg="#3f51b5", fg="white", command=toggle_theme)
theme_btn.pack(pady=10)

root.mainloop()
