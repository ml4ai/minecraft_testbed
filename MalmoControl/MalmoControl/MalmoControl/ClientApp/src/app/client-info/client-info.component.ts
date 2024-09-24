import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { WebsocketService } from '../Services/websocket.service';
import { MatTable } from '@angular/material/table';
import { ExperimentService } from '../Services/experiment.service';
import { ButtonRendererComponent } from './button-renderer.component';

@Component({
  selector: "app-client-info",
  templateUrl: "./client-info.component.html",
  styleUrls: ["./client-info.component.css"],
})
export class ClientInfoComponent implements OnInit {
  public baseUrl: string;
  frameworkComponents: any;
  
  constructor(
    private http: HttpClient,
    @Inject("BASE_URL") baseUrl: string,
    private webSocketService: WebsocketService,
    public experimentService: ExperimentService
  ) {
    this.baseUrl = baseUrl;
    this.addWSMessageListeners();
    this.frameworkComponents = {
      buttonRenderer: ButtonRendererComponent,
    }
  }

  ngOnInit(): void {}

  public addWSMessageListeners() {
    this.webSocketService.hubConnection.on(
      "clientmapsystemplayername",
      (message) => {
        console.log(message);
        if (message.data != null && message.data.playername != null) {
          var matchFound = false;

          // Check for duplicate playername
          this.experimentService.gridOptions.api.forEachNode((rowNode, index) => {
            if (rowNode.data.playername == message.data.playername) {
              matchFound = true;
            }
          });

          if (!matchFound) {
            this.experimentService.gridOptions.api.applyTransaction({
              add: [
                {
                  playername: message.data.playername,
                  callsign: "",
                  participant_id: "",
                  staticmapversion: "",
                  markerblocklegend: "",
                  unique_id: "",
                },
              ],
            });
          }
        }
      }
    );
  }
}
