import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { WebsocketService } from '../Services/websocket.service';
import { ExperimentService } from '../Services/experiment.service';

@Component({
  selector: "app-observer-info",
  templateUrl: "./observer-info.component.html",
  styleUrls: ["./observer-info.component.css"],
})
export class ObserverInfoComponent implements OnInit {
  public baseUrl: string;
  frameworkComponents: any;
  
  constructor(
    private http: HttpClient,
    @Inject("BASE_URL") baseUrl: string,
    private webSocketService: WebsocketService,
    public experimentService: ExperimentService
  ) {
    this.baseUrl = baseUrl;
    this.frameworkComponents = {
      // buttonRenderer: ButtonRendererComponent,
    }
  }

  ngOnInit(): void {}

}
