FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pricing/manage.py"]

CMD ["runserver", "0.0.0.0:8000"]

EXPOSE 8000

