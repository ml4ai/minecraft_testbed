import { Component, OnInit } from '@angular/core';
import { MetadataAppService } from '../../metadata-app/metadata-app.service';
import { LoggingService } from '../../../logging/logging.service';
import { timer } from 'rxjs';
import { HealthStatusService } from '../../health-status/health-status.service';

@Component({
  selector: 'app-metadata-app-status',
  templateUrl: './metadata-app-status.component.html',
  styleUrls: ['./metadata-app-status.component.scss']
})
export class MetadataAppStatusComponent implements OnInit {
  public online = false;
  public elasticsearchOnline = false;
  public mqttOnline = false;
  public postgresOnline = false;
  public discoveryOnline = false;
  public diskSpaceOnline = false;

  public diskSpaceDetails = '';

  constructor(
    private metadataAppService: MetadataAppService,
    private loggingService: LoggingService,
    private healthStatusService: HealthStatusService
  ) { }

  ngOnInit(): void {
    this.healthTimer();
  }

  healthTimer(): void {
    const source = timer(0, 10000);
    source.subscribe(val => {
      this.updateHealth();
    });
  }

  updateHealth(): void {
    this.metadataAppService.getHealth()
      .subscribe(result => {
        if (!result) {
          this.online = false;
          this.healthStatusService.setMetadataAppOnline(false);
          this.elasticsearchOnline = false;
          this.mqttOnline = false;
          this.postgresOnline = false;
          this.discoveryOnline = false;
          this.diskSpaceOnline = false;
          this.healthStatusService.setMetadataAppElasticsearchOnline(false);
        }
        else {
          if (result.status === 'UP') {
            this.online = true;
            this.healthStatusService.setMetadataAppOnline(true);
          } else {
            this.online = false;
            this.healthStatusService.setMetadataAppOnline(false);
          }
          if (result.details.elasticsearch.status === 'UP') {
            this.elasticsearchOnline = true;
            this.healthStatusService.setMetadataAppElasticsearchOnline(true);
          } else {
            this.elasticsearchOnline = false;
            this.healthStatusService.setMetadataAppElasticsearchOnline(false);
          }
          if (result.details['mqtt-client'].status === 'UP') {
            this.mqttOnline = true;
            this.healthStatusService.setMetadataAppMqttClientOnline(true);
          } else {
            this.mqttOnline = false;
            this.healthStatusService.setMetadataAppMqttClientOnline(false);
          }
          if (result.details['vertx-pg-client'].status === 'UP') {
            this.postgresOnline = true;
            this.healthStatusService.setMetadataAppPostgresClientOnline(true);
          } else {
            this.postgresOnline = false;
            this.healthStatusService.setMetadataAppPostgresClientOnline(false);
          }
          if (result.details['compositeDiscoveryClient()'].status === 'UP') {
            this.discoveryOnline = true;
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(true);
          } else {
            this.discoveryOnline = false;
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(false);
          }
          if (result.details.diskSpace.status === 'UP') {
            this.diskSpaceOnline = true;
            this.healthStatusService.setMetadataAppDiskSpaceOnline(true);
            this.diskSpaceDetails = `Total: ${Math.round(result.details.diskSpace.details.total / 1024 / 1024 / 1024).toFixed(2)} GB Free: ${Math.round(result.details.diskSpace.details.free / 1024 / 1024 / 1024).toFixed(2)} GB`;
          } else {
            this.diskSpaceOnline = false;
            this.healthStatusService.setMetadataAppDiskSpaceOnline(false);
            this.diskSpaceDetails = `Total: ${Math.round(result.details.diskSpace.details.total / 1024 / 1024 / 1024).toFixed(2)} GB Free: ${Math.round(result.details.diskSpace.details.free / 1024 / 1024 / 1024).toFixed(2)} GB`;
          }
        }
      });
  }

  getStatus() {
    this.metadataAppService.getHealth()
      .subscribe(result => {
        if (!result) {
          this.online = false;
          this.healthStatusService.setMetadataAppOnline(false);
          this.elasticsearchOnline = false;
          this.postgresOnline = false;
          this.discoveryOnline = false;
          this.diskSpaceOnline = false;
          this.healthStatusService.setMetadataAppElasticsearchOnline(false);
          this.log('metadata-app error: Error: No Living connections');
        }
        else {
          if (result.status === 'UP') {
            this.online = true;
            this.healthStatusService.setMetadataAppOnline(true);
            this.log('metadata-app status: ' + result);
          } else {
            this.online = false;
            this.healthStatusService.setMetadataAppOnline(false);
            this.log('metadata-app status: ' + result);
          }
          if (result.details.elasticsearch.status === 'UP') {
            this.elasticsearchOnline = true;
            this.healthStatusService.setMetadataAppElasticsearchOnline(true);
            this.log('elasticsearch status: ' + result.details.elasticsearch.status);
          } else {
            this.elasticsearchOnline = false;
            this.healthStatusService.setMetadataAppElasticsearchOnline(false);
            this.log('elasticsearch status: ' + result.details.elasticsearch.status);
          }
          if (result.details['mqtt-client'].status === 'UP') {
            this.mqttOnline = true;
            this.healthStatusService.setMetadataAppMqttClientOnline(true);
            this.log('mqtt client status: ' + result.details['mqtt-client'].status);
          } else {
            this.mqttOnline = false;
            this.healthStatusService.setMetadataAppMqttClientOnline(false);
            this.log('mqtt client status: ' + result.details['mqtt-client'].status);
          }
          if (result.details['vertx-pg-client'].status === 'UP') {
            this.postgresOnline = true;
            this.healthStatusService.setMetadataAppPostgresClientOnline(true);
            this.log('postgres client status: ' + result.details['vertx-pg-client'].status);
          } else {
            this.postgresOnline = false;
            this.healthStatusService.setMetadataAppPostgresClientOnline(false);
            this.log('postgres client status: ' + result.details['vertx-pg-client'].status);
          }
          if (result.details['compositeDiscoveryClient()'].status === 'UP') {
            this.discoveryOnline = true;
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(true);
            this.log('discovery client status: ' + result.details['compositeDiscoveryClient()'].status);
          } else {
            this.discoveryOnline = false;
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(false);
            this.log('discovery client status: ' + result.details['compositeDiscoveryClient()'].status);
          }
          if (result.details.diskSpace.status === 'UP') {
            this.diskSpaceOnline = true;
            this.healthStatusService.setMetadataAppDiskSpaceOnline(true);
            this.log('disk space status: ' + result.details.diskSpace.status);
          } else {
            this.diskSpaceOnline = false;
            this.healthStatusService.setMetadataAppDiskSpaceOnline(false);
            this.log('disk space status: ' + result.details.diskSpace.status);
          }
        }
      });
  }

  /** Log an ExperimentService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`ElasticsearchStatusComponent: ${message}`);
  }
}
