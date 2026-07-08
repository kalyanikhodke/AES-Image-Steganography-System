import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64, hmac, hashlib


def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=100000)

def make_hmac(key, data):
    return hmac.new(key, data.encode(), hashlib.sha256).hexdigest()


def can_fit(image_path, data_len):
    img = Image.open(image_path)
    capacity = (img.size[0] * img.size[1] * 3) // 8
    return data_len < capacity

def encode_image(image_path, data, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    data += "###"
    binary_data = ''.join(format(ord(i), '08b') for i in data)

    idx = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(pixels[i, j])
            for k in range(3):
                if idx < len(binary_data):
                    pixel[k] = pixel[k] & ~1 | int(binary_data[idx])
                    idx += 1
            pixels[i, j] = tuple(pixel)

    img.save(output_path)

def decode_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    binary_data = ""
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in range(3):
                binary_data += str(pixels[i, j][k] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    data = ""

    for byte in all_bytes:
        data += chr(int(byte, 2))
        if data.endswith("###"):
            return data[:-3]
    return ""

image_path = ""
file_path = ""


def toggle_input():
    if input_mode.get() == "file":
        message_entry.config(state="disabled")
    else:
        message_entry.config(state="normal")

def select_image():
    global image_path, img1
    image_path = filedialog.askopenfilename(filetypes=[("PNG files","*.png")])

    if not image_path:
        messagebox.showwarning("Warning", "Please select an image!")
        return

    img = Image.open(image_path).resize((220,160))
    img1 = ImageTk.PhotoImage(img)
    original_image_label.config(image=img1)
    path_label.config(text=image_path)

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])

    if not file_path:
        messagebox.showwarning("Warning", "Please select a text file!")
        return

    file_label.config(text=file_path)

def encode_message():
    global file_path

    if not image_path:
        messagebox.showwarning("Warning", "Please select an image first!")
        return

    password = password_entry.get()
    if not password:
        messagebox.showwarning("Warning", "Please enter password!")
        return

    # -------- INPUT MODE --------
    if input_mode.get() == "text":
        message = message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message!")
            return

    else:  # FILE MODE
        if not file_path:
            messagebox.showwarning("Warning", "Please select a text file!")
            return

        with open(file_path, "r") as file:
            message = file.read()

    # -------- ENCRYPTION --------
    salt = get_random_bytes(16)
    key = derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    data = base64.b64encode(salt + cipher.nonce + ciphertext).decode()
    mac = make_hmac(key, data)
    final_data = data + "|" + mac

    if not can_fit(image_path, len(final_data)):
        messagebox.showerror("Error", "Message too large!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png")

    if not save_path:
        messagebox.showwarning("Warning", "Please choose save location!")
        return

    encode_image(image_path, final_data, save_path)

    img = Image.open(save_path).resize((220,160))
    global img2
    img2 = ImageTk.PhotoImage(img)
    encoded_image_label.config(image=img2)

    messagebox.showinfo("Success", "Message encoded successfully!")

def decode_message():
    file_path_img = filedialog.askopenfilename(filetypes=[("PNG files","*.png")])

    if not file_path_img:
        messagebox.showwarning("Warning", "Please select an image!")
        return

    password = password_entry.get()
    if not password:
        messagebox.showwarning("Warning", "Please enter password!")
        return

    data = decode_image(file_path_img)

    try:
        enc, mac = data.split("|")
    except:
        messagebox.showerror("Error", "No hidden data found!")
        return

    raw = base64.b64decode(enc)
    salt = raw[:16]
    nonce = raw[16:32]
    ciphertext = raw[32:]

    key = derive_key(password, salt)

    if make_hmac(key, enc) != mac:
        messagebox.showerror("Error", "Data integrity failed!")
        return

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext).decode()

    result_label.config(text="Decrypted Message:\n" + decrypted)


root = tk.Tk()
root.title("Network Security Project - AES Image Steganography")
root.geometry("750x650")
root.configure(bg="#1e1e1e")

# Title
tk.Label(root, text="🔐 Network Security Project",
         font=("Arial",18,"bold"),
         bg="#1e1e1e", fg="white").pack(pady=10)

tk.Label(root, text="AES Image Steganography System",
         font=("Arial",12),
         bg="#1e1e1e", fg="lightgray").pack()

# Image Frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

original_image_label = tk.Label(frame, bg="#1e1e1e")
original_image_label.pack(side="left", padx=20)

encoded_image_label = tk.Label(frame, bg="#1e1e1e")
encoded_image_label.pack(side="right", padx=20)

# Buttons
tk.Button(root, text="Select Image", command=select_image,
          bg="#333333", fg="white", width=20).pack(pady=5)

path_label = tk.Label(root, text="No image selected",
                      bg="#1e1e1e", fg="lightgray")
path_label.pack()

# Input Mode
input_mode = tk.StringVar(value="text")

tk.Label(root, text="Select Input Type",
         bg="#1e1e1e", fg="white").pack()

tk.Radiobutton(root, text="Enter Message",
               variable=input_mode, value="text",
               command=toggle_input,
               bg="#1e1e1e", fg="white", selectcolor="#333333").pack()

tk.Radiobutton(root, text="Load from File",
               variable=input_mode, value="file",
               command=toggle_input,
               bg="#1e1e1e", fg="white", selectcolor="#333333").pack()

# File selection
tk.Button(root, text="Select Text File", command=select_file,
          bg="#444444", fg="white", width=20).pack(pady=5)

file_label = tk.Label(root, text="No file selected",
                      bg="#1e1e1e", fg="lightgray")
file_label.pack()

# Message
tk.Label(root, text="Enter Message",
         bg="#1e1e1e", fg="white").pack()

message_entry = tk.Entry(root, width=60,
                         bg="#2d2d2d", fg="white")
message_entry.pack(pady=5)

# Password
tk.Label(root, text="Enter Password",
         bg="#1e1e1e", fg="white").pack()

password_entry = tk.Entry(root, show="*", width=60,
                          bg="#2d2d2d", fg="white")
password_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Encode Message", command=encode_message,
          bg="#4CAF50", fg="white", width=25).pack(pady=10)

tk.Button(root, text="Decode Message", command=decode_message,
          bg="#2196F3", fg="white", width=25).pack()

# Result
result_label = tk.Label(root, text="",
                        bg="#1e1e1e", fg="lightgreen",
                        font=("Arial",11))
result_label.pack(pady=20)

root.mainloop()
