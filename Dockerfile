FROM python:3.9

LABEL version="Domain"

COPY . /home/adf

WORKDIR /home/adf

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["run.py"]
