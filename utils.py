import smtplib
import random
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def send_otp(email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code - Student Buddy'
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg.set_content(f"Your OTP code is: {otp}. It is valid for 10 minutes.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Error:", e)
        return False
