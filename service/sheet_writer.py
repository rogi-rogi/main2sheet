import gspread
from google.oauth2.service_account import Credentials

def init_sheet(service_account_path: str, sheet_name: str):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        service_account_path,
        scopes=scopes
    )
    client = gspread.authorize(creds)

    try:
        # 스프레드시트(문서) 열기
        spreadsheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"📄 스프레드시트 '{sheet_name}' 없음. 새로 생성합니다.")
        spreadsheet = client.create(sheet_name)

    try:
        # 기본 워크시트(탭) 접근
        sheet = spreadsheet.sheet1
    except (gspread.WorksheetNotFound, IndexError):
        print("📑 기본 워크시트가 없어 새로 생성합니다.")
        sheet = spreadsheet.add_worksheet(title="Sheet1", rows="100", cols="20")

    return sheet
    

def write_emails_to_sheet(parsed_emails: list[dict], service_account_path: str, sheet_name: str):
    """파싱된 이메일 리스트를 주어진 시트에 기록"""

    sheet = init_sheet(service_account_path, sheet_name)
    sheet.clear()

    # 헤더 삽입
    sheet.append_row(["Subject", "From", "Date", "Body (300자)", "Attachments Count"])

    for email in parsed_emails:
        row = [
            email.get("subject", ""),
            email.get("from", ""),
            email.get("date", ""),
            email.get("body", "")[:300],
            len(email.get("attachments", []))
        ]
        sheet.append_row(row)
