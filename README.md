# simple api server  

요구사항:
    1. 서버의 어노테이션에 대해 수치화된 정보 웹 으로 제공
    2. 제공받은 수치들을 종류별로 통계화
    3. 해당하는 이미지 제공
    4. 이미지에 어노테이션 오버레이

mongodb as database

## Requirements

Python version >= 3.9  

## Usage

To run the server, please execute the following from the project root directory:  

```pwsh
docker run -dp 27017:27017 -v C:\pyth\db_statistics\database:/data/db --name mongodb mongo
python -m pip3 install -r requirements.txt
python -m flask run
```

[web page](http://localhost:5000/index)

## Test

To run tests, please execute the following from the root directory:

```pwsh
python -m pytest
```

## Swagger document

[swagger api document](http://localhost:5000/)  

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```pwsh
# starting up a container
docker-compose up
```


## resolve

for mod_wsgi installation error, on powershell below  

```pwsh
mkdir -p C:\wamp64\bin\apache\apache2.4.51
$env:MOD_WSGI_APACHE_ROOTDIR = "C:\wamp64\bin\apache\apache2.4.51"
```

project hierarchy  
    - app.py
        controllers
            - config.py
            database
            services
                - config.py,  
                database
                    - config.py,  
        templates
