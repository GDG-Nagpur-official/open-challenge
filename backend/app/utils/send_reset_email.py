from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_reset_email(to_email, reset_url):
    message = Mail(
        from_email='no-reply@api-management-system.com',
        to_emails=to_email,
        subject='Reset Your Password',
        html_content=f'''
            <h3>Password Reset</h3>
            <p>This link is valid for 1 hour.</p>
            <a href="{reset_url}">Reset Password</a>
        '''
    )

    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    sg.send(message)
