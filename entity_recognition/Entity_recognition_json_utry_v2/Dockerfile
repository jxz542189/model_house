FROM ubuntu:16.04
MAINTAINER autumn
#RUN rm /etc/apt/sources.list
COPY . /app
WORKDIR /app
#COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common\
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update \
    && apt-get install -y python3.6 \
    && apt install -y python3.6-dev \
    && apt install -y python3.6-venv \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python3.6 get-pip.py \
    && rm -rf get-pip.py \
    && ln -s /usr/bin/python3.6 /usr/bin/python \
    && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ENV PYTHONIOENCODING=utf-8
EXPOSE 6000
CMD ["gunicorn", "entity_server:app", "-c", "gun.py"]

