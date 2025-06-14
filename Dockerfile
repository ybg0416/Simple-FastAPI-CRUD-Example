FROM python:3.13-alpine AS require
LABEL authors="YBG"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# psutil 모듈 설치를 위해 필요한 패키지 설치
RUN apk add --no-cache --update \
    build-base \
    linux-headers

FROM require AS venv
WORKDIR /usr/src/app

RUN pip install uv

COPY pyproject.toml ./

RUN uv sync

FROM venv AS runner
WORKDIR /usr/src/app

COPY --from=venv /usr/src/app/.venv ./

COPY .env .
COPY app/ ./app

ENTRYPOINT ["sh", "-c", "uv run uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000" ]
HEALTHCHECK --interval=10s --timeout=5s CMD curl -k --fail http://localhost:8000/health || exit 1