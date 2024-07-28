FROM python:3.12-alpine AS require
LABEL authors="YBG"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc linux-headers libc-dev curl

FROM require AS venv
WORKDIR /usr/src/app

RUN python -m venv .venv
RUN source .venv/bin/activate

COPY ./requirements.txt .
COPY ./requirements-dev.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements-dev.txt

FROM venv AS runner
WORKDIR /usr/src/app

COPY --from=venv /usr/src/app/.venv ./
RUN source .venv/bin/activate

COPY .env .
COPY app/ ./app

ENTRYPOINT [ "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000" ]
HEALTHCHECK --interval=10s --timeout=5s CMD curl -k --fail http://localhost:8000/health || exit 1