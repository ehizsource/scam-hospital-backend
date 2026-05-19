import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = "noreply@scamehospital.com"


def send_email(to_email: str, subject: str, html_body: str):
    if not SMTP_USER or not SMTP_PASS:
        print(f"Email skipped because SMTP credentials are not configured. To: {to_email}, Subject: {subject}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())


def send_received_email(name: str, email: str, scam_type: str):
    subject = "We received your case — ScameHospital"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f0f4f8; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; padding: 40px;">
            <h1 style="color: #0a1628;">Scame<span style="color: #00d4ff;">Hospital</span></h1>
            <h2 style="color: #0a1628;">We've Received Your Request ✅</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>Thank you for reaching out. We have received your submission regarding
               a <strong>{scam_type}</strong> and our team is reviewing your case.</p>
            <div style="background: #f0f9ff; border-left: 4px solid #00d4ff;
                        padding: 15px 20px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 0; color: #0066cc; font-weight: 600;">What happens next?</p>
                <p style="margin: 10px 0 0; color: #555; font-size: 14px;">
                    Once you complete your payment, you will receive a confirmation
                    email with your Google Meet session link.
                </p>
            </div>
            <p>Questions? Contact us at
               <a href="mailto:help@scamehospital.com" style="color: #00d4ff;">
               help@scamehospital.com</a>
            </p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;"/>
            <p style="color: #aaa; font-size: 12px; text-align: center;">
                This is an automated message. Please do not reply.<br/>
                © 2026 ScameHospital. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, body)


def send_confirmation_email(
    name: str,
    email: str,
    package: str,
    date: str,
    time: str,
    meet_link: str,
    client_time: Optional[str] = None,
    client_timezone: Optional[str] = None,
):
    client_time_row = ""
    if client_time:
        timezone_note = f" ({client_timezone})" if client_timezone else ""
        client_time_row = f"""
                    <tr>
                        <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Client Local Time</td>
                        <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{client_time}{timezone_note}</td>
                    </tr>
        """

    subject = "Booking Confirmed — ScameHospital 🎉"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f0f4f8; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; padding: 40px;">
            <h1 style="color: #0a1628;">Scame<span style="color: #00d4ff;">Hospital</span></h1>
            <h2 style="color: #0a1628;">Booking Confirmed 🎉</h2>
            <p>Hi <strong>{name}</strong>, your payment was successful and your session is confirmed.</p>
            <div style="background: #f0f9ff; border-radius: 12px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #0066cc; margin-top: 0;">Session Details</h3>
                <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                    <tr>
                        <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Package</td>
                        <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{package}</td>
                    </tr>
                    <tr>
                        <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Date</td>
                        <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{date}</td>
                    </tr>
                    <tr>
                        <td style="color: #888; padding: 10px 0;">Time</td>
                        <td style="font-weight: 600; color: #0a1628;">{time}</td>
                    </tr>
                    {client_time_row}
                </table>
            </div>
            <div style="background: linear-gradient(135deg, #0a1628, #1a2a4a);
                        border-radius: 12px; padding: 25px; text-align: center; margin: 25px 0;">
                <p style="color: rgba(255,255,255,0.7); margin: 0 0 15px;">Click below to join your session</p>
                <a href="{meet_link}"
                   style="background: #00d4ff; color: #0a1628; padding: 14px 35px;
                          border-radius: 25px; text-decoration: none; font-weight: 700;
                          font-size: 15px; display: inline-block;">
                    Join Google Meet Session
                </a>
                <p style="color: rgba(255,255,255,0.3); font-size: 11px; margin: 15px 0 0;">
                    {meet_link}
                </p>
            </div>
            <div style="background: #e8f5e9; border-radius: 10px; padding: 15px 20px; font-size: 13px;">
                <strong style="color: #2e7d32;">Important Reminders:</strong>
                <ul style="margin: 10px 0 0; padding-left: 18px; line-height: 1.8;">
                    <li>A reminder will be sent 24 hours before your session</li>
                    <li>Join the meeting 5 minutes early</li>
                    <li>Have any relevant documents ready to share</li>
                    <li>Be in a quiet, private location</li>
                </ul>
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;"/>
            <p style="color: #aaa; font-size: 12px; text-align: center;">
                Need help? <a href="mailto:help@scamehospital.com" style="color: #00d4ff;">
                help@scamehospital.com</a><br/>
                © 2026 ScameHospital. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, body)
def send_admin_notification(admin_email: str, name: str, email: str, scam_type: str, package: str, date: str, time: str):
    subject = f"New Booking — {name} ({package})"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f0f4f8; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; padding: 40px;">
            <h1 style="color: #0a1628;">Scame<span style="color: #00d4ff;">Hospital</span></h1>
            <h2 style="color: #0a1628;">New Booking Received 🔔</h2>
            <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                <tr>
                    <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Name</td>
                    <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{name}</td>
                </tr>
                <tr>
                    <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Email</td>
                    <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{email}</td>
                </tr>
                <tr>
                    <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Scam Type</td>
                    <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{scam_type}</td>
                </tr>
                <tr>
                    <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Package</td>
                    <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{package}</td>
                </tr>
                <tr>
                    <td style="color: #888; padding: 10px 0; border-bottom: 1px solid #eee;">Date</td>
                    <td style="font-weight: 600; color: #0a1628; border-bottom: 1px solid #eee;">{date}</td>
                </tr>
                <tr>
                    <td style="color: #888; padding: 10px 0;">Time</td>
                    <td style="font-weight: 600; color: #0a1628;">{time}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    send_emailsend_email(admin_email, subject, body)