import smtplib
import random
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Use the correct static logo path
WEBSITE_LOGO_URL = "/static/images/icon3.png"  # Update yourdomain.com as needed
WEBSITE_NAME = "Campus Kart"
SUPPORT_EMAIL = EMAIL_USER


def generate_otp():
    return str(random.randint(100000, 999999))


def build_html_email(subject, heading, message, otp=None, button_url=None, button_text=None, action_url=None, action_text=None):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <title>{subject}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0; padding: 0;
            }}
            .container {{
                background-color: #ffffff;
                max-width: 600px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .email-header {{
                width: 100%;
                text-align: center;
                margin-bottom: 24px;
                padding-top: 10px;
                padding-bottom: 10px;
                background: #f5f8ff;
                border-radius: 8px 8px 0 0;
            }}
            .email-header img {{
                max-width: 90%;
                height: auto;
                border-radius: 8px;
                margin: 0 auto;
                display: block;
            }}
            .logo {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo img {{
                width: 120px;
                height: auto;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.6;
                color: #333333;
            }}
            .otp {{
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                background: #f0f0f0;
                padding: 10px 20px;
                display: inline-block;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #007bff;
                color: #ffffff !important;
                text-decoration: none;
                border-radius: 4px;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="email-header">
                <img src="/static/images/banner.png" alt="Campus Kart Banner" />
            </div>
            <div class="logo">
                <img src="{WEBSITE_LOGO_URL}" alt="{WEBSITE_NAME} Logo" />
            </div>
            <div class="content">
                <h2>{heading}</h2>
                <p>{message}</p>
    """

    if otp:
        html_content += f"""
                <p class="otp">{otp}</p>
        """

    if button_url and button_text:
        html_content += f"""
                <p style="text-align: center;">
                    <a href="{button_url}" class="button">{button_text}</a>
                </p>
        """

    # Add cornflowerblue action button at the end if provided
    if action_url and action_text:
        html_content += f"""
            <p style="text-align: center; margin-top: 32px;">
                <a href="{action_url}" style="display:inline-block;padding:14px 32px;background-color:cornflowerblue;color:#fff !important;text-decoration:none;border-radius:6px;font-size:17px;font-weight:600;">{action_text}</a>
            </p>
        """

    html_content += f"""
                <p>Thank you,<br />The {WEBSITE_NAME} Team</p>
            </div>
            <div class="footer">
                &copy; {WEBSITE_NAME} | This is an automated message. If you need help, contact us at {SUPPORT_EMAIL}.
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def send_otp(email, otp):
    msg = EmailMessage()
    msg['Subject'] = f'Your Verification Code - {WEBSITE_NAME}'
    msg['From'] = EMAIL_USER
    msg['To'] = email

    heading = "Your OTP Code"
    message = "Use the code below to verify your account. It is valid for 10 minutes."

    # Add a dashboard/profile button for after verification
    action_url = "http://localhost:5000/profile"  # Change to your deployed dashboard/profile URL
    action_text = "Go to Your Dashboard"

    msg.set_content(f"Your OTP is: {otp}")
    msg.add_alternative(build_html_email(msg['Subject'], heading, message, otp=otp, action_url=action_url, action_text=action_text), subtype='html')

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
        # Seller email
        seller_subject = f'{WEBSITE_NAME} - New Purchase Notification'
        seller_heading = "You Have a New Buyer!"
        seller_message = f"""
Hi Seller,<br><br>
We have found a buyer for your product. Our admin will contact you soon on your registered mobile number.<br><br>
<b>Buyer LinkedIn:</b> {buyer_linkedin}<br><br>
"""
        seller_action_url = "http://localhost:5000/profile"  # Seller dashboard/profile
        seller_action_text = "View Your Dashboard"

        seller_msg = EmailMessage()
        seller_msg['Subject'] = seller_subject
        seller_msg['From'] = EMAIL_USER
        seller_msg['To'] = seller_email
        seller_msg.set_content("A buyer has been found for your product.")
        seller_msg.add_alternative(build_html_email(seller_subject, seller_heading, seller_message, action_url=seller_action_url, action_text=seller_action_text), subtype='html')

        # Buyer email
        buyer_subject = f'{WEBSITE_NAME} - Purchase Confirmation'
        buyer_heading = "Congratulations on Your Purchase!"
        buyer_message = f"""
Hello Buyer,<br><br>
Thank you for your purchase on {WEBSITE_NAME}! 🎉<br>
Our admin will contact you soon with more details.<br><br>
<b>Seller LinkedIn:</b> {seller_linkedin}<br><br>
"""
        buyer_action_url = "http://localhost:5000/profile"  # Buyer dashboard/profile
        buyer_action_text = "View Your Profile"

        buyer_msg = EmailMessage()
        buyer_msg['Subject'] = buyer_subject
        buyer_msg['From'] = EMAIL_USER
        buyer_msg['To'] = buyer_email
        buyer_msg.set_content("Thank you for your purchase.")
        buyer_msg.add_alternative(build_html_email(buyer_subject, buyer_heading, buyer_message, action_url=buyer_action_url, action_text=buyer_action_text), subtype='html')

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
    heading = "Account Warning Notice"
    message = f"""
Dear User,<br><br>
You have been marked as a faulty buyer for a recent transaction. Your current fault count is <b>{fault_count}</b>.<br>
If your fault count exceeds 7, your account will be permanently deactivated as per our policy.<br><br>
If you believe this is an error, please contact our support team.<br><br>
"""
    action_url = "http://localhost:5000/profile"  # Or a support/contact page
    action_text = "View Your Account"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg.set_content(f"Your current fault count is {fault_count}.")
    msg.add_alternative(build_html_email(subject, heading, message, action_url=action_url, action_text=action_text), subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print('Failed to send warning email:', e)
