FROM python:3.4

# パッケージのインストール
RUN apt-get update \
    && apt-get install -y imagemagick ghostscript

RUN mkdir /usr/src/im
WORKDIR /usr/src/im
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN chmod 755 cmd.sh test.sh

CMD ./cmd.sh
