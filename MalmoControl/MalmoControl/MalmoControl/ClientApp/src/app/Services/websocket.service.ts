import { Injectable, Inject } from '@angular/core';
import { environment } from 'src/environments/environment';
import {HubConnection, HubConnectionBuilder } from '@aspnet/signalr';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private _validatorMessages: BehaviorSubject<any[]> = new BehaviorSubject([]);
  public readonly validatorMessages$: Observable<any[]> = this._validatorMessages.asObservable();

  public hubConnection: HubConnection;
  public socketConnected:boolean = false;
  private baseUrl;

  constructor(@Inject('BASE_URL') baseUrl: string) {
   
    this.keepAlivePing();
    this.baseUrl = baseUrl;
    this.buildSocketConnection();
    this.startSocketConnection();
    console.log(this.baseUrl);
    
   }

  clearLog() {
    const items = [...this._validatorMessages.value];
    items.length = 0;
    this._validatorMessages.next(items);
  }

  private buildSocketConnection() {

    
      this.hubConnection = new HubConnectionBuilder()
        .withUrl(this.baseUrl + environment.wspath)
        .build();
    
    
  }

  private startSocketConnection() {
    this.hubConnection
      .start()      
      .then(() => {
        console.log('Connection started');
        this.socketConnected = true;

        this.clearLog();

        this.hubConnection.on('messageValidatorMessage', (data: any) => {
          const items = [...this._validatorMessages.value];
          items.push(JSON.parse(data));

          this._validatorMessages.next(items);
        });
        
        this.hubConnection.onclose(()=>{
          this.socketConnected = false;
          //console.log( "Connection Closed ... atttempting to recursively reconnect")          
          //this.startSocketConnection()

        });

        
       
      })
      .catch(err => console.log('Error while starting connection: ' + err));

  }

  private async keepAlivePing(){    

      setInterval( ()=> {

        if (this.socketConnected === true){

          this.hubConnection.send('KeepAlive').then(()=>{
            console.log('Keep alive ping sent.')
          });

        }       
      }, 10000 );        
  }
 
}
