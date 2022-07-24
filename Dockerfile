FROM python:3.8.3-slim-buster

RUN apt-get update && apt-get -y install --no-install-recommends \
        build-essential \
        libudev-dev
RUN pip install psutil\
                numpy
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]