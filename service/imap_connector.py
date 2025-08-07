import imaplib
from datetime import datetime, timedelta

def connect_imap(server, user, password):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, password)
    return mail

def search_recent_unread(mail, since_days=7):
    today = datetime.today()
    since_date = (today - timedelta(days=since_days)).strftime("%d-%b-%Y")
    mail.select("Inbox")
    status, data = mail.search(None, 'UNSEEN', 'SINCE', since_date)
    if status != "OK":
        return []
    return data[0].split()
