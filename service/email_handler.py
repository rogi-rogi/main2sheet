from service.email_parser import parse_email

def handle_emails(mail, email_ids, download_dir):
    parsed_emails = []

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, '(RFC822)')
        if status != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
            print("⚠️ 메일 로딩 실패 또는 구조 이상")
            continue

        raw_email = msg_data[0][1]
        parsed = parse_email(raw_email, download_dir)
        parsed_emails.append(parsed)

        print("────────────────────────────────────────────────────────────────────────────")
        print(f"📩 {parsed['subject']}")
        print(f"From: {parsed['from']}")
        print(f"Date: {parsed['date']}")
        print(f"Body (300자):\n{parsed['body'][:300]}")

        if parsed["attachments"]:
            print("🖼 첨부 이미지:")
            for path in parsed["attachments"]:
                print(f" - {path}")

    return parsed_emails
