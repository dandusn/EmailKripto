ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "ecckripto" + ORG_EMAIL
FROM_PWD = "ecc123ecc"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

import smtplib
import time
import imaplib
import email

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
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_body = get_mail_body(msg)
                email_from = msg['from']
                print('From : ' + email_from + '\n')
                print('Body : ' + email_body + '\n')

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