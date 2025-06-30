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


def notify_buyer_and_seller(buyer_email, buyer_linkedin, seller_email, seller_linkedin):
    try:
        # Email to Seller
        seller_msg = EmailMessage()
        seller_msg['Subject'] = 'Student Buddy - New Purchase Notification'
        seller_msg['From'] = EMAIL_USER
        seller_msg['To'] = seller_email
        seller_msg.set_content(
            f"""
Hi Seller,

We have found a buyer for you. The admin will contact you soon on your registered mobile number.

Thank you,
Team BPIT Cart
            """.strip()
        )

        # Email to Buyer
        buyer_msg = EmailMessage()
        buyer_msg['Subject'] = 'Student Buddy - Purchase Confirmation'
        buyer_msg['From'] = EMAIL_USER
        buyer_msg['To'] = buyer_email
        buyer_msg.set_content(
            f"""
Hello Buyer,

Congratulations on purchasing the product on Student Buddy! 🎉
The admin will contact you soon with more details.

Thank you,
Team BPIT Cart
            """.strip()
        )

        # Send both emails using same connection
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(seller_msg)
            server.send_message(buyer_msg)

        return True

    except Exception as e:
        print("Error:", e)
        return False

def send_faulty_buyer_warning(email, fault_count):
    subject = 'Warning: Faulty Purchase Behavior Detected'
    body = f"""
Dear User,

You have been marked as a faulty buyer for a recent transaction. Your current fault count is {fault_count}.
If your fault count exceeds 7, your account will be terminated as per our policy.

If you believe this is a mistake, please contact support.

Thank you,
BPIT Cart Team
"""
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg.set_content(body)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print('Failed to send warning email:', e)
