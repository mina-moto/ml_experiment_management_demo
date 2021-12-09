FROM python:3.8
ENV TZ=Asia/Tokyo
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    vim \
    wget \
    libgl1-mesa-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt