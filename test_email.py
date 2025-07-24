import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Test Email from Campus Kart'
msg['From'] = EMAIL_USER
msg['To'] = 'kunalsharma7003@gmail.com'  # send to self for test
msg.set_content('This is a test email from your Campus Kart project.')

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    print('Email sent successfully!')
except Exception as e:
    print('Failed to send email:', e)
