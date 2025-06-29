import tkinter as tk
from tkinter import messagebox, filedialog, font

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def on_encrypt():
    try:
        shift = int(shift_entry.get())
        text = input_text.get("1.0", tk.END).strip()
        result = caesar_cipher(text, shift, mode='encrypt')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for shift.") 

def on_decrypt():
    try:
        shift = int(shift_entry.get())
        text = input_text.get("1.0", tk.END).strip()
        result = caesar_cipher(text, shift, mode='decrypt')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for shift.")

def copy_to_clipboard():
    result = output_text.get("1.0", tk.END).strip()
    if result:
        window.clipboard_clear()
        window.clipboard_append(result)
        messagebox.showinfo("Copied", "Result copied to clipboard!")

def save_to_file():
    result = output_text.get("1.0", tk.END).strip()
    if not result:
        messagebox.showwarning("Empty", "There's no result to save!")
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if filepath:
        with open(filepath, "w") as file:
            file.write(result)
        messagebox.showinfo("Saved", f"Result saved to {filepath}")

# ========== GUI Setup ==========
window = tk.Tk()
window.title("🔐 Caesar Cipher Tool")
window.geometry("550x580")
window.config(padx=15, pady=15, bg="#f8f1f0")  # Light gray-blue background

# Custom fonts
title_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Verdana", size=10)

# Title
tk.Label(window, text="Caesar Cipher Tool", bg="#f8f0f0", font=title_font, fg="#333").pack(pady=10)

# Input section
tk.Label(window, text="🔤 Enter Message:", bg="#f8f0f0", font=label_font, fg="#333").pack(anchor='w')
input_text = tk.Text(window, height=5, font=("Consolas", 11), bg="#ffffff")
input_text.pack(fill='x', pady=5)

tk.Label(window, text="🔁 Shift Value:", bg="#f0f4f8", font=label_font, fg="#333").pack(anchor='w', pady=(10, 0))
shift_entry = tk.Entry(window, font=("Segoe UI", 11), bg="#ffffff")
shift_entry.pack(fill='x', pady=5)

# Action buttons
btn_frame = tk.Frame(window, bg="#f0f4f8")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Encrypt", width=12, font=button_font, bg="#4CAF50", fg="white",
          activebackground="#45a049", command=on_encrypt).pack(side='left', padx=10)

tk.Button(btn_frame, text="Decrypt", width=12, font=button_font, bg="#2196F3", fg="white",
          activebackground="#1e88e5", command=on_decrypt).pack(side='left', padx=10)

# Output section
tk.Label(window, text="📄 Result:", bg="#f0f4f8", font=label_font, fg="#333").pack(anchor='w', pady=(10, 0))
output_text = tk.Text(window, height=5, font=("Consolas", 11), bg="#fff9c4")  # Light yellow for output
output_text.pack(fill='x', pady=5)

# Extra buttons
extra_frame = tk.Frame(window, bg="#f0f4f8")
extra_frame.pack(pady=10)

tk.Button(extra_frame, text="📋 Copy to Clipboard", width=18, font=button_font, bg="#9C27B0", fg="white",
          activebackground="#8e24aa", command=copy_to_clipboard).pack(side='left', padx=8)

tk.Button(extra_frame, text="💾 Save to File", width=18, font=button_font, bg="#FF5722", fg="white",
          activebackground="#e64a19", command=save_to_file).pack(side='left', padx=8)

window.mainloop()

