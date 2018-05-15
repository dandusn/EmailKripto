import codecs

from Fierkes import Fierkes

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "ecckripto" + ORG_EMAIL
FROM_PWD = "ecc123ecc"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

import smtplib
import time
import imaplib
import email
import ecdsa

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])
        typ, data = mail.fetch(str.encode(str(latest_email_id)), '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(codecs.decode(response_part[1],'utf-8'))
                email_subject = msg['subject']
                email_body = get_mail_body(msg)
                email_from = msg['from']
                print('From : ' + email_from + '\n')
                print('Body : ' + email_body + '\n')

        a = email_body

        print(email_subject)
        En = False
        Sig = False

        if email_subject == "EnSig":
            En = True
            Sig = True
        elif email_subject == "Sig":
            Sig = True
        elif email_subject == "En":
            En = True


        if Sig:
            #Signature
            Ec = ecdsa
            s = Ec.parse_sign_from_email(a)
            print(Ec.parse_sign(s[0], s[1], s[2]))
            c = Ec.CurveModP(1, 0, 3, 7)
            p = Ec.Point(3, 5)
            signat = (s[0], s[1], s[2])
            print(s[3])
            print(Ec.verify(codecs.encode(s[3], 'utf-8'), c, p, c.nth_order(p), signat))

        if En:
            #Dekript
            Fr = Fierkes()
            string = email_body
            if Sig:
                string = s[3]
            for i in range(16):
                Fr.fnd.assighnString(string, True)
                string = Fr.Decrypt()


        print(string)
        f = string.split('|')
        print(f[0])

    except Exception as e:
        print(str(e))

def get_mpart(mail):
    maintype = mail.get_content_maintype()
    if maintype == 'multipart':
        for part in mail.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
        return ""
    elif maintype == 'text':
        return mail.get_payload()


def get_mail_body(mail):
    if mail.is_multipart():
        body = get_mpart(mail)
    else:
        body = mail.get_payload()
    return body

read_email_from_gmail()