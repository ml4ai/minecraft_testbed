# MQTT Message Validator Instructions

## Building Docker container
- Navigate to the root (top level) of the MQTTValidationServiceContainer directory, this is the same level that the dockerfile appears in
- Open a shell window and run *docker build -t mqttvalidationservice:latest .*

## Updating Docker Container After a New Release --> Building From Source
- Navigate to the root (top level) of the MQTTValidationServiceContainer directory, this is the same level that the dockerfile appears in
- Open a shell window in this directory and run *docker build -t mqttvalidationservice:latest --build-arg CACHE_BREAKER=somestring .*
- You can replace the word "somestring" with any string of your choice, as long as it is unique each time
- This build is significantly faster, as the majority of the image layers are already built

## Updating Docker Container After a New Release --> Pulling New Image 
- Open a shell window and run docker login --username foo --password bar. Replace foo and bar with your username and password.
- Then run docker pull gcr.io/asist-2130/mqttvalidationservice:latest
- This should update your current mqttvalidationservice:latest image, correctly altering only the image layers that have changed

## Configuration
- You must configure the MQTT Host before using the container. This can be done in the Local/MessageValidator/appsettings.json file. Navigate to the Mqtt section of the file. You should see 2 values that look like this -->  "host" and "port". In the field labeled "host", enter the IP address of the machine running the ELk Stack like so : "host":"192.168.0.189" . Similarly, in the field labeled "port", enter the port number of the exposed broker in the ELK Stack like so : "port":"1883". This port number should almost always be 1883.
