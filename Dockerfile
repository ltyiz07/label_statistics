FROM python:3.9-alpine

RUN mkdir -p /flask_server
WORKDIR /flask_server

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

#ENV PORT=5000
#EXPOSE 5000
#ENTRYPOINT ["python3"]
#CMD ["-m", "flask", "run", "--host=0.0.0.0"]