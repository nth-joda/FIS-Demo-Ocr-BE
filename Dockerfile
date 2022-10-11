FROM python:3.9.14-slim-buster

WORKDIR /app

COPY requirementsOct22.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]