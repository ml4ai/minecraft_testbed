import { Injectable, Inject } from '@angular/core';
import {HubConnection, HubConnectionBuilder } from '@aspnet/signalr';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class AudioWebsocketService {

  public hubConnection: HubConnection;
  public connectionActive: boolean = false;
  public name: string = "Unknown";

  constructor() {
   }

  public startConnection(sampleRate: number) : Promise<void> {
    this.hubConnection = new HubConnectionBuilder()
                            .withUrl ('https://' + document.location.host + '/AsistDataIngester/audio?name=' + this.name + '&sampleRate=' + sampleRate)
                            .build();
    return this.hubConnection
      .start()
      .then(() => {
        console.log('Connection started');
        // this.hubConnection.on('messageValidatorMessage', (data: any) => {
        //   const items = [...this._validatorMessages.value];
        //   items.push(JSON.parse(data));

        //   this._validatorMessages.next(items);
        // });

        this.connectionActive = true;
      })
      .catch(err => {
        console.log('Error while starting connection: ' + err);
        this.connectionActive = false;
      });
  }

  public sendAudioData(data) {
    this.hubConnection.invoke('SendAudioData', data);
  }

  public stopConnection() {
    this.hubConnection
        .stop()
        .then(() => {
            console.log('Connection stopped');
            this.connectionActive = false;
        })
        .catch(err => console.log('Error while stopping connection: ' + err));    
  }

  assignNameToWebSocket( name: string ): void {
    this.name = name;
  }
}
