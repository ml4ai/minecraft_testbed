import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { LoggingService } from '../logging.service';
import { Subscription } from 'rxjs';
import { IMqttMessage, MqttService } from 'ngx-mqtt';

@Component({
  selector: 'app-logging',
  templateUrl: './logging.component.html',
  styleUrls: ['./logging.component.scss']
})
export class LoggingComponent implements OnInit, OnDestroy {
  private loggingSubscription: Subscription;
  messages: any;

  constructor(
    private cdRef: ChangeDetectorRef,
    public loggingService: LoggingService
  ) {

  }

  ngOnInit(): void {
    this.loggingSubscription = this.loggingService.messages.subscribe(messages => this.addMessages(messages));
  }

  ngOnDestroy(): void {
    this.loggingSubscription.unsubscribe();
  }

  addMessages(messages): void {
    this.messages = messages;
    this.cdRef.detectChanges();
  }
}
