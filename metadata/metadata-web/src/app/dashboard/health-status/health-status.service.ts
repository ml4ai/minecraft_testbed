import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import {LoggingService} from '../../logging/logging.service';

@Injectable({
  providedIn: 'root'
})
export class HealthStatusService {
  // private _isElasticsearchOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  // public isElasticsearchOnline = this._isElasticsearchOnline.asObservable();
  // private elasticsearchOnline = false;

  private _isMetadataAppOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppOnline = this._isMetadataAppOnline.asObservable();
  private metadataAppOnline = false;

  private _isMetadataAppElasticsearchOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppElasticsearchOnline = this._isMetadataAppElasticsearchOnline.asObservable();
  private metadataAppElasticsearchOnline = false;

  private _isMetadataAppMqttClientOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppMqttClientOnline = this._isMetadataAppMqttClientOnline.asObservable();
  private metadataAppMqttClientOnline = false;

  private _isMetadataAppPostgresClientOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppPostgresClientOnline = this._isMetadataAppPostgresClientOnline.asObservable();
  private metadataAppPostgresClientOnline = false;

  private _isMetadataAppDiscoveryClientOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppDiscoveryClientOnline = this._isMetadataAppDiscoveryClientOnline.asObservable();
  private metadataAppDiscoveryClientOnline = false;

  private _isMetadataAppDiskSpaceOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isMetadataAppDiskSpaceOnline = this._isMetadataAppDiskSpaceOnline.asObservable();
  private metadataAppDiskSpaceOnline = false;

  constructor(
    private loggingService: LoggingService,
  ) { }

  // setElasticsearchOnline(online: boolean) {
  //   this._isElasticsearchOnline.next(online);
  //   if (this.elasticsearchOnline !== online) {
  //     this.log(online ? 'Elasticsearch is online.' : 'Elasticsearch is offline!');
  //   }
  //   this.elasticsearchOnline = online;
  // }

  setMetadataAppOnline(online: boolean) {
    this._isMetadataAppOnline.next(online);
    if (this.metadataAppOnline !== online) {
      this.log(online ? 'matadata-app is online.' : 'matadata-app is offline!');
    }
    this.metadataAppOnline = online;
  }

  setMetadataAppElasticsearchOnline(online: boolean) {
    this._isMetadataAppElasticsearchOnline.next(online);
    if (this.metadataAppElasticsearchOnline !== online) {
      this.log(online ? 'elasticsearch is online.' : 'elasticsearch is offline!');
    }
    this.metadataAppElasticsearchOnline = online;
  }

  setMetadataAppMqttClientOnline(online: boolean) {
    this._isMetadataAppMqttClientOnline.next(online);
    if (this.metadataAppMqttClientOnline !== online) {
      this.log(online ? 'mqtt is online.' : 'mqtt is offline!');
    }
    this.metadataAppMqttClientOnline = online;
  }

  setMetadataAppPostgresClientOnline(online: boolean) {
    this._isMetadataAppPostgresClientOnline.next(online);
    if (this.metadataAppPostgresClientOnline !== online) {
      this.log(online ? 'postgres is online.' : 'postgres is offline!');
    }
    this.metadataAppPostgresClientOnline = online;
  }

  setMetadataAppDiscoveryClientOnline(online: boolean) {
    this._isMetadataAppDiscoveryClientOnline.next(online);
    if (this.metadataAppDiscoveryClientOnline !== online) {
      this.log(online ? 'discovery is online.' : 'discovery is offline!');
    }
    this.metadataAppDiscoveryClientOnline = online;
  }

  setMetadataAppDiskSpaceOnline(online: boolean) {
    this._isMetadataAppDiskSpaceOnline.next(online);
    if (this.metadataAppDiskSpaceOnline !== online) {
      this.log(online ? 'disk space is online.' : 'disk space is offline!');
    }
    this.metadataAppDiskSpaceOnline = online;
  }

  private log(message: string) {
    this.loggingService.add(`HealthStatusService: ${message}`);
  }

}
