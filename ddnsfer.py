import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telegram
from telegram import Bot
import os
import asyncio

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json().get('ip')
    return ip

def send_email_notification(new_ip):
    email = "your_email@example.com"
    password = "your_email_password"
    to_email = "recipient_email@example.com"
    subject = "IP Address Change Notification"
    body = f"Your new public IP address is: {new_ip}"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def send_telegram_notification(new_ip):
    bot_token = '7374766958:AAFzW0wCxlaxfI4Zmvl2VWgAbbtAI3vXf8Y'
    chat_id = '1473145398'
    message = f"Your new public IP address is: {new_ip}"
    
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    ip_file = 'current_ip.txt'
    
    new_ip = get_public_ip()

    if os.path.exists(ip_file):
        with open(ip_file, 'r') as file:
            current_ip = file.read().strip()
    else:
        current_ip = ""

    if new_ip != current_ip:
        #send_email_notification(new_ip)
        await send_telegram_notification(new_ip)
        
        with open(ip_file, 'w') as file:
            file.write(new_ip)

if __name__ == "__main__":
    asyncio.run(main())
