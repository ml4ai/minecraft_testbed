#!/bin/bash

# A quick and dirty resource monitor with timestamps preceding every docker stats write

i=1

time=$(date +%F-%H-%M-%S-%Z)

while [ $i -eq 1 ];do

    echo $(date +%s) >> resource_usage_$time.log
    echo $(date) >> resource_usage_$time.log
    docker stats --no-stream >> resource_usage_$time.log

done