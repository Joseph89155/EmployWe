# email_utils.py
import smtplib
from email.message import EmailMessage

# Replace these with your actual email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "youremail@gmail.com"        # Use your email
EMAIL_PASSWORD = "yourapppassword"           # Use an App Password for Gmail

def send_onboarding_email(to_email, username, role):
    msg = EmailMessage()
    msg['Subject'] = 'Welcome to the Company!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    msg.set_content(f"""
Hi {username},

Welcome aboard! Your role as '{role}' has been successfully registered in our system.

We're excited to have you on the team.

Regards,
HR Department
EmployWe
""")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
