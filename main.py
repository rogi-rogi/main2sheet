import os
import imaplib
from datetime import datetime, timedelta

import config.env_loader as env
from service.email_parser import parse_email
from service.email_handler import handle_emails
from service.sheet_writer import write_emails_to_sheet
from service.imap_connector import connect_imap, search_recent_unread
from bs4 import BeautifulSoup

DOWNLOAD_DIR = "downloads"


def setup_download_dir():
    """다운로드 폴더가 없으면 생성"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"📂 다운로드 폴더 생성됨: {DOWNLOAD_DIR}")


def main():
    env.init_env()
    EMAIL_USER, EMAIL_PASS, IMAP_SERVER = env.get_user_info()
    SERVICE_ACCOUNT_FILE, SHEET_NAME = env.get_sheet_info()

    mail = connect_imap(IMAP_SERVER, EMAIL_USER, EMAIL_PASS)
    email_ids = search_recent_unread(mail, since_days=7)
  
    setup_download_dir()
    print("✅ SERVICE_ACCOUNT_FILE =", SERVICE_ACCOUNT_FILE)
    parsed_emails = handle_emails(mail, email_ids, DOWNLOAD_DIR)
    print(SERVICE_ACCOUNT_FILE, SHEET_NAME)
    print(parsed_emails)
    write_emails_to_sheet(parsed_emails, SERVICE_ACCOUNT_FILE, SHEET_NAME)

if __name__ == '__main__':
    main()
