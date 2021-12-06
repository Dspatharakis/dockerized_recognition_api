FROM ubuntu:18.04

WORKDIR /tmp

RUN apt update && \
    apt install -yq --no-install-recommends \
        python3 \
        python3-pip \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools

RUN pip3 install \
    setuptools \
    wheel

COPY ./edge_server_requirements.txt .

RUN pip3 install -r edge_server_requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY edge_server/ edge_server/

COPY setup.py .

RUN pip3 install .

COPY edge_server/config.yaml /etc/config.yaml

RUN rm -r /tmp/*

ENV EDGE_SERVER_CONFIG_PATH /etc/config.yaml
ENV EDGE_SERVER_IP_ADDR 0.0.0.0
ENV EDGE_SERVER_PORT 8000

COPY entrypoint.sh .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
