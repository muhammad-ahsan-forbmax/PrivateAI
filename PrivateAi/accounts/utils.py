from random import randint

from redis import Redis
from django.core.mail import EmailMultiAlternatives

redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_otp():
    return str(randint(a=100000, b=999999))


def send_otp_email(email: str, otp: str, purpose: str = "register"):
    if purpose == "register":
        subject = "🎉 Verify Your Account"
        title = "Welcome! Verify Your Account"
        message = "Use this OTP to complete your registration."
    elif purpose == "reset":
        subject = "🔐 Reset Your Password"
        title = "Password Reset Request"
        message = "Use this OTP to reset your password."
    else:
        subject = "🔐 OTP Verification"
        title = "OTP Verification"
        message = "Use this OTP to proceed."

    text_content = f"""
    {message}
    OTP: {otp}
    This code expires in 5 minutes.
    """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; background:#f4f6f8; padding:20px;">

        <div style="max-width:500px;margin:auto;background:white;padding:30px;border-radius:10px;text-align:center;">

            <h2 style="color:#333;">{title}</h2>

            <p style="color:#555;font-size:16px;">
                {message}
            </p>

            <div style="
                font-size:30px;
                font-weight:bold;
                letter-spacing:6px;
                margin:20px 0;
                padding:15px;
                background:#f1f3f5;
                border-radius:8px;
                display:inline-block;
            ">
                {otp}
            </div>

            <p style="color:#777;font-size:14px;">
                This OTP will expire in <strong>5 minutes</strong>.
            </p>

            <p style="color:#aaa;font-size:12px;">
                If you didn't request this, please ignore this email.
            </p>

        </div>

    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email="no-reply@yourapp.com", to=[email], )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
