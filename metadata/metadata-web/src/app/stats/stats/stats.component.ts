import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import {Subscription, timer} from 'rxjs';
import { ElasticsearchService } from '../../dashboard/elasticsearch';
import { HealthStatusService } from '../../dashboard/health-status/health-status.service';
import {MetadataAppService} from "../../dashboard/metadata-app/metadata-app.service";

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss']
})
export class StatsComponent implements OnInit, OnDestroy {
  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  private elasticsearchBusySubscription: Subscription;
  public elasticsearchBusy = false;

  @HostListener('window:beforeunload', ['$event'])
  unloadNotification($event: any) {
    if (this.elasticsearchBusy) {
      $event.returnValue = true;
    }
  }

  constructor(
    private metadataAppService: MetadataAppService,
    private elasticsearch: ElasticsearchService,
    private healthStatusService: HealthStatusService
  ) { }

  ngOnInit(): void {
    this.healthTimer();
    // this.elasticsearchOnlineSubscription = this.healthStatusService.isElasticsearchOnline.subscribe(isOnline => this.elasticsearchOnline = isOnline);
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => this.metadataAppOnline = isOnline);
    this.elasticsearchBusySubscription = this.elasticsearch.isElasticsearchBusy.subscribe(isBusy => this.elasticsearchBusy = isBusy);
  }

  ngOnDestroy(): void {
    // this.elasticsearchOnlineSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.elasticsearchBusySubscription.unsubscribe();
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
          this.healthStatusService.setMetadataAppOnline(false);
          this.healthStatusService.setMetadataAppElasticsearchOnline(false);
        }
        else {
          if (result.status === 'UP') {
            this.healthStatusService.setMetadataAppOnline(true);
          } else {
            this.healthStatusService.setMetadataAppOnline(false);
          }
          if (result.details.elasticsearch.status === 'UP') {
            this.healthStatusService.setMetadataAppElasticsearchOnline(true);
          } else {
            this.healthStatusService.setMetadataAppElasticsearchOnline(false);
          }
          if (result.details['mqtt-client'].status === 'UP') {
            this.healthStatusService.setMetadataAppMqttClientOnline(true);
          } else {
            this.healthStatusService.setMetadataAppMqttClientOnline(false);
          }
          if (result.details['vertx-pg-client'].status === 'UP') {
            this.healthStatusService.setMetadataAppPostgresClientOnline(true);
          } else {
            this.healthStatusService.setMetadataAppPostgresClientOnline(false);
          }
          if (result.details['compositeDiscoveryClient()'].status === 'UP') {
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(true);
          } else {
            this.healthStatusService.setMetadataAppDiscoveryClientOnline(false);
          }
          if (result.details.diskSpace.status === 'UP') {
            this.healthStatusService.setMetadataAppDiskSpaceOnline(true);
         } else {
            this.healthStatusService.setMetadataAppDiskSpaceOnline(false);
          }
        }
      });
  }
}
