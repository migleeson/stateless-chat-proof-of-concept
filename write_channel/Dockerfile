FROM python:3.6.13-alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
# install psycopg2 requirements
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY writes.py .

CMD ["python", "-u", "./writes.py"]
