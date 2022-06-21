# simple api server

Redis as server side caching -> caching model evaluation result.  
Redis as broker -> use pub/sub messaging queue as celery broker.  
SQLite as databse -> load challenge info at relational database.   

## Requirements
Python version >= 3.9  

## Usage
To run the server, please execute the following from the project root directory:  
(on windows add --pool=solo)
```
docker run -dp 6379:6379 redis:alpine  
python -m pip3 install -r requirements.txt
python -m celery -A evaluate_api.service.evaluator worker -l INFO --pool=solo &
python -m flask run
```
[web page](http://localhost:5000/)

## Test
To run tests, please execute the following from the root directory:
```
python -m pytest
```

## Swagger document
[swagger api document](http://localhost:5000/apis)  


## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```
# starting up a container
docker-compose up
```
