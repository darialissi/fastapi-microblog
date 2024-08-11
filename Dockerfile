FROM python:3.11-slim

RUN mkdir /f_app

WORKDIR /f_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000