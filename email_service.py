import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_contact_email(name, email, message):
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

    msg = Mail(
        from_email=os.getenv("MAIL_DEFAULT_SENDER"),
        to_emails=os.getenv("MAIL_DEFAULT_SENDER"),
        subject=f"New contact message from {name}",
        html_content=f"""
        <h3>New Contact Message</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Message:</b><br>{message}</p>
        """
    )

    sg.send(msg)
