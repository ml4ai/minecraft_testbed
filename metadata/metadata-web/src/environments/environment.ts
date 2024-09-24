// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
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

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
