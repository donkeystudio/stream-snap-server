FROM python:3.10-slim-bullseye

ADD main.py .

ENV TZ="Asia/Singapore"
RUN ln -snf /user/share/zoneinfo/$TZ etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update
RUN apt-get install -y ffmpeg

CMD [ "python3", "./main.py" ]