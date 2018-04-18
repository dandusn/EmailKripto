import smtplib

def Emailsender(to, subject, msg):
    try:
        #fp = open('msg.txt', 'rb')
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('kriptoecctest@gmail.com','kripto123kripto')
        sub = "Subject: {}\n\n{}".format(subject, msg)
        mail.sendmail('kriptoecctest@gmail.com',to,sub)
        mail.quit()
        print("success")
    except:
        print("not success")