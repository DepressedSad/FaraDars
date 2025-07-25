import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000,999999))

def send_otp_email(email,otp_code):
    subject='Your verification code.'
    message=f'Your login code to the site: {otp_code}'
    send_mail(subject,message,'faradars.educational@gmail.com',[email])