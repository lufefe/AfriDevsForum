FROM python:3

ENV PATH="/scripts:${PATH}"
#ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cahce --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /flaskblog
COPY .app /app
WORKDIR /flaskblog
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

CMD ["entrypoint.sh"]