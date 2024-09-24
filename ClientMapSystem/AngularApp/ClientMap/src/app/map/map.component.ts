import { AfterContentInit, OnInit, Component } from '@angular/core';
import { Router } from '@angular/router';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import {ActionDialogComponent} from '../action-dialog/action-dialog.component';

import {WebsocketService } from '../websocket.service';
import { SessionService } from '../Services/session.service';
import { environment } from 'src/environments/environment';
import { PositionEvent } from '../EventModels/event_models';
import {HeatmapIntervention} from '../types';
import * as internal from 'events';

const Action = {
  START: 'start', 
  STOP: 'stop', 
  PAUSE: 'pause'
}

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements AfterContentInit, OnInit {

title = 'ClientMap';
gridDivs = [];

mapLoaded = false;

missionStarted = false;

map;

mapImage: HTMLImageElement;
blackoutImage: HTMLImageElement;
qrImage: HTMLImageElement;

lastDivRed: HTMLElement = null;
lastDivGreen: HTMLElement = null;
lastDivBlue: HTMLElement = null;

playerElementRed: HTMLImageElement = null;
playerElementGreen: HTMLImageElement = null;
playerElementBlue: HTMLImageElement = null;

playerRadius = 0;

playerX = 0;

playerY = 0;

clickedDiv: HTMLDivElement;
  
boundedZCoord = 5000; 

body:HTMLBodyElement;

markerBlockMap:Map<string,string>=new Map<string,string>();
threatListIds:string[] = []

constructor( public webSocketService: WebsocketService, public dialog: MatDialog, private router: Router,
  private sessionService: SessionService ) {
    
    this.map = webSocketService.map;


}

ngOnInit(): void{

}

ngAfterContentInit(): void {  
  
  // Build the map divs

  console.log('Loading Map : ' + this.map);

  const gridLayer = document.getElementById('GridLayer');

  this.mapImage = document.getElementById('Map') as HTMLImageElement;

  this.qrImage = document.getElementById('QRImageElement') as HTMLImageElement;

  const interactionContainer = document.getElementById('InteractionContainer');

  if ( this.webSocketService.playerName == 'asist_advisor' ){
    this.mapImage.style.height = '90%';
    this.qrImage.style.height = '90%';
    interactionContainer.style.height = '10%'
  }

  this.blackoutImage = document.getElementById('BlackoutImageElement') as HTMLImageElement;

  this.blackoutImage.src = environment.hostpath + 'assets/Blackout.png';

  

  this.qrImage.src = environment.hostpath + 'assets/RickQRv2.png';

  if (this.map === 'ASIST'){

    this.mapImage.src = environment.hostpath + 'assets/PlayArea.png';

    for (let z = -11; z < 67; z++) {
      for (let x = -2225; x <= -2087; x++){
        this.gridDivs.push(`GridDiv_${x},${z}`);
      }
    }

    gridLayer.style.setProperty('grid-template-columns', 'repeat(139,1fr)' );

  }  

  this.body = document.getElementById('body') as HTMLBodyElement;  

  // EMITTER SUBSCRIPTIONS

  this.webSocketService.positionEmitter.subscribe( (message: PositionEvent) => {

    this.updatePlayerPosition(message);

  });

  this.webSocketService.commBlackoutEmitter.subscribe( (message:string) => {

    console.log("Blackout Emitter has passed to Map element")   

    this.processBlackoutPerturbation(message);
  });

  this.webSocketService.missionStateEmitter.subscribe( (message) => {       
  
    if( message === 'Start'){
      this.triggerQRCode(message);
    }    

  });

  this.webSocketService.threatListEmitter.subscribe( (message: [[number,number]]) => {       
  
    console.log("ThreatList made it to the map --> " + message)

    message.forEach ( item =>{

      try {

        // get the div element which represents this position item[0]=x item[1]=z
    
        let gridID = `GridDiv_${item[0]},${item[1]}`;    
    
        const element = document.getElementById(gridID);    
    
        if (element !== null){      
          const assetLocation = environment.hostpath + 'assets/threat.png';

          const rect = element.getBoundingClientRect();
          const x = rect.x;
          const y = rect.y;
    
          //console.log('Coords for block:' + x,y);              
            
          const threatElement:HTMLImageElement = new Image();
  
          const transformString = `translate(${x + (rect.width / 2) - 5}px,${ y + (rect.height / 2) - 5}px)`;
  
          // marker properties since they don't get picked up from css for some reason      
          threatElement.className='Threat';
          threatElement.style.height = '16px';
          threatElement.style.width = '16px';
          threatElement.style.zIndex = '2';
          threatElement.style.transform = transformString;
          threatElement.id = `Threat_${item[0]},${item[1]}`
          threatElement.style.position = 'absolute';
    
          this.body.appendChild( threatElement);
  
          threatElement.src = assetLocation;
          this.threatListIds.push(threatElement.id); 
        }
      }
      catch(e){
        console.log(e)
      }
    });
  });
     

  this.webSocketService.markerBlockEmitter.subscribe( (message:[number,number,number,string,string]) => {

    if(message[4]==='removed'){

      console.log('received marker removed in from websocket service via markerblockemitter')
      this.removeMarkerBlock(message);
    }
    else{
      this.updateMarkerBlock(message);
    }    

  });

  this.webSocketService.callsignEmitter.subscribe( (message ) => {

    this.clearMarkerBlocks();
    this.clearThreatSigns();

  });

  this.webSocketService.startHeatmapEmitter.subscribe((message: HeatmapIntervention) => {
    this.updateHeatmap(message, Action.START);
    console.log("Start Emmiter");
  });

  this.webSocketService.stopHeatmapEmitter.subscribe((message:HeatmapIntervention) => {
    this.updateHeatmap(message, Action.STOP);
    console.log("End Emmiter");
  });

  this.webSocketService.pauseHeatmapEmitter.subscribe((message: HeatmapIntervention) => {
    this.updateHeatmap(message, Action.PAUSE);
  });

  this.playerResize('Red');
  this.playerResize('Green');
  this.playerResize('Blue');

  window.addEventListener('resize', () => {

    this.resizeEverything();
    
  });

  this.mapImage.addEventListener( 'load' , () => {

   this.resizeEverything();

  });   
}

public resizeEverything(){
  this.gridResize();
    this.playerResize('Red');
    this.playerResize('Green');
    this.playerResize('Blue');
    this.interactionResize();
    this.markersResize();
    this.threatsResize();

    // Corrects the first one if off
    setTimeout( () => {
      this.gridResize();
      this.playerResize('Red');
      this.playerResize('Green');
      this.playerResize('Blue');
      this.interactionResize();
      this.markersResize();
      this.threatsResize();
    }, 500);
}

public clearMarkerBlocks(){

  this.markerBlockMap.forEach((v,k)=>{
    
    console.log("Clearing Markers")

    const body = document.getElementById('body');
    
    // get the image element
    const element = document.getElementById(k);

    body.removeChild(element);    
    
  });

  this.markerBlockMap.clear();

}

public clearThreatSigns(){ 

  this.threatListIds.forEach( (id)=>{
    
    console.log("Clearing ThreatListIds")

    const body = document.getElementById('body');
    
    // get the image element
    const element = document.getElementById(id);

    body.removeChild(element);    
    
  });

  this.threatListIds=[];

}

public interactionResize(){
  
  const interactionContainer = document.getElementById('InteractionContainer');

  if(interactionContainer !== null ){

    const window_height = window.innerHeight;

    const map_width = this.mapImage.clientWidth? this.mapImage.clientWidth : 800;
    const map_height = this.mapImage.clientHeight? this.mapImage.clientHeight: 600;

    const interactionHeight = window_height-map_height - 20;
        
    interactionContainer.style.transform = `translate(${0}px,${map_height+4}px)`;
    interactionContainer.style.setProperty('width',`${map_width}px`);
    interactionContainer.style.setProperty('height',`${interactionHeight}px`);

  } 

}

public gridResize(): void {

  const width = this.mapImage.clientWidth;
  const height = this.mapImage.clientHeight;

  //console.log('Map Width : ' + width);
  //console.log('Map Height : ' + height);

  let gridCellWidth;
  let gridCellHeight;

  if ( this.map === 'ASIST'){

    // ASIST: 139 by 140 blocks
    gridCellWidth = width / 139;
    gridCellHeight = height / 77;

    this.boundedZCoord = 66;
  }

  else if (this.map === 'Falcon'){

    // FALCON : 50 by 90 blocks
    gridCellWidth = width / 50;
    gridCellHeight = height / 90;

  }

  const elements: HTMLCollectionOf<HTMLDivElement> = document.getElementsByClassName('GridDivs') as HTMLCollectionOf<HTMLDivElement>;

  for ( let i = 0; i < elements.length; i++) {

    elements[i].style.width = gridCellWidth.toString() + 'px';
    elements[i].style.height = gridCellHeight.toString() + 'px';
  }

  // console.log('Set Grid Cells to be : ' + gridCellWidth , gridCellHeight);

}

public threatsResize():void{
  this.threatListIds.forEach((id)=>{
    const element = document.getElementById(id);
    // split it's id into parts to get x and z coords, id is key in storage map as well
    const splitString = id.split('_');
    const splitStringCoords = splitString[1].split(',');
    
    //console.log(splitString);
    //console.log(splitStringCoords);
    
    const x = splitStringCoords[0];
    const z = splitStringCoords[1];
    
    // get the div it belongs in
    const divToMoveTo = document.getElementById(`GridDiv_${x},${z}`);
    const rect = divToMoveTo.getBoundingClientRect();
  
    // get the coords it belongs in
    const toX = rect.x;
    const toY = rect.y;

    const transformString = `translate(${toX}px,${toY}px)`;    
      
    // do the translation
    element.style.transform = transformString;
     
  });
}

public markersResize():void{

  this.markerBlockMap.forEach((v,k)=>{
    
    console.log("Resizing Markers")
    
    // get the image element
    const element = document.getElementById(k);
    
    // split it's id into parts to get x and z coords, id is key in storage map as well
    const splitString = k.split('_');
    const splitStringCoords = splitString[1].split(',');
    
    //console.log(splitString);
    //console.log(splitStringCoords);
    
    const x = splitStringCoords[0];
    const z = splitStringCoords[1];
    
    // get the div it belongs in
    const divToMoveTo = document.getElementById(`GridDiv_${x},${z}`);
    const rect = divToMoveTo.getBoundingClientRect();
  
    // get the coords it belongs in
    const toX = rect.x;
    const toY = rect.y;

    const transformString = `translate(${toX}px,${toY}px)`;

    // BECAUSE THE ANIMATION INCLUDES THE TRANSFORM
    if(v.includes('sos')){
      this.animateSOS(element,transformString);
    }
    else{
      // do the translation
      element.style.transform = transformString;
    }
    

  });

}

public playerResize(callSign): void{

  let lastDiv: HTMLElement = null;

  if (callSign === 'Red'){ 
    
    lastDiv = this.lastDivRed

    if ( lastDiv !== null){

      const rect = lastDiv.getBoundingClientRect();
  
      const x = rect.x;
      const y = rect.y;
  
      // console.log(x, y);
  
      this.playerElementRed.style.transform = `translate(${x}px,${y}px)`;
  
    }
  
  }
  else if (callSign === 'Green'){ 
    
    lastDiv = this.lastDivGreen

    if ( lastDiv !== null){

      const rect = lastDiv.getBoundingClientRect();
  
      const x = rect.x;
      const y = rect.y;
  
      // console.log(x, y);
  
      this.playerElementGreen.style.transform = `translate(${x}px,${y}px)`;
  
    }
  
  }
  else if (callSign === 'Blue'){ 
    
    lastDiv = this.lastDivBlue

    if ( lastDiv !== null){

      const rect = lastDiv.getBoundingClientRect();
  
      const x = rect.x;
      const y = rect.y;
  
      // console.log(x, y);
  
      this.playerElementBlue.style.transform = `translate(${x}px,${y}px)`;
  
    }  
  }
}

testDiv(event): void {

  console.log(event);
  //console.log(event.target.srcElement.id);
}

gridDivClick(event): boolean{
  this.clickedDiv = event.srcElement as HTMLDivElement;
  console.log(this.clickedDiv.clientLeft);
  //this.launchActionDialog();
  return false;
}

onClick(event):void{
  console.log(event);
}

launchActionDialog(): void {

  const dialogConfig = new MatDialogConfig();
  dialogConfig.autoFocus = true;

  const dialogRef = this.dialog.open( ActionDialogComponent, dialogConfig);

  dialogRef.afterClosed().subscribe( color => {

    // console.log(color);
    // this.clickedDiv.style.backgroundColor = color;

    }
  );
}

removeMarkerBlock(message:[number,number,number,string,string]):void{
  
  console.log ('In remove marker block');
  const markerID = `Marker_${message[0]},${message[2]}`;

  if( this.markerBlockMap.has( markerID ) ) {

    console.log("Removing existing marker : " + markerID );

    const markerElement:HTMLImageElement = document.getElementById(markerID) as HTMLImageElement;
    
    this.body.removeChild(markerElement);

    this.markerBlockMap.delete(markerID); 

  }

}

updateMarkerBlock(message:[number,number,number,string,string]):void{
  try{

    // get the div element which represents this position

    let gridID = `GridDiv_${message[0]},${message[2]}`;    

    const element = document.getElementById(gridID);    

    if (element !== null){      
      
      const rect = element.getBoundingClientRect();
      const x = rect.x;
      const y = rect.y;

      console.log('Coords for block:' + x,y);

      // CHECK IF THIS DIV ELEMENT ALREADY HAS A MARKER ON IT

      let existingMarker = null;

      const markerID = `Marker_${message[0]},${message[2]}`;

      if( this.markerBlockMap.has( markerID ) ) {

        existingMarker = this.markerBlockMap.get( markerID ) ;
      }

      const assetLocation = environment.hostpath + 'assets/Markers/block_marker_'+ message[4] +'.png';
      
      // IF THIS IS AN EMPTY DIV ELEMENT DO THIS
      if (existingMarker === null ){           
        
        const markerElement:HTMLImageElement = new Image();

        const transformString = `translate(${x + (rect.width / 2) - 5}px,${ y + (rect.height / 2) - 5}px)`;

        // marker properties since they don't get picked up from css for some reason      
        markerElement.className='Marker';
        markerElement.style.height = '16px';
        markerElement.style.width = '16px';
        markerElement.style.zIndex = '2';
        markerElement.style.transform = transformString;
        markerElement.id = `Marker_${message[0]},${message[2]}`
        markerElement.style.position = 'absolute';
  
        this.body.appendChild(markerElement);

        markerElement.src = assetLocation;
        this.markerBlockMap.set(markerID,assetLocation); 

        if(message[4].includes('sos')){
          
          console.log('Animating SOS marker');

          this.animateSOS(markerElement, transformString);
         
        }
        
        //this.markerBlockMap.forEach((v,k)=>{
        //  console.log("v : " + v, "k: " + k);
        //});

      }

      // IF THE ELEMENT ALREADY HAS A MARKER ON IT DO THIS
      else{

        console.log("Replace existing marker : " + markerID );

        const markerElement:HTMLImageElement = document.getElementById(markerID) as HTMLImageElement;
        markerElement.src = assetLocation;
        const transformString = markerElement.style.transform;
        this.markerBlockMap.set(markerID,assetLocation);

        if(message[4] === 'sos'){
          
          this.animateSOS(markerElement,transformString);
         
        }
      }
      console.log('Placed Marker @ ' + `GridDiv_${message[0]},${message[2]}` );
    }
  }
  catch(error){

    console.log('Something went wrong placing the marker blocks');
    console.log(error);

  }
}
updatePlayerPosition( message ): void{

  try {

    let gridID = `GridDiv_${message[0]},${message[2]}`;

    //console.log(gridID);

    //player is in hallway
    if (message[2] > this.boundedZCoord){
      gridID = `GridDiv_${message[0]},${this.boundedZCoord}`;
      //console.log(gridID);
    } 

    const callSign =message[4]
    let lastDiv: HTMLElement = null;

    if (callSign === 'Red'){
      
      if( this.playerElementRed == null ){

        this.playerElementRed = document.getElementById('PlayerRed') as HTMLImageElement;
    
        this.playerElementRed.src = environment.hostpath + 'assets/player_red.png';
         
        if ( this. playerRadius == null ){
          this.playerRadius = this.playerElementRed.clientWidth;
        }
      }

      lastDiv = this.lastDivRed;
    }
    else if (callSign === 'Green'){
      
      if( this.playerElementGreen == null ){

        this.playerElementGreen = document.getElementById('PlayerGreen') as HTMLImageElement;
    
        this.playerElementGreen.src = environment.hostpath + 'assets/player_green.png';
        
        if ( this. playerRadius == null ){
          this.playerRadius = this.playerElementGreen.clientWidth;
        }
      }

      lastDiv = this.lastDivGreen;
    }
    else if (callSign === 'Blue'){
      if( this.playerElementBlue == null ){

        this.playerElementBlue = document.getElementById('PlayerBlue') as HTMLImageElement;
    
        this.playerElementBlue.src = environment.hostpath + 'assets/player_blue.png';

        if ( this. playerRadius == null ){
          this.playerRadius = this.playerElementBlue.clientWidth;
        }
        
    
      }   
      lastDiv = this.lastDivBlue;
    }

    // only update if the position has changed
    if ( (lastDiv === null) || (gridID.localeCompare(lastDiv.id) !== 0) ) {
      // change this to use element refs instead, probably a better idea
      const element = document.getElementById(gridID);  
      
      if (element !== null){

        const rect = element.getBoundingClientRect();
        const x = rect.x;
        const y = rect.y;
        
        let playerElement:HTMLImageElement = null;

        const callsign = message[4];

        if( callsign === 'Red'){
          playerElement = this.playerElementRed;

          this.lastDivRed = element;
        }
        else if( callsign === 'Blue'){
          playerElement = this.playerElementBlue;

          this.lastDivBlue = element;
        }
        else if(callsign === 'Green'){
          playerElement = this.playerElementGreen;

          this.lastDivGreen = element;
        }
        
        playerElement.style.transform = `translate(${x + (rect.width / 2) - 5}px,${ y + (rect.height / 2) - 5}px)`;

        

      }
      else{
        console.log('Position out of map scope.');
      }
    }
    
  }
    
  catch(error){
    console.log("Failure parsing position message on playerPositionUpdate : ", error);
  
  }  

}

updateHeatmap(message:HeatmapIntervention, action: string){
  


  // Z DIRECTION IS "UP/DOWN" IN CLIENTMAP
  // WALKING UP DECREASES Z, WALKING DOWN INCREASES Z

  // X DIRECTION IS "LEFT/RIGHT" IN CLIENTMAP
  // WALKING LEFT DECREASES X, WALKING RIGHT INCREASES X

  let topleftX = message.topLeft.x;
  let topleftZ = message.topLeft.z;

  let botrightX = message.bottomRight.x;
  let botrightZ = message.bottomRight.z;
 
  // ensures a minimum thickness of 3 in all directions
  if (topleftX === botrightX){
    topleftX--;
    botrightX++;
  }
  if( topleftZ === botrightZ ){
    
    topleftZ--;    
    botrightZ++;  
  }

   // if highlight is below the map
   if(botrightZ > this.boundedZCoord){

    topleftZ = this.boundedZCoord-2;
    botrightZ = this.boundedZCoord;
  }  
  
  for (let i = topleftZ; i <= botrightZ; i++){
    //console.log('i '+i);
    for (let j = topleftX; j <=botrightX; j++){
      const div_id = `GridDiv_${j},${i}`;
      //console.log(div_id)
      const div = document.getElementById(div_id);
      //console.log(div_id);
      if (div !== null){
        switch(action){
          case Action.START:
            div.className = "heatmap";
            break;
          case Action.STOP:
            div.className = null;
            break;
          case Action.PAUSE:
            div.className = "heatmap-stable";
            break;
          default:
            div.className = null;
            break;

        }
      }
        
    }
  }
}

// message is "start" or "stop"
processBlackoutPerturbation(message:string){

  try{    

    if(message === "start"){
      
      this.blackoutImage.style.zIndex = '5';
    }
    else if ( message === "stop"){
      this.blackoutImage.style.zIndex = '-1';
    }

  }
  catch(error){

    console.log(error)

  }
  
}

triggerQRCode(message:string){

  try{    

    if(message){
      
      this.qrImage.style.zIndex = '5';

      // Setup timer to turn off QR Code
      setTimeout( () => {
        this.qrImage.style.zIndex = '-1';
      }, 5000);
    }
    else {
      this.qrImage.style.zIndex = '-1';
    }

  }
  catch(error){

    console.log(error)

  }
  
}

animateSOS(markerElement:HTMLElement, transformString){

  markerElement.animate([      
    // keyframes
    
    { transform: transformString+'scale(1)' },
    { transform: transformString+'scale(1.5)' },
    { transform: transformString+'scale(1)' },
    
    ], {
    // timing options
    duration: 1000,
    iterations: Infinity
  });

}

}