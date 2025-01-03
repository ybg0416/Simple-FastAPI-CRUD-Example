FROM python:3.13-alpine AS require
LABEL authors="YBG"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc linux-headers libc-dev curl

FROM require AS venv
WORKDIR /usr/src/app

RUN python -m venv .venv

COPY ./requirements.txt ./requirements-dev.txt ./

RUN source .venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements-dev.txt

FROM venv AS runner
WORKDIR /usr/src/app

COPY --from=venv /usr/src/app/.venv ./

COPY .env .
COPY app/ ./app

ENTRYPOINT ["sh", "-c", "source .venv/bin/activate && uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000" ]
HEALTHCHECK --interval=10s --timeout=5s CMD curl -k --fail http://localhost:8000/health || exit 1