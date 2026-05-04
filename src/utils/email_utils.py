import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json


def build_html_table(dq_report: dict) -> str:
    """Convert DQ report into HTML table"""
    rows = ""
    for k, v in dq_report.items():
        rows += f"<tr><td>{k}</td><td>{v}</td></tr>"

    return f"""
    <html>
        <body>
            <h3>DQ Report</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                {rows}
            </table>
            <br>
            <p>Thank You,<br><b>ETL</b></p>
        </body>
    </html>
    """


def send_dq_email(dq_report, sender_email, receiver_email, password):
    """
    Sends DQ report via email with HTML + plain fallback
    """

    # 🔹 Subject
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"DQ Report - {today}"

    # 🔹 Signature
    signature = "\n\nThank You,\nETL"

    # 🔹 Content
    plain_body = json.dumps(dq_report, indent=4) + signature
    html_body = build_html_table(dq_report)

    # 🔹 Email object
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

        print("📧 DQ report email sent successfully")

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        raise