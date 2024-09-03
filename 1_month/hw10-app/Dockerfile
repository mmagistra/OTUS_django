FROM python:3.12.4-bookworm

ENV PYTHONUNBUFFERED=1
WORKDIR /var/app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN pip install asyncpg

COPY app .

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80