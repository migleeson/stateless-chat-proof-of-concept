FROM python:3.6.13-alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
# install gevent prerequisites
RUN apk add --no-cache libffi-dev gcc musl-dev make build-base
RUN pip install --no-cache-dir -r requirements.txt

COPY reads.py .

CMD ["python", "-u", "./reads.py"]
