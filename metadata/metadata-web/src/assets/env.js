(function(window) {
  window['env'] = window['env'] || {};

  // Environment variables
  window['env']['metadataAppUrl'] = 'http://localhost:8080';
  window['env']['elasticsearchUrl'] = 'http://localhost:9200';
  window['env']['dockerUrl'] = 'http://localhost:8080';
  window['env']['agentsUrl'] = 'http://localhost:5150';
  window['env']['elasticsearchRequestTimeout'] = 60000;
  window['env']['mqttHost'] = 'localhost';
  window['env']['mqttPort'] = 9001;
  window['env']['mitmUrl'] = 'default';
  window['env']['testbedVersion'] = '1.0';
})(this);
