import base64
from datetime import datetime

import pyotp
from mailjet_rest import Client
from passlib.context import CryptContext

from app.settings.settings import Settings

settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mailjet = Client(
    auth=(settings.email_api_key, settings.email_api_secret), version="v3.1"
)


class generateKey:
    @staticmethod
    def return_value(phone, email):
        return f"{phone}-{email}{datetime.date(datetime.now())}{settings.secret_key}"


def send_email(receiver: str, sender: str, subject: str, text: str, html: str):
    """Sends an email to the provided recipient.

    Args:
        receiver (str): The recipient's email address.
        sender (str): The sender's email address.
        subject (str): The email subject.
        text (str): The email body in text format.
        html (str): The email body in HTML format.
    """
    data = {
        "Messages": [
            {
                "From": {
                    "Email": sender,
                },
                "To": [
                    {
                        "Email": receiver,
                    }
                ],
                "Subject": subject,
                "TextPart": text,
                "HTMLPart": html,
                "CustomID": "AppGettingStartedTest",
            }
        ]
    }
    return mailjet.send.create(data=data)


def generate_otp(org_id, email):
    """Generates a 6-digit OTP for organization invite.

    Args:
        org_id (int): The organization ID.
        email (EmailStr): the email of the user to be encoded

    Returns:
        str: The generated OTP.
    """
    keygen = generateKey()
    key_bytes = keygen.return_value(org_id, email).encode()
    return base64.b32encode(key_bytes).decode("utf-8")


class OTPVerificationMixin:
    """A mixin class for OTP verification."""

    @staticmethod
    def generate_key(org_id, email):
        """Generates a 6-digit OTP for organization invite.

        Args:
            org_id (int): The organization ID.
            email (EmailStr): the email of the user to be encoded

        Returns:
            str: The generated OTP.
        """
        keygen = generateKey()
        key_bytes = keygen.return_value(org_id, email).encode()
        return base64.b32encode(key_bytes).decode("utf-8")

    def verify_otp(self, otp, org_id, email):
        """Verifies the provided OTP.

        Args:
            otp (str): The provided OTP.
            org_id (int): The organization ID.
            email (str): user email.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        key = self.generate_key(org_id, email)
        OTP = pyotp.TOTP(key, interval=int(settings.OTP_INTERVAL))
        return OTP.verify(otp)


def generate_otp_link(org_id):
    """Generates a link for organization invite.

    Args:
        org_id (int): The organization ID.

    Returns:
        str: The generated link.
    """
    return f"{settings.FRONTEND_URL}/invite/{org_id}"


def send_otp_to_email(sender, email, org_id, org_name):
    """Sends an OTP to the provided email address.

    Args:
        email (str): The recipient's email address.
        sender (str): The sender's email address.
        org_name (str): The organization name.
        org_id (int): The organization ID.
    """
    key = generate_otp(org_id, email)
    OTP = pyotp.TOTP(key, interval=int(settings.OTP_INTERVAL))
    otp = OTP.now()
    subject = f"Invitation to join {org_name} organization"

    # Create the HTML content for the email with inline CSS styles
    html_content = f"""
    <html>
    <head>
        <style>
            /* Add your inline CSS styles here */
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            .message {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .otp {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="message">Hello,</p>
            <p class="message">You have been invited to join the {org_name} organization.</p>
            <p class="message">Your OTP (One-Time Password) for authentication is: <span class="otp">{otp}</span></p>
            <p class="message">Please use this OTP to complete your registration.</p>
            <p class="message">Thank you!</p>
        </div>
    </body>
    </html>
    """

    # Call the send_email function to send the email
    return (
        send_email(email, "sanctuspeter@gmail.com", subject, "", html_content),
        otp,
    )


def send_forget_password_email(email, otp_var):
    """Sends a password reset link to the provided email address.

    Args:
        email (str): The recipient's email address.
        otp_var (str): The OTP.
    """
    key = generate_otp(1024, email)
    OTP = pyotp.TOTP(key, interval=int(settings.OTP_INTERVAL))
    otp = OTP.now()
    subject = "Password reset link"
    html_content = f"""
    <html>
    <head>
        <style>
            /* Add your inline CSS styles here */
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            .message {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .otp {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="message">Hello,</p>
            <p class="message">You have requested to reset your password.</p>
            <p class="message">Your OTP (One-Time Password) for authentication is: <span class="otp">{otp}</span></p>
            <p class="message">Please use this OTP to complete your password reset.</p>
            <p class="message">Thank you!</p>
        </div>
    </body>
    </html>
    """
    return send_email(
        email, "sanctuspeter@gmail.com", subject, "", html_content
    )
