(function(window) {
  window.env = window.env || {};

  // Environment variables
  window['env']['metadataAppUrl'] = '${METADATA_APP_URL}';
  window['env']['elasticsearchUrl'] = '${ELASTICSEARCH_URL}';
  window['env']['dockerUrl'] = '${DOCKER_URL}';
  window['env']['agentsUrl'] = '${AGENTS_URL}';
  window['env']['elasticsearchRequestTimeout'] = '${ELASTICSEARCH_REQUEST_TIMEOUT}';
  window['env']['mqttHost'] = '${MQTT_HOST}';
  window['env']['mqttPort'] = '${MQTT_PORT}';
  window['env']['mitmUrl'] = '${MITM_URL}';
  window['env']['testbedVersion'] = '${TESTBED_VERSION}';
})(this);
