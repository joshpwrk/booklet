# syntax=docker/dockerfile:1

FROM python:3-alpine
COPY . .
RUN pip install redis
CMD ["python3", "server.py"]
EXPOSE 8000