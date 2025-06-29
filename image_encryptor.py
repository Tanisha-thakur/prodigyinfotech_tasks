import os
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk

# Ensure folders exist
os.makedirs("encrypted", exist_ok=True)
os.makedirs("decrypted", exist_ok=True)

# Create GUI
root = TkinterDnD.Tk()
root.title("Pixel Manipulation Encryption")
root.geometry("500x600")

# Title label
title = tk.Label(root, text="Pixel Manipulation Encryption", font=("Arial", 18, "bold"))
title.pack(pady=20)

# Key entry
key_label = tk.Label(root, text="Encryption Key:", font=("Arial", 12))
key_label.pack()
key_entry = tk.Entry(root, width=10)
key_entry.insert(0, "50")
key_entry.pack(pady=10)

# Image preview label
preview_label = tk.Label(root)
preview_label.pack(pady=10)

# Function to show image preview
def show_image_preview(path):
    img = Image.open(path)
    img = img.resize((250, 250))
    img_tk = ImageTk.PhotoImage(img)
    preview_label.configure(image=img_tk)
    preview_label.image = img_tk

# Encrypt image
def encrypt_image(path):
    try:
        key = int(key_entry.get())
        image = Image.open(path).convert("RGBA")
        pixels = image.load()

        for i in range(image.width):
            for j in range(image.height):
                r, g, b, a = pixels[i, j]
                pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256, a)

        encrypted_path = os.path.join("encrypted", os.path.basename(path).split('.')[0] + "_encrypted.png")
        image.save(encrypted_path)
        messagebox.showinfo("Success", f"Image encrypted and saved as {encrypted_path}")
        show_image_preview(encrypted_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Decrypt image
def decrypt_image(path):
    try:
        key = int(key_entry.get())
        image = Image.open(path).convert("RGBA")
        pixels = image.load()

        for i in range(image.width):
            for j in range(image.height):
                r, g, b, a = pixels[i, j]
                pixels[i, j] = ((r - key) % 256, (g - key) % 256, (b - key) % 256, a)

        decrypted_path = os.path.join("decrypted", os.path.basename(path).split('.')[0] + "_decrypted.png")
        image.save(decrypted_path)
        messagebox.showinfo("Success", f"Image decrypted and saved as {decrypted_path}")
        show_image_preview(decrypted_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# File select buttons
def select_file_and_encrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypt_image(file_path)

def select_file_and_decrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        decrypt_image(file_path)

encrypt_btn = tk.Button(root, text="Encrypt Image", bg="green", fg="white", width=20, command=select_file_and_encrypt)
encrypt_btn.pack(pady=10)

decrypt_btn = tk.Button(root, text="Decrypt Image", bg="dodgerblue", fg="white", width=20, command=select_file_and_decrypt)
decrypt_btn.pack(pady=10)

# Drag and drop area
drop_label = tk.Label(root, text="Drag & Drop an Image Here", relief="ridge", width=40, height=4, bg="lightgray")
drop_label.pack(pady=20)

def on_drop(event):
    file_path = event.data.strip('{}')
    encrypt_image(file_path)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
