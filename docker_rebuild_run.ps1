docker rm -f annotation_statistics
docker rmi -f annotation_statistics
docker build -t annotation_statistics .
docker run -d -p 5000:5000 annotation_statistics
