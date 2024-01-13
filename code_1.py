import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

class SecureMessagingApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Secure Messaging App")

        # Generate or load the key for encryption
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)

        self.create_gui()

    def load_or_generate_key(self):
        # Load the key if it exists, or generate a new one
        key_file = "encryption_key.key"
        try:
            with open(key_file, "rb") as key_file:
                key = key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(key_file, "wb") as key_file:
                key_file.write(key)
        return key

    def create_gui(self):
        # Create GUI components
        self.message_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.message_entry = tk.Entry(self.root, width=40)
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)

        # Arrange GUI components
        self.message_display.pack(pady=10)
        self.message_entry.pack(pady=5)
        self.send_button.pack(pady=10)

    def send_message(self):
        message = self.message_entry.get()
        try:
            encrypted_message = self.encrypt_message(message)
            self.display_message(f"Encrypted: {encrypted_message}")

            decrypted_message = self.decrypt_message(encrypted_message)
            self.display_message(f"Decrypted: {decrypted_message}")
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def encrypt_message(self, message):
        # Encrypt the message using Fernet symmetric encryption
        encrypted_message = self.cipher.encrypt(message.encode())
        return encrypted_message.decode()

    def decrypt_message(self, encrypted_message):
        # Decrypt the message using Fernet symmetric encryption
        decrypted_message = self.cipher.decrypt(encrypted_message.encode())
        return decrypted_message.decode()

    def display_message(self, message):
        self.message_display.insert(tk.END, f"{message}\n")
        self.message_entry.delete(0, tk.END)

if __name__ == "_main_":
    root = tk.Tk()
    app = SecureMessagingApp(root)
    root.mainloop()