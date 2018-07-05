#!/usr/bin/env bash

docker build . -t ee:0.1
docker run -itd -p 5000:5000 --network prometheus_monitor-net --name eureka_exporter ee:0.1
echo "----------------------------------"
echo "Congrats you are the MAN...."
echo "Link for accessing metrics is http://localhost:5000/metrics"
