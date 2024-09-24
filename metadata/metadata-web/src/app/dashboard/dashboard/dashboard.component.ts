import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { ElasticsearchService } from '../elasticsearch';
import { Subscription, timer } from 'rxjs';
import { HealthStatusService } from '../health-status/health-status.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
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
    private elasticsearch: ElasticsearchService,
    private healthStatusService: HealthStatusService
  ) { }

  ngOnInit(): void {
    // this.elasticsearchOnlineSubscription = this.healthStatusService.isElasticsearchOnline.subscribe(isOnline => this.elasticsearchOnline = isOnline);
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => this.metadataAppOnline = isOnline);
    this.elasticsearchBusySubscription = this.elasticsearch.isElasticsearchBusy.subscribe(isBusy => this.elasticsearchBusy = isBusy);
  }

  ngOnDestroy(): void {
    // this.elasticsearchOnlineSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.elasticsearchBusySubscription.unsubscribe();
  }

}
