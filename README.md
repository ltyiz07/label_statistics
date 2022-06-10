# simple api server

## Requirements
Python 3.9

## Usage
To run the server, please execute the following from the project root directory:
```
docker run -dp 6379:6379 redis:alpine  
python -m pip3 install -r requirements.txt
python -m celery -A evaluate_api.service.evaluator worker -l INFO --pool=solo &
python -m flask run
```

## Test
To run tests, please execute the following from the root directory:
```
python -m pytest
```

[web page](http://localhost:5000/)  
[swagger api document](http://localhost:5000/apis)  


## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```
# building the image
docker build -t evaluate_api .

# starting up a container
docker run -p 5000:5000 evaluate_api
```

SQL 데이터베이스 구조  
![img.png](img.png)