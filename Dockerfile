FROM python:3.4

# パッケージのインストール
RUN apt-get update \
    && apt-get install -y imagemagick ghostscript

RUN mkdir /usr/src/im
WORKDIR /usr/src/im
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src ./src
COPY test ./test
COPY cmd.sh .
RUN chmod 755 cmd.sh

CMD ./cmd.sh
