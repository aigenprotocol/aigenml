FROM tensorflow/tensorflow:2.11.0

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5001

CMD [ "python", "server.py" ]
