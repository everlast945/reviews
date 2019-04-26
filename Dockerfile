FROM python:3.7

RUN apt-get update

COPY ./src/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--chdir", "./reviews", "setting.wsgi:app"]