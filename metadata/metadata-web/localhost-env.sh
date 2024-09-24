cp metadata-web.env metadata-web-old.env
echo "NODE_ENV=production
METADATA_APP_URL=http://localhost:8080
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_REQUEST_TIMEOUT=60000
MQTT_HOST=localhost
MQTT_PORT=9001
MITM_URL=default" > metadata-web.env 
tail -1 metadata-web-old.env >> metadata-web.env

