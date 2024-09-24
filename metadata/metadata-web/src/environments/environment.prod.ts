export const environment = {
  production: true,
  metadataAppUrl: window['env']['metadataAppUrl'] || 'http://localhost:8080',
  elasticsearchUrl: window['env']['elasticsearchUrl'] || 'http://localhost:9200',
  dockerUrl: window['env']['dockerUrl'] || 'http://localhost:8080',
  agentsUrl: window['env']['agentsUrl'] || 'http://localhost:5150',
  elasticsearchRequestTimeout: window['env']['elasticsearchRequestTimeout'] || 60000,
  mqttHost: window['env']['mqttHost'] || 'localhost',
  mqttPort: window['env']['mqttPort'] || 9001,
  mitmUrl: window['env']['mitmUrl'] || 'http://localhost:8082',
  testbedVersion: window['env']['testbedVersion'] || '1.0'
};
