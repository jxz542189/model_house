FROM ubuntu:16.04
MAINTAINER autumn
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list
RUN apt-get update
#RUN apt-get install -y apt-transport-https vim iproute2 net-tools build-essential ca-certificates curl wget software-properties-common
RUN apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common

#安装python3.6 来自第三方
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y python3.6
RUN apt install -y python3.6-dev
RUN apt install -y python3.6-venv
#为3.6安装pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
RUN ln -s /usr/bin/python3.6 /usr/bin/python
ENV PYTHONIOENCODING=utf-8
COPY . /app
WORKDIR /app
#COPY requirements.txt ./
#-i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
CMD ["gunicorn", "entity_server:app", "-c", "gun.py"]
EXPOSE 6000


FROM ubuntu:16.04
MAINTAINER autumn
RUN rm /etc/apt/sources.list
COPY . /app
WORKDIR /app
COPY sources.list /etc/apt/sources.list
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
