# elk-stack
This example Docker Compose configuration demonstrates the logstah, elasticsearch and kibana components of the
Elastic Stack, all running on a single machine under Docker.

## Prerequisites
- Docker and Docker Compose.

* ENV vars are set in the following file:
  * logstash.env
    * MQTT_HOST=mosquitto

* At least 4GiB of RAM for the containers. Windows and Mac users _must_
configure their Docker virtual machine to have more than the default 2 GiB of
RAM:

* Linux Users must set the following configuration as `root`:

```
sysctl -w vm.max_map_count=262144
```
By default, the amount of Virtual Memory [is not enough](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).


## Starting the stack

We can launch the stack with `docker-compose up -d --build` to create Elastic Stack with
Elasticsearch, Kibana, and Logstash.

Point a browser at [`http://localhost:5601`](http://localhost:5601) to see the results.


## Notes
1. If you want to explore the data that has been collected, you can use kibana, via http://<host>:5601/  
Before you can see the data in kibana (and every day you collect data with the ELK container), you will need to create a new index pattern.  To create an index patter follow these steps
      - go to the kibana web page at http://<host>:5601
      - log in with the instructions from above
      - go to the Management section (link at bottom left)
      - Click on Index Patterns under the Kibana section
      - Look for the 'Create Index pattern' button and click it
      - Under Step 1 of 2, find the index in the list of indices and copy the name into the Index patter name.  then click Next step
      - In the Time Filter field name pulldown list, select @timestamp, then click Create index pattern
      - Now click on Discovery on the upper right portion of the screen
      - Under the "Add a filter +" link select the index pattern you just created.
      - Now click the Refresh button on the upper right side of the screen
      - If you done get any display of data, try setting the timeframe by clicking just above the Refresh button and setting a time frame to display data for.
      - If you still don't get any data, then there might be an issues someplace else in your set up.
   
