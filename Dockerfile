FROM python:3.10.5-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add python3-dev gcc libc-dev py-pip openssl ca-certificates py-openssl \
    libffi-dev openssl-dev py-pip build-base
RUN pip install --upgrade pip
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./app ./app
CMD ["python", "app/main.py"]