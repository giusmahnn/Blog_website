import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def otp_generation():
    return random.randint(100000, 999999)





def send_email(user, otp, domain):
    subject = "Password Reset Requested"
    from_email = 'admin@myblog.com'
    to_email = user.email
    context = {
        'username': user.username,
        'otp': otp,
        'domain': domain,
    }
    html_content = render_to_string('registration/password_reset_otp_email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()