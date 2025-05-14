import smtplib
from email.message import EmailMessage
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class EmailDispatcher:
    """
    Agent responsible for sending emails with attachments.

    For Gmail:
    1. Make sure "Less secure app access" is turned on in your Google account settings,
       or preferably, use an App Password:
       - Go to your Google Account > Security > 2-Step Verification > App passwords
       - Create a new app password and use it in the .env file
    2. If you're still having issues, check:
       - https://accounts.google.com/DisplayUnlockCaptcha
    """

    def __init__(self):
        """Initialize the EmailDispatcher."""
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))

        # Validate configuration
        if not all([self.email_address, self.email_password, self.smtp_server, self.smtp_port]):
            logger.warning("Email configuration incomplete. Check your .env file.")

    def send_email(self, subject, body, to, attachment_path=None):
        """
        Send an email with an optional attachment.

        Args:
            subject (str): Email subject
            body (str): Email body content
            to (str): Recipient email address
            attachment_path (str, optional): Path to file to attach

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.email_address
            msg['To'] = to
            msg.set_content(body)

            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                    msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)
            elif attachment_path:
                logger.warning(f"Attachment file not found: {attachment_path}")

            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)

            logger.info(f"Email sent successfully to {to}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
