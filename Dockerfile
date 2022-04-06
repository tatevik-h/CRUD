FROM python:3.9-slim-buster

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


CMD alembic upgrade head && \
    uvicorn  src.main:app --host 0.0.0.0 --port 8000
