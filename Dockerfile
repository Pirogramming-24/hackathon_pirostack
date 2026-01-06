FROM python:3.12-slim

# 파이썬 출력 버퍼링 비활성화 및 바이트코드 생성 방지
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 시스템 의존성 설치 (Pillow 및 PostgreSQL 라이브러리용)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hackathon.wsgi:application"]