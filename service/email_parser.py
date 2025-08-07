import email
from bs4 import BeautifulSoup
import mimetypes
import uuid
from email.header import decode_header
import os


def decode_mime_words(s):
    """MIME 인코딩이 포함된 문자열 디코딩 (예: 파일명)"""
    if not s:
        return ""
    decoded_fragments = decode_header(s)
    return ''.join(
        frag.decode(enc or 'utf-8', errors='ignore') if isinstance(frag, bytes) else frag
        for frag, enc in decoded_fragments
    )

def save_attachments(msg, download_dir: str):
    """이메일에서 모든 첨부파일 저장"""
    os.makedirs(download_dir, exist_ok=True)
    file_paths = []

    for i, part in enumerate(msg.walk()):
        content_dispo = str(part.get("Content-Disposition", ""))
        if "attachment" in content_dispo.lower():
            content_type = part.get_content_type()
            filename = part.get_filename()

            # 파일명 디코딩 또는 자동 생성
            if filename:
                filename = decode_mime_words(filename)
            else:
                ext = mimetypes.guess_extension(content_type) or ".bin"
                filename = f"attachment_{uuid.uuid4().hex}{ext}"

            filepath = os.path.join(download_dir, filename)

            payload = part.get_payload(decode=True)
            if payload:
                with open(filepath, "wb") as f:
                    f.write(payload)
                file_paths.append(filepath)
                print(f"📥 저장 완료: {filename}")
            else:
                print(f"⚠️ 첨부파일 디코딩 실패: {filename}")

    return file_paths


def parse_email(msg_bytes: bytes, download_dir: str):
    """이메일 내용을 파싱하여 텍스트 본문 + 첨부 이미지 저장 경로 추출"""
    msg = email.message_from_bytes(msg_bytes)

    subject = decode_mime_words(msg.get("Subject", ""))
    sender = decode_mime_words(msg.get("From", ""))
    date = decode_mime_words(msg.get("Date", ""))
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_dispo = str(part.get("Content-Disposition", ""))

            if content_type == "text/html" and "attachment" not in content_dispo:
                html = part.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                body = soup.get_text(separator=" ", strip=True)

            elif content_type == "text/plain" and not body:
                body = part.get_payload(decode=True).decode(errors="ignore").strip()
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore").strip()

    attachments = save_attachments(msg, download_dir)

    return {
        "subject": subject,
        "from": sender,
        "date": date,
        "body": body,
        "attachments": attachments
    }
