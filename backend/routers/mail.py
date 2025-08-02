import os
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from random import randint
from app.auth.auth import client
from dotenv import load_dotenv

load_dotenv('.env')

USERNAME = os.environ.get("USERNAME")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
PASSWORD = os.environ.get("PASSWORD")


def generate_otp():
    return randint(00000,99999)

class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME = USERNAME,
    MAIL_PASSWORD = PASSWORD,
    MAIL_FROM = "notification@example.com",
    MAIL_PORT = PORT,
    MAIL_SERVER = HOST,
    MAIL_FROM_NAME="NOTIFICATION",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_mail(email: EmailStr) -> JSONResponse:
    key = f"{email}otp"
    token = generate_otp()
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your One-Time Password</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="padding: 20px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <tr>
                        <td align="center" bgcolor="#007bff" style="padding: 30px 0; color: #ffffff; font-size: 28px; font-weight: bold; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                            OTP Security Verification
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h1 style="font-size: 24px; margin: 0; color: #333333; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">Password Reset Request</h1>
                            <p style="margin: 20px 0; font-size: 16px; line-height: 1.5; color: #555555;">
                                Please use the following One-Time Password (OTP) to reset your password.
                            </p>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center" style="background-color: #e9ecef; padding: 15px 25px; border-radius: 8px; font-size: 32px; letter-spacing: 8px; font-weight: bold; color: #0056b3; font-family: 'Courier New', Courier, monospace;">
                                        {token}
                                    </td>
                                </tr>
                            </table>
                            <p style="margin: 20px 0; font-size: 16px; line-height: 1.5; color: #555555;">
                                This code is valid for <strong>1 minute</strong>.
                            </p>
                            <p style="margin-top: 30px; font-size: 14px; line-height: 1.5; color: #888888;">
                                If you did not request this, please ignore this email. Your account is still secure.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""

    # Save the token in Redis with a TTL of 60 seconds
    client.set(key, token, ex=60)

    # Create the email message
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})