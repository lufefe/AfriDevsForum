#FROM ubuntu:20.04
#FROM ubuntu:latest
FROM python:3.9

#RUN apt-get update
#RUN apt-get install python3-pip
#RUN apt-get install flask
#RUN apt-get update -m

#RUN apt-get install -m pip python-dev build-essential
#RUN adduser -D flaskblog

#RUN apt-get update \
#    && apt-get install python-pip
#
#RUN apt-get update
#RUN apt-get -y install gcc


#LABEL version="MkI"

#COPY ./flaskblog ./flaskblog
#COPY ./scripts /scripts
#COPY ./run.py /run.py
COPY . /home/adf

#WORKDIR /

WORKDIR /home/adf


#
#RUN apk add -U \
#        ca-certificates \
#  && rm -rf /var/cache/apk/* \
#  && pip install --no-cache-dir \
#          setuptools \
#          wheel

#COPY requirements.txt .
#RUN python -m venv venv
#RUN python -m pip install --upgrade pip
#RUN pip install gunicorn
#RUN pip install --no-cache-dir \
#          setuptools \
#          wheel

RUN pip install -r requirements.txt

#
#RUN chmod +x scripts/boot.sh
#
#ENV FLASK_APP run.py
#
#RUN chown -R flaskblog:flaskblog ./
#USER flaskblog

EXPOSE 5000

#RUN chmod +x /scripts/*

#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static

#RUN adduser -D user
#RUN chown -R user:user /vol
#RUN chmod -R 755 /vol/web
#ENTRYPOINT ["python"]
ENTRYPOINT ["python"]
#ENTRYPOINT ["scripts/boot.sh"]
CMD ["run.py"]

#CMD ["boot.sh"]