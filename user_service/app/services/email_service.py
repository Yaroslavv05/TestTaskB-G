import aiosmtplib
from email.mime.text import MIMEText

async def send_email(email: str):
    message = MIMEText("Thank you for registering!")
    message["From"] = "email@gmail.com"
    message["To"] = email
    message["Subject"] = "Registration Successful"

    smtp_client = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587, start_tls=True)
    await smtp_client.connect()
    await smtp_client.login("email@gmail.com", "password")
    await smtp_client.send_message(message)
    await smtp_client.quit()
