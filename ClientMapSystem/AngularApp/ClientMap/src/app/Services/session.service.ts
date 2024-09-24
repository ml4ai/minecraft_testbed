import { Injectable } from '@angular/core';
import { ClientMapConfig } from '../types';
import { WebsocketService } from '../websocket.service';

@Injectable({
  providedIn: 'root'
})
export class SessionService {

  // THE PURPOSE OF THIS CLASS IS TO PERSIST THE APP STATE ACROSS RELOADS OR ERRORS IN THE LOCAL BROWSER SESSION OBJECT
  // ALLOWS UP TO 5MB OF DATA WITH AN EXPIRATION SETTING

  // JSON OBJECT REPRESENTING CLIENTMAP SETTINGS
  config:ClientMapConfig;
  // HOLDS ALL PLAYER INFO FOR THE CURRENT SESSION (TRIAL)  
  currentPlayer:string = null;
  currentPlayerCallSign = null;
  currentPlayerRole = null;
  otherPlayers:Map<string,string> = null;
  playerCallsignMap:Map<string,string> = null;
  currentMission:string = null;
  trialMessage = null;

  client_info:[]

  constructor() { 

  }
}
