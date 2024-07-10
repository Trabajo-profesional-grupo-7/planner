FROM python:3.10-slim

WORKDIR /code

RUN apt update && apt install curl -y

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./test /code/test

EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8004"]
