docker rm -f evaluate_api
docker rmi -f evaluate_api
docker build -t evaluate_api .
docker run -d -p 5000:5000 evaluate_api
