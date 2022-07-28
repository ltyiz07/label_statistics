FROM python:3.10-alpine

RUN mkdir -p /label_statistics
WORKDIR /label_statistics
COPY requirements.txt requirements.txt
COPY .flaskenv .flaskenv
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=5000
EXPOSE 5000

ENV FLASK_APP=proj_stat
ENV FLASK_ENV=development
ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0"]