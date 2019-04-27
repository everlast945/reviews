FROM python:3.7

RUN apt-get update

COPY ./src/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "setting.wsgi:app", "--chdir", "./reviews", "--bind", "0.0.0.0:8000", "--workers", "5", "--timeout", "120" ]