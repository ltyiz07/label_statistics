# simple api server

## Requirements
Python 3.9

## Usage
To run the server, please execute the following from the root directory:
```
pip3 install -r requirements.txt
python3 -m evaluation_server
```

## Test
To run tests, please execute the following from the root directory:
```
pytest -q
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