import smtplib
from flask import render_template

def Emailsender(to, subject, msg):
    try:
        #fp = open('msg.txt', 'rb')
        #blm digunakan
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('kriptoecctest@gmail.com','kripto123kripto')
        sub = "Subject: {}\n\n{}".format(subject, msg)
        mail.sendmail('kriptoecctest@gmail.com',to,sub)
        mail.quit()
        print("success")
    except Exception as e:
        print("unsuccess" + e)