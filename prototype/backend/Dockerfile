FROM pytorch/pytorch:latest
#FROM python:3.7-alpine

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
#RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000
COPY . .

#CMD [ "uwsgi", "--ini", "app.ini" ]
CMD ["flask", "run"]