FROM python:latest

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "flask run" ]
