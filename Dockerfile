#FROM ubuntu:20.04
FROM python:3
#
#RUN apt-get update \
#    && apt-get install python-pip
#
#RUN pip install --upgrade pip

#LABEL version="MkI"

#COPY ./flaskblog ./flaskblog
#COPY ./scripts /scripts
#COPY ./run.py /run.py

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

#RUN chmod +x /scripts/*

#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static

#RUN adduser -D user
#RUN chown -R user:user /vol
#RUN chmod -R 755 /vol/web

ENTRYPOINT ["python"]
CMD ["run.py"]

#CMD ["entrypoint.sh"]