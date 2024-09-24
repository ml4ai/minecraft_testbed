import { Component, Inject, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ArrayDTO } from '../Interface/DTO';
import { WebsocketService } from '../Services/websocket.service';


@Component({
  selector: 'app-fetch-ports',
  templateUrl: './fetch-ports.component.html',
  styleUrls: ['./fetch-ports.component.css']
})
export class FetchPortsComponent implements AfterViewInit {

  public ports: ArrayDTO;
  public output: string[] = ['placeholder'];
  public baseUrl: string;
  

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string, private webSocketService: WebsocketService) {

    this.baseUrl = baseUrl;
    this.addWSMessageListeners();

  }

   ngAfterViewInit() {
  //   const loop = async () => {

  //     this.requestPorts().then( () => {
  //       setTimeout( () => { loop();  }, 5000 );  }
  //     );
  //   };

  //   loop();
   }

  // public async requestPorts() {

  //   this.http.get<ArrayDTO>(this.baseUrl + 'api/Malmo/getPorts', { responseType: 'json' }).subscribe(ports => {
  //     this.ports = ports;
  //     this.output = this.ports.data;
  //     },
  //     error => console.error(error)
  //     // ,
  //     // () => console.log( this.output )
  //   );
  // }

  public addWSMessageListeners() {

    this.webSocketService.hubConnection.on('portsUpdate', (ports) => {
      console.log(ports);
      this.output = ports.data;
    });
  }

}


