from flask_mail import Message
from flask import url_for
from . import mail, app

def send_verification_mail(token, toMail):
    msg = Message('Verify mail',
                  sender='noreply@demo.com',
                  recipients=[toMail])
    

    msg.body = f'''To verify your email click on this link
{url_for('verification', token = token, _external = True)}

If not initiated by you just ignore the mail
'''
    mail.send(msg)