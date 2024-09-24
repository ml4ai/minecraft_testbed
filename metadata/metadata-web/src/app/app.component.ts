import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LoggingService } from './logging/logging.service';
import { Subscription } from 'rxjs';
import { MessagePopupComponent } from './message-popup/message-popup.component';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'metadata-web';
  version = `version: ${environment.testbedVersion}`;
  private messageSubscription: Subscription;
  routes = [
    { path: 'dashboard', name: 'Dashboard' },
    { path: 'docker', name: 'Docker' },
    { path: 'experiments', name: 'Experiments' },
    { path: 'trials', name: 'Trials' },
    { path: 'replays', name: 'Replays' },
    { path: 'stats', name: 'Stats' },
  ];
  private metadataLogSubscription: Subscription;

  constructor(
    private popup: MatSnackBar,
    private loggingService: LoggingService,
    private mqttService: MqttService) {
    this.metadataLogSubscription = this.mqttService.observe('metadata/log').subscribe((message: IMqttMessage) => {
      const json = new TextDecoder('utf-8').decode(message.payload);
      const logMessage = JSON.parse(json);
      // console.log(json);
      const decodedString = atob(logMessage.encoded_string);
      this.loggingService.add('metadata-app: ' + decodedString);
    });
  }

  ngOnInit(): void {
    this.messageSubscription = this.loggingService.message.subscribe(message => this.openPopup(message));
  }

  ngOnDestroy(): void {
    this.messageSubscription.unsubscribe();
    this.metadataLogSubscription.unsubscribe();
  }

  openPopup(message: string) {
    this.popup.openFromComponent(MessagePopupComponent, {
      data: message,
      duration: 3000
    });
  }
}

