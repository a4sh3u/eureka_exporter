#!/usr/bin/env bash

docker build . -t ee:0.1
docker run -itd -p 5000:5000 --network prometheus_monitor-net --name eureka_exporter ee:0.1
