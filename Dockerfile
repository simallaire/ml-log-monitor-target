FROM python:3.6.1-alpine
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]