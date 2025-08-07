# 📬 Mail2Sheet
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![IMAP](https://img.shields.io/badge/IMAP-Email--Parsing-yellow?logo=maildotru)
![Gspread](https://img.shields.io/badge/Gspread-Google%20Sheets-lightgrey?logo=google-sheets&logoColor=green)
![OAuth2](https://img.shields.io/badge/OAuth2-Service%20Account-brightgreen?logo=google)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-HTML--Parsing-orange?logo=beautifulsoup&logoColor=white)


> **Mail2Sheet**는 교내 `대학일자리플러스센터`로 수신되는 각종 채용/홍보 메일을 자동으로 파싱하여, 지정된 **구글 스프레드시트**에 정리해주는 자동화 도구입니다.

<br>

## 🛠 주요 기능

- **IMAP** 프로토콜을 통해 메일 서버 접속
- 최근 7일 간의 **안 읽은 메일**만 필터링
- 메일 본문, 제목, 발신자, 날짜, 첨부파일 수를 파싱
- **첨부파일 자동 다운로드** (예: 포스터, 지원서 등)
- 메일 내용을 **스프레드시트에 자동 기록**

<br>

## 🧾 사용 예시

```bash
$ python main.py
```
실행 시 다음 경로에 메일 첨부파일이 저장되고,
스프레드시트에는 다음과 같은 형식으로 기록됩니다:

<br>

## 📁 출력 예시

| Subject | From | Date | Body (300자) | Attachments Count |
|--------|------|------|--------------|--------------------|
| [슈퍼루키] 채용공고 공유 요청 | job@kangnam.ac.kr | 2025-08-07 | 안녕하세요, 담당자님. 아래의 채용공고를... | 1 |

<br>

## ⚙️ 환경 설정 (.env)

```env
EMAIL_USER=example@school.ac.kr
EMAIL_PASS=yourpassword
IMAP_SERVER=imap.school.ac.kr
SERVICE_ACCOUNT_FILE=/config/google-service-account.json
SHEET_NAME=메일기록시트
```

<br>

## 🔐 Google API 사전 설정

- Google Drive API, Google Sheets API 사용 설정 필요
- 서비스 계정 생성 후 `.json` 키를 발급받아 환경 변수로 지정
- 해당 구글 계정에서 만든 스프레드시트에 **편집 권한 공유** 필요
  - `main-scheduler@<your-project>.iam.gserviceaccount.com`

<br>

## 📁 폴더 구조

```bash
├── downloads/               # 첨부파일 저장 경로
├── service/
│   ├── email_handler.py     # 메일 파싱 및 다운로드
│   ├── email_parser.py      # 메일 파싱 로직
│   ├── sheet_writer.py      # 시트 기록 로직
│   └── imap_connector.py    # IMAP 연결 및 메일 검색
├── config/
│   ├── mailscheduler-xxxxx.json # 구글 서비스 계정 키
│   ├── .env
│   └── env_loader.py        # .env 환경변수 로딩
├── main.py
├──requirements.txt
├── README.md
└── LICENSE
```

<br>

## 📌 주의사항

- Gmail이 아닌 **학교 메일서버(IMAP)** 사용 시 포트/보안 설정 확인 필요
- Google Sheets API 인증 실패 시 `403` 에러 발생 가능 → 서비스 계정 권한 확인
- `.env` 또는 서비스 계정 키는 **절대 공개 금지**

<br>

## 🧑‍💻 기여

Pull Request와 Issue를 환영합니다!  
학교 이메일 자동화를 고민하는 누구든지 이 프로젝트를 확장해보세요.
