FROM python:latest

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000/tcp

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
