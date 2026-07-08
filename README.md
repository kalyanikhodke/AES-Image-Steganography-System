# 🔐 AES Image Steganography System

## 📖 Project Overview

The **AES Image Steganography System** is a Python-based desktop application that securely hides confidential messages inside PNG images using **Least Significant Bit (LSB) Steganography** and **AES Encryption**. The application provides a user-friendly graphical interface built with Tkinter, allowing users to encrypt, embed, and retrieve secret messages with password protection.

---

## ✨ Features

- 🖼️ Hide secret messages inside PNG images
- 🔒 AES encryption for secure message protection
- 🔑 Password-based key generation using PBKDF2
- 🛡️ HMAC verification for data integrity
- 📂 Load messages directly from a text file
- 💬 Enter messages manually
- 🔓 Decode hidden messages from encoded images
- 🖥️ Easy-to-use graphical interface built with Tkinter

---

## 🛠️ Technologies Used

- Python 3
- Tkinter (GUI)
- Pillow (Image Processing)
- PyCryptodome (AES Encryption)
- Base64 Encoding
- HMAC (SHA-256)
- PBKDF2 Key Derivation
- LSB Image Steganography

---

## 📂 Project Structure

```
AES-Image-Steganography/
│── main.py
│── images/
│── README.md
│── requirements.txt
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/AES-Image-Steganography.git
```

### Install dependencies

```bash
pip install pillow pycryptodome
```

### Run the application

```bash
python main.py
```

---

## 🔄 Workflow

1. Select a PNG image.
2. Enter a secret message or load a text file.
3. Enter a secure password.
4. Encrypt and embed the message inside the image.
5. Save the encoded image.
6. Decode the hidden message using the correct password.

---

## 🔒 Security Features

- AES Encryption (EAX Mode)
- Password-Based Key Derivation (PBKDF2)
- HMAC-SHA256 Integrity Verification
- Base64 Encoding
- LSB Image Steganography

---

## 📸 Screenshots

You can add screenshots of:
- Home Screen
- Image Selection
- Message Encoding
- Message Decoding
- Output Window

---

## 📚 Concepts Used

- Cryptography
- Network Security
- Steganography
- GUI Programming
- File Handling
- Image Processing
- Data Integrity Verification

---

## 🔮 Future Enhancements

- Support JPEG and BMP images
- Drag-and-drop image upload
- Video steganography
- Audio steganography
- Stronger encryption options
- Multi-file support
- User authentication
- Dark/Light mode

---

## 👩‍💻 Author

**Kalyani Khodke**

Electronics & Telecommunication Engineering Student

Skills:
- Python
- Java
- SQL
- Network Security
- Cryptography
- Machine Learning

---

⭐ If you like this project, please give it a Star on GitHub!
