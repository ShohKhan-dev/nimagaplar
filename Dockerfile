FROM ubuntu:20.04


# Install dependencies
RUN apt-get update && apt-get install -y \
        software-properties-common
    RUN add-apt-repository universe
    RUN apt-get update && apt-get install -y \
        python3.9 \
        python3-pip
    RUN python3.9 -m pip install pip
    RUN apt-get update && apt-get install -y \
        python3-distutils \
        python3-setuptools
    RUN apt-get update && apt-get install -y \
        default-libmysqlclient-dev
    RUN apt-get install -y cron

        

WORKDIR /django

COPY requirements.txt requirements.txt

# RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

