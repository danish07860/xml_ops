import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json


def send_dq_email(dq_report, sender_email, receiver_email, password):
    # 🔹 Subject with date
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"DQ Report - {today}"

    # 🔹 Convert report to pretty JSON
    body = json.dumps(dq_report, indent=4)

    # 🔹 Email setup
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # 🔹 Send email (Gmail example)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

    print("📧 DQ report email sent!")