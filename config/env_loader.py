import os
from dotenv import load_dotenv

ENV_PATH = "/config/.env"

# 기존 + 확장 키
REQUIRED_KEYS = [
    "EMAIL_USER", "EMAIL_PASS", "IMAP_SERVER",
    "SERVICE_ACCOUNT_FILE", "SHEET_NAME"
]

def load_env():
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)

def read_env():
    return {key: os.getenv(key) for key in REQUIRED_KEYS}

def prompt_missing_values(env_dict):
    updated = False

    if not env_dict["EMAIL_USER"]:
        env_dict["EMAIL_USER"] = input("📧 이메일 주소: ").strip()
        updated = True

    if not env_dict["EMAIL_PASS"]:
        env_dict["EMAIL_PASS"] = input("🔒 이메일 앱 비밀번호: ").strip()
        updated = True

    if not env_dict["IMAP_SERVER"]:
        server = input("📡 IMAP 서버 주소 (기본값: mail.kangnam.ac.kr): ").strip()
        env_dict["IMAP_SERVER"] = server or "mail.kangnam.ac.kr"
        updated = True

    if not env_dict["SERVICE_ACCOUNT_FILE"]:
        env_dict["SERVICE_ACCOUNT_FILE"] = input("📄 서비스 계정 JSON 경로: ").strip()
        updated = True

    if not env_dict["SHEET_NAME"]:
        env_dict["SHEET_NAME"] = input("📑 Google 시트 이름: ").strip()
        updated = True

    return updated

def append_missing_to_env(env_dict):
    if not os.path.exists(ENV_PATH):
        existing_keys = []
    else:
        with open(ENV_PATH, "r") as f:
            existing_keys = [line.split("=")[0].strip() for line in f if "=" in line]

    with open(ENV_PATH, "a") as f:
        for key, value in env_dict.items():
            if key not in existing_keys and value:
                f.write(f"{key}={value}\n")
                print(f"✅ {key} 항목이 .env에 추가되었습니다.")

def init_env():
    load_env()
    env_dict = read_env()
    updated = prompt_missing_values(env_dict)
    if updated:
        append_missing_to_env(env_dict)
    else:
        print("✅ 모든 환경변수가 이미 설정되어 있습니다.")

def get_user_info():
    return (os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"), os.getenv("IMAP_SERVER"))

def get_sheet_info():
    return (os.getenv("SERVICE_ACCOUNT_FILE"), os.getenv("SHEET_NAME"))
