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
Hello Seller,

Your product has been purchased on Student Buddy.

Buyer Details:
Email: {buyer_email}
LinkedIn: {buyer_linkedin}

Please note:
If you do not update the payment status of this product within 7 days, your account will be banned from our platform.

Thank you,
Team Student Buddy
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

You have successfully initiated a purchase on Student Buddy.

Seller Details:
Email: {seller_email}
LinkedIn: {seller_linkedin}

You can reach out to the seller for further coordination.

Thank you,
Team Student Buddy
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
