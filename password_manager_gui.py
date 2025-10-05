import sqlite3
import hashlib
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

# ----------------- DATABASE SETUP -----------------
conn = sqlite3.connect("passwords_gui.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS master (
    id INTEGER PRIMARY KEY,
    password_hash TEXT,
    key TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS vault (
    id INTEGER PRIMARY KEY,
    website TEXT,
    username TEXT,
    password TEXT
)''')
conn.commit()

# ----------------- FUNCTIONS -----------------
def hash_master(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_master():
    root = tk.Tk()
    root.withdraw()  # hide root
    master_pwd = simpledialog.askstring("Setup", "Set Master Password:", show="*")
    root.destroy()
    if not master_pwd:
        messagebox.showerror("Error", "Master Password cannot be empty!")
        return
    hashed = hash_master(master_pwd)
    key = Fernet.generate_key()
    cursor.execute("INSERT INTO master (password_hash, key) VALUES (?, ?)", (hashed, key.decode()))
    conn.commit()
    messagebox.showinfo("Success", "Master Password created successfully!")

def verify_master():
    root = tk.Tk()
    root.withdraw()
    master_pwd = simpledialog.askstring("Login", "Enter Master Password:", show="*")
    root.destroy()
    cursor.execute("SELECT password_hash, key FROM master WHERE id=1")
    row = cursor.fetchone()
    if row and hash_master(master_pwd) == row[0]:
        return Fernet(row[1].encode())
    else:
        messagebox.showerror("Error", "Wrong Master Password!")
        return None
def add_password(cipher):
    website = simpledialog.askstring("Add Password", "Website:")
    username = simpledialog.askstring("Add Password", "Username:")
    pwd = simpledialog.askstring("Add Password", "Password:", show="*")
    if not (website and username and pwd):
        messagebox.showerror("Error", "All fields required!")
        return
    enc_pwd = cipher.encrypt(pwd.encode()).decode()
    cursor.execute("INSERT INTO vault (website, username, password) VALUES (?, ?, ?)", (website, username, enc_pwd))
    conn.commit()
    messagebox.showinfo("Success", "Password saved successfully!")

def view_passwords(cipher):
    cursor.execute("SELECT website, username, password FROM vault")
    rows = cursor.fetchall()
    if not rows:
        messagebox.showinfo("Info", "No passwords stored yet.")
    else:
        result = ""
        for row in rows:
            website, username, enc_pwd = row
            dec_pwd = cipher.decrypt(enc_pwd.encode()).decode()
            result += f"Website: {website}\nUsername: {username}\nPassword: {dec_pwd}\n\n"
        messagebox.showinfo("Stored Passwords", result)

# ----------------- GUI APP -----------------
def main_app(cipher):
    root = tk.Tk()
    root.title("Password Manager - Vishal")
    root.geometry("400x300")

    tk.Label(root, text="Password Manager", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Button(root, text="➕ Add New Password", command=lambda: add_password(cipher), width=30).pack(pady=10)
    tk.Button(root, text="🔑 View Stored Passwords", command=lambda: view_passwords(cipher), width=30).pack(pady=10)
    tk.Button(root, text="❌ Exit", command=root.quit, width=30).pack(pady=10)

    root.mainloop()

# ----------------- MAIN -----------------
cursor.execute("SELECT * FROM master")
if cursor.fetchone() is None:
    create_master()

cipher = verify_master()
if cipher:
    main_app(cipher)
