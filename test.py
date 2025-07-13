import bcrypt

password = "adminofthestuddybuddyy69283123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed.decode())  # This will give a string to store in .env

from dotenv import load_dotenv
load_dotenv()

import smtplib
import os

EMAIL_USER = "buddyystudy@gmail.com"  # Replace with your Gmail address
EMAIL_PASS = "uvsykimpqontxjma" # Replace with your App Password (no spaces if Google doesn't show them)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
    print("✅ Login successful! Your email and app password are valid.")
except Exception as e:
    print("❌ Login failed:", e)