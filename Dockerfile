FROM python:3.4

# パッケージのインストール
RUN apt-get update \
    && apt-get install -y imagemagick ghostscript \
    && pip install Flask==0.10.1

RUN mkdir /usr/src/im
WORKDIR /usr/src/im
COPY src ./src
COPY cmd.sh .
RUN chmod 755 cmd.sh

CMD ./cmd.sh
