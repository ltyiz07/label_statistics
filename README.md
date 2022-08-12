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

set TAR_SOURCE at .\proj_stat\config.py as path where *.tar files located.  

```pwsh
docker run -dp 27017:27017 -v ./database:/data/db --name mongodb mongo
python -m pip3 install -r requirements.txt
python -m flask run
```

실행후 아래 페이지에서 "Update Database" 링크 클릭  
[web page](http://localhost:5000)  
[Notion info](https://road-bit-136.notion.site/5337e546b32a4c98aa5a4420ea817e11)

## Test

To run tests, please execute the following from the root directory:

```pwsh
python -m pytest
```

## Swagger document

[swagger api document](http://localhost:5000/)  

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
