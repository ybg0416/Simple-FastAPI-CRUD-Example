# Simple FastAPI CRUD Example

## 📌 Features

- 240727 created, Python 3.12.x, fastapi~=0.111.1, pydantic~=2.8.2, sqlmodel~=0.0.21
    - PostgreSQL
    - Create users
    - endpoints CRUD
        - Member
    - API healthcheck
    - Complete swagger Api info

## 💾 Installation

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## 🔧 Config

- `.env.example`을 복사, 참고 하여 `.env` 파일 작성
  - docker 사용 시, `POSTGRES_HOST` = `host.docker.internal`

## 🏃 Run

```bash
# http
uvicorn app.main:app

# dev 
uvicorn app.main:app --reload
```