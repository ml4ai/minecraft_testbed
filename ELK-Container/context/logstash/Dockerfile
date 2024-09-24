FROM docker.elastic.co/logstash/logstash:7.6.2

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json

RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-input-paho-mqtt
RUN logstash-plugin install logstash-input-dead_letter_queue
