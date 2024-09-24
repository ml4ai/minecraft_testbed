import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { HealthStatusService } from './health-status.service';
import { ElasticsearchService } from '../elasticsearch';

@Component({
  selector: 'app-health-status',
  templateUrl: './health-status.component.html',
  styleUrls: ['./health-status.component.scss']
})
export class HealthStatusComponent implements OnInit, OnDestroy {

  constructor() { }

  ngOnInit(): void { }

  ngOnDestroy(): void { }
}
