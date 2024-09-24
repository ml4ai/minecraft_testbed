import { BLACK_ON_WHITE_CSS_CLASS } from '@angular/cdk/a11y/high-contrast-mode/high-contrast-mode-detector';
import { EventEmitter, Injectable} from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';
import {PositionEvent} from './EventModels/event_models';
import { Router } from '@angular/router';
import { AudioWebsocketService } from './Services/audiowebsocket.service';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { State } from './state'
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { ClientMapConfig, HeatmapIntervention } from './types';
import { SessionService } from './Services/session.service';



@Injectable({
  providedIn: 'root'
})
export class WebsocketService  {

  config:ClientMapConfig;
  role_text;

  //debugMode = false;

  positionEmitter: EventEmitter<any[]> = new EventEmitter();

  
  mapUpdateEmitter: EventEmitter<any[]> = new EventEmitter();
  mbLegendEmitter: EventEmitter<any[]> = new EventEmitter();
  unique_idEmitter: EventEmitter<any[]> = new EventEmitter();
  participant_idEmitter: EventEmitter<any[]> = new EventEmitter();
  trialActiveEmitter: EventEmitter<boolean> = new EventEmitter();
  missionStateEmitter: EventEmitter<string> = new EventEmitter();
  threatListEmitter: EventEmitter<[[number,number]]> = new EventEmitter();

  //ADAPT

  textInterventionEmitter: EventEmitter<any[]> = new EventEmitter();
  heatmapInterventionEmitter: EventEmitter<any[]> = new EventEmitter();

  startHeatmapEmitter:EventEmitter<HeatmapIntervention> = new EventEmitter();
  stopHeatmapEmitter:EventEmitter<HeatmapIntervention> = new EventEmitter();
  pauseHeatmapEmitter:EventEmitter<HeatmapIntervention> = new EventEmitter();

  playerEmitter:EventEmitter<any> = new EventEmitter(); 
  callsignEmitter:EventEmitter<any> = new EventEmitter();
  markerBlockEmitter:EventEmitter<any> = new EventEmitter();
  roleEmitter:EventEmitter<any> = new EventEmitter();
  commBlackoutEmitter:EventEmitter<any> = new EventEmitter();


  playerName: string = '';

  map: string = '';

  constructor( public socket: Socket,               
               private router: Router, 
               private audioWebsocketService: 
               AudioWebsocketService,
               private sessionService:SessionService, 
               private http: HttpClient
              ) {
    
    
    this.socket.on('hello',(message) => {

      console.log(message);

      this.socket.emit('message', 'Hello from the front end!');

    });

    this.setupAuthentication();

  }

  getState(): Observable<State> {
    return this.http.get<State>('/ClientMap/state')
    .pipe(
      catchError(this.handleError)
    );
  }
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    return throwError(
      'Error in getState()');
  }
  

  assignNameToWebSocket( name: string ): void {

    this.playerName = name;
   
    // LISTEN TO POSITION UPDATES FROM EVERYONE IF ADVISOR OR CONFIG SAYS SO

    if(name === "asist_advisor" || (this.config['showGlobalPositions']===true)){

      console.log("Listening on Front End to positionUpdate_global messages");

      this.socket.on('positionUpdate_global', (message ) => {        

        // change the last index to a callsign instead of a playername

        // [x, y, z, mission_timer, playername]
        
        const player = message[4];

        message[4]=this.sessionService.playerCallsignMap.get(player);

        this.positionEmitter.emit(message);
  
      });
      
    }  
    // LISTEN FOR JUST YOUR OWN POSITION UPDATES 
    else{

      this.socket.on('positionUpdate_' + name, (message ) => {

        

        // [x, y, z, mission_timer, playername]
        const player = message[4];
        
        // change the last index to a callsign instead of a playername
        message[4]=this.sessionService.playerCallsignMap.get(player);

        this.positionEmitter.emit(message);
  
      });

    }   

    this.socket.on('threatlist', ( message:[[number,number]] ) => {

      console.log('ThreatList Update : ' + message);     

      if(this.sessionService.currentPlayerRole === 'Engineering_Specialist')
      
        this.threatListEmitter.emit(message);
    
    });

    this.socket.on('markerUpdate_global', ( message:[number,number,number,string,string] ) => {

      console.log('Marker block Update : ' + message);
      
      // [x, y, z, playername, marker_type]

      const player = message[3];

      message[3]=this.sessionService.playerCallsignMap.get(player);

      this.markerBlockEmitter.emit(message);
    
    });

    this.socket.on('trial', ( message ) => {
      
      console.log('---------------- trial started -----------------')

      this.sessionService.trialMessage = message;
      const sub_type = message['msg']['sub_type']
      if (sub_type == 'start') {
        
        // should really make an interface for trial message
        this.sessionService.currentMission = message['data']['experiment_mission'];
        
        this.trialActiveEmitter.emit(true);
      }
      else if (sub_type == 'end' || sub_type == 'stop') {
        this.trialActiveEmitter.emit(false);
      }
    });

    this.socket.on('missionState', ( message:string ) => {

      //EMIT TO MAP COMPONENET
      this.missionStateEmitter.emit(message);

    });

    this.socket.on('unique_idUpdate_' + name, ( message ) => {
      
        this.unique_idEmitter.emit(message);        
    });
  
    this.socket.on('participant_idUpdate_' + name, ( message ) => {

      this.participant_idEmitter.emit(message);

    });

    this.socket.on('textIntervention_' + name, ( message ) => {
      
      console.log("received text intervention in websocketservice ", message);

      this.textInterventionEmitter.emit(message);

    });

    this.socket.on('heatmapIntervention_'+name, (message) => {

      console.log("received heatmap intervention in websocketservice")
      
      this.heatmapInterventionEmitter.emit(message);

    });

    this.socket.on('startHeatmap_'+name, (message) => {

      console.log("StartHeatMap Intervention : " + message);

      this.startHeatmapEmitter.emit(message);
    });

    this.socket.on('stopHeatmap_'+name, (message) => {

      console.log("Stop HeatMap Intervention : " + message);

      this.stopHeatmapEmitter.emit(message);
    });

    this.socket.on('playerMap', (message) => {
      this.playerEmitter.emit(message);
    });

    this.socket.on('roleChange', (message) => {
      console.log('Received Role Change message : ' + message );
      this.sessionService.currentPlayerRole = message;
      this.roleEmitter.emit(message);
    });

    this.socket.on('commBlackout', (state:string) => {
      // state is "start" or "stop"
      console.log("Comms Blackout Emitter triggered : " + state)
      
      if( this.playerName != 'asist_advisor'){
        this.commBlackoutEmitter.emit(state);
      }
      
    });

    this.socket.on('assignCallsign', (message)=> {

      // clear any previous player data

      // the emitted message does not mean anything right now, it could have data if that's what we wanted
      this.callsignEmitter.emit('clearmarkers');
      this.sessionService.playerCallsignMap = new Map<string,string>();
      this.sessionService.otherPlayers = new Map<string,string>();

      // save playername to session
      this.sessionService.currentPlayer = this.playerName;            

      if (message && message.name && message.info) {
        
        if(this.playerName == 'asist_advisor'){
          for (let i = 0; i < message.info.length; i++) {
            const playername = message.info[i].playername;
            this.sessionService.playerCallsignMap.set(playername,message.info[i].callsign);
          }
        }
        else{

          for (let i = 0; i < message.info.length; i++) {
          
            const playername = message.info[i].playername;
            
            // save this player's callsign to session
            if (playername === this.sessionService.currentPlayer) { this.sessionService.currentPlayerCallSign = message.info[i].callsign }                
              
              // store all the players callsigns
              this.sessionService.playerCallsignMap.set(playername,message.info[i].callsign);
              
              if ( playername !== this.sessionService.currentPlayer){
  
                // KEEP A MAP OF THE OTHER PLAYERS FOR CONVENIENCE
                this.sessionService.otherPlayers.set( playername, message.info[i].callsign );
  
              }
  
            }          
        }
      }
    });
    this.socket.on('pauseHeatmap_'+name, (message)=> {
      this.pauseHeatmapEmitter.emit(message)
    })
  }

  setupAuthentication(){
    
    this.socket.on('authenticationResponse', (payload) => {

        console.log(payload);

        if ( payload['response'] === true ){
          this.map = payload['map'];
          this.config = payload['config'] as ClientMapConfig;
          this.sessionService.config = this.config;
          this.assignNameToWebSocket(payload['name']);
          this.audioWebsocketService.assignNameToWebSocket(payload['name']);
         
          if (payload['name'].toLowerCase() === 'asist_advisor'){
            this.router.navigateByUrl('/advisor')
          } else {
            this.router.navigateByUrl('/map');
          }
        }
    });
  }
}
