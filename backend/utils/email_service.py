import os
import smtplib
from email.mime.text import MIMEText


def send_reset_email(to_email, reset_link):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    # Safety check
    if not smtp_user or not smtp_pass:
        print("⚠ SMTP credentials missing. Printing reset link instead.")
        print("RESET LINK:", reset_link)
        return

    try:
        msg = MIMETextmsg = MIMEText(f"""
<h2>Password Reset</h2>
<p>You requested to reset your password.</p>
<p>
  <a href="{reset_link}"
     style="padding:10px 16px;background:#2563eb;color:white;
     text-decoration:none;border-radius:6px;">
     Reset Password
  </a>
</p>
<p>If you didn’t request this, ignore this email.</p>
""", "html")

        msg["Subject"] = "Password Reset"
        msg["From"] = smtp_user
        msg["To"] = to_email

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print("✅ Password reset email sent successfully")

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed (check Gmail App Password)")
        print("RESET LINK:", reset_link)

    except Exception as e:
        print("❌ Email sending failed:", e)
        print("RESET LINK:", reset_link)
