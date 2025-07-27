import bcrypt

password = "adminofthestuddybuddyy69283123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed.decode())  # This will give a string to store in .env

import smtplib

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = "buddyystudy@gmail.com"
EMAIL_PASS = "jkuxjlkpstzvrifz"

msg = MIMEMultipart()
msg['From'] = EMAIL_USER
msg['To'] = "kunalsharma7003@gmail.com"
msg['Subject'] = "Test Subject"

body = "This is a test email from Python."
msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        print("✅ Email sent successfully")
except Exception as e:
    print("❌ Failed to send email:", e)


