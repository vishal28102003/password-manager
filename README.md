# password-manager
🔐 Password Manager (CLI-Based)
A simple Password Manager built with Python that uses local encryption + master password for securing your credentials.
It runs in the terminal (no GUI) and stores data in an encrypted JSON file.

🚀 Features
Master password authentication 🔑
Add new credentials (service, username, password)
Retrieve saved credentials by service name
All passwords are stored encrypted (using cryptography.fernet)
Lightweight & runs directly from the terminal

🛠️ Tech Stack
Python 3
cryptography (Fernet) for AES encryption
JSON for storage

📂 Project Structure
password_manager.py   # Main script
master.key            # Encrypted master password (auto-generated)
passwords.json        # Encrypted password storage

▶️ How to Run

Clone the repo / download the script
Install required library:
pip install cryptography
Run the script:
python password_manager.py
On first run, set a master password

Use the menu to add / retrieve credentials

📸 Example Run
Password Manager
1. Add new credentials
2. Retrieve credentials
3. Exit
   
Choose an option: 1
Enter service name: Gmail
Enter username: testuser@gmail.com
Enter password: ********

Credentials saved successfully!

🔒 Security
Passwords are never stored in plain text
Encrypted using Fernet (AES) with a master key
Master password required for access

📌 Future Improvements
Add password generator
Export/import credentials with encryption
Multi-user support

👤 Author
Vishal Katiyar
📧 vishalkatiyar541@gmail.com

🌐 GitHub
 | LinkedIn
