import { AfterContentInit, Component, OnInit } from '@angular/core';
import { MatDialog} from '@angular/material/dialog';
import { WebsocketService } from '../websocket.service';
import { SurveyComponent } from '../survey/survey.component';
import { Survey } from '../survey';
import { SurveyService } from '../survey.service';
import { AudioWebsocketService } from '../Services/audiowebsocket.service';
import { SessionService } from '../Services/session.service';
import { environment } from 'src/environments/environment';
import { HeatmapIntervention, TextIntervention, Position, Intervention } from '../types';

import Speech from 'speak-tts';

@Component({
  selector: 'app-interaction-pane',
  templateUrl: './interaction-pane.component.html',
  styleUrls: ['./interaction-pane.component.scss']
})
export class InteractionPaneComponent implements OnInit, AfterContentInit {

  MBLegendImage: HTMLImageElement;
  //debug: boolean = false;
  minutes: any;
  seconds: any;
  interventionStart = [];
  selectedSurvey: Survey;
  surveys: Survey[] = [];
  audioEnabled: boolean;
  constraints = {audio : true, video : false};
  context: AudioContext;
  audioStream: any;
  unique_id: string;
  participant_id: string;
  trialStarted: boolean;
  audioSending: boolean;
  missionStarted = false;
  startConnection: boolean = false;
  roleText: string[] = [];

  // FROM ADAPT  
  currentPlayerTextRec: TextIntervention;
  currentPlayerHeatRec: HeatmapIntervention;
  otherPlayers = new Map<String, TextIntervention>();
  playerMap = new Map<String, String>();
  correctHeatmap = false;
  speech = new Speech();
  counter: number = 0;
  
  //list of interventions to be displayed
  interventionsMap = new Map<number, Intervention>();
  textInterventions: TextIntervention[] = [];
  mapInterventions: HeatmapIntervention[] = [];

  puzzleImagePath = "Not Set";


  constructor( public sessionService:SessionService, public webSocketService: WebsocketService, private surveyService: SurveyService, public dialog: MatDialog, private audioWebsocketService: AudioWebsocketService ) { 

  }

  ngOnInit(): void {
    this.getSurveys();
    this.speech.init();
    

  }

  ngAfterContentInit(){

    if(this.webSocketService.playerName == 'asist_advisor'){
      
      this.webSocketService.positionEmitter.subscribe( (message: [number,number,number,string] ) => 
      
        this.updateTimer(message)
      );

    }
    else{

      this.webSocketService.roleEmitter.subscribe( (message: any) => {

        const mission:string = this.sessionService.currentMission;       
  
        if ( message === "Medical_Specialist"){         
          
          if ( mission.startsWith('Saturn_A',0)){            
  
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Medic_SaturnA.png';            
            
          }
          else if ( mission.startsWith('Saturn_B',0)){
            
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Medic_SaturnB.png';
  
          }
  
          else if ( mission.startsWith('Saturn_C',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Medic_SaturnC.png';

          }
          else if ( mission.startsWith('Saturn_D',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Medic_SaturnD.png';

          }
          
        }
        else if ( message === "Transport_Specialist"){
          
          if ( mission.startsWith('Saturn_A',0)){            
  
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Transporter_SaturnA.png';            
            
          }
          else if ( mission.startsWith('Saturn_B',0)){
            
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Transporter_SaturnB.png';
  
          }
  
          else if ( mission.startsWith('Saturn_C',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Transporter_SaturnC.png';

          }
          else if ( mission.startsWith('Saturn_D',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Transporter_SaturnD.png';

          }
        }
  
        else if ( message === "Engineering_Specialist"){
         
          if ( mission.startsWith('Saturn_A',0)){            
  
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Engineer_SaturnA.png';            
            
          }
          else if ( mission.startsWith('Saturn_B',0)){
            
            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Engineer_SaturnB.png';
  
          }
  
          else if ( mission.startsWith('Saturn_C',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Engineer_SaturnC.png';

          }
          else if ( mission.startsWith('Saturn_D',0)){

            this.puzzleImagePath = environment.hostpath + 'assets/RoleBasedImages/Engineer_SaturnD.png';

          }
        }
      
      });
  
  
      this.webSocketService.unique_idEmitter.subscribe( (message) => {
        console.log("Updating uid: " + message);
        this.unique_id = message
      });
  
      this.webSocketService.participant_idEmitter.subscribe( (message) => {
        this.participant_id = message
      });
      
      this.webSocketService.positionEmitter.subscribe( (message: [number,number,number,string] ) => 
      
        this.updateTimer(message)
      );   
  
      this.webSocketService.missionStateEmitter.subscribe( (state: boolean) => {
  
        console.log("interaction-pane: missionStarted changed to " + state);
        
        this.missionStarted = state;
  
        const element: HTMLImageElement = document.getElementById("puzzle_image") as HTMLImageElement;
  
        element.src = this.puzzleImagePath;

        if( this.sessionService.currentMission.toLowerCase().includes("training") ){
          element.style.display = 'none';
        }
        else{
          element.style.display = 'block';
        }
        
        
        element.animate([      
            // keyframes
            { transform: 'scale(1)' },
            { transform: 'scale(1.05)' },
            { transform: 'scale(1)' }
            ], {
            // timing options
            duration: 1000,
            iterations: 10
          });     
  
      })
     
      this.webSocketService.trialActiveEmitter.subscribe( (message) => {
        console.log("Updating TrialStarted: " + message);
        this.trialStarted = message;
        this.missionStarted = false;

        if (message == false){
          
          const element: HTMLImageElement = document.getElementById("puzzle_image") as HTMLImageElement;

          element.style.display = 'none';
        }
  
        this.updateAudioState();
      });

      
  
      // interventions
      this.webSocketService.textInterventionEmitter.subscribe((message: [string, string, string, string]) => {
        const text = message[0];
        const start = message[1];
        if (start === '-1:-1'){
          return;
        }
        const end = message[2];
        const receiver = message[3];
        const time = this.minutes + ":" + this.seconds;
        const id = this.counter++;
  
        //this.textInterventions.push({ start: start, end: end, text: text, receiver: receiver, time: time});
  
        this.interventionsMap.set(id, { start: start, end: end, text: text, receiver: receiver, time: time, type: "TextIntervention", id: id, status: "not started" } as TextIntervention);
  
      });
  
      this.webSocketService.heatmapInterventionEmitter.subscribe((message: [string, string, Position, Position]) => {
  
        const start = message[0];
        const end = message[1];
        const topLeft = message[2];
        const bottomRight = message[3];
        const id = this.counter++;
  
        //this.mapInterventions.push({id: id, start: start, end: end, topLeft: topLeft, bottomRight: bottomRight, type:"HeatmapIntervention", status: "not started"})
  
        this.interventionsMap.set(id, { start: start, end: end, topLeft: topLeft, bottomRight: bottomRight, type: "HeatmapIntervention", status: "not started", id: id } as HeatmapIntervention);
      });

    }   


  }

  emitDebugMode(){

    //this.webSocketService.debugMode = this.debug;

    //console.log("Debug Mode : " + this.webSocketService.debugMode);

  }

  updateTimer( message: [number,number,number,string]): void{
    
    try {

      const timeString = message[3];

      // console.log(message);
      const regExp = RegExp('^[0-9]{1,2}[ ]{0,1}:[ ]{0,1}[0-9]{1,2}$');

      if (regExp.test(timeString)) {

        //console.log('timestring: ' + timeString);

        const splitString = timeString.split(':');
        const minute = splitString[0];
        const second = splitString[1];

        if (this.isItTime(timeString)) {
          // DON'T UPDATE TIMER
        }
        else {
          //console.log('Updating: ' + minute,second);
          this.minutes = minute;
          this.seconds = second;

        }
        this.checkInterventions();
        //this.checkInterventionStart();
        //this.checkInterventionEnd();
      }
      else {

        //console.log('RegEx failed: ', timeString);
        this.minutes = -1;
        this.seconds = -1;

      }

    }
    catch (error) {
      console.log("Failed to parse time: ", error);
    }
  }

  checkInterventions() {

    this.interventionsMap.forEach((intervention) => {
      if (intervention.end === 'null' || intervention.end === null) {
        intervention.end = this.subtract30();
      }

      //check interventions to see where their status is. If they haven't been started and start is  null or it is the start time, then display the intervention
      if (intervention.status === "not started" && (intervention.start === 'null' || intervention.start === null || this.isItTime(intervention.start))) {
        if (intervention.type === "TextIntervention") {
          let textInt: TextIntervention = intervention as TextIntervention;

          if (textInt.receiver === this.sessionService.currentPlayerCallSign) {
            this.currentPlayerTextRec = textInt;
            this.speak(textInt.text);
          }
          else if (this.otherPlayers.has(this.playerMap.get(textInt.receiver))) {
            this.otherPlayers.set(this.playerMap.get(textInt.receiver), textInt);
          }
          textInt.status = "started";

        }
        else if (intervention.type === "HeatmapIntervention") {
          let mapInt: HeatmapIntervention = intervention as HeatmapIntervention;
          this.webSocketService.startHeatmapEmitter.emit(mapInt);
          this.currentPlayerHeatRec = mapInt;
          mapInt.status = "started";
        }

        //if this intervention has been started, then check if it needs to be removed  
      } else if (intervention.status === "started") {

        if (intervention.type === "TextIntervention" && this.isItTime(intervention.end)) {
          let textInt: TextIntervention = intervention as TextIntervention;
          this.interventionsMap.delete(textInt.id);

          //should probably figure out how to do heatmap stuff better so that it doesn't remove the color for new interventions along with old ones

          //There should only be one highlight intervention at any given time, so if there's a heatmap started that isn't the one we're supposed to be showing, it should get deleted
        } else if (intervention.type === "HeatmapIntervention") {
          let mapInt: HeatmapIntervention = intervention as HeatmapIntervention;

          if (mapInt != this.currentPlayerHeatRec) {
            this.webSocketService.stopHeatmapEmitter.emit(mapInt);
            this.interventionsMap.delete(mapInt.id);
            this.correctHeatmap = true;
          } else if (this.isItPastTime(intervention.end)){
            this.webSocketService.pauseHeatmapEmitter.emit(mapInt);
          } else if (this.correctHeatmap){
            //check if we've already corrected this?
            this.webSocketService.stopHeatmapEmitter.emit(mapInt);
            this.webSocketService.startHeatmapEmitter.emit(mapInt);
            this.correctHeatmap = false;
          }

        }
      }
    });
  }

  isItTime(time: string): boolean {

    const timerMins = parseInt(this.minutes);
    const timerSecs = parseInt(this.seconds);

    const splitString = time.split(':');
    const min = parseInt(splitString[0]);
    const sec = parseInt(splitString[1]);

    return (timerMins === min && timerSecs === sec);
  }

  isItPastTime(time: string): boolean {
    const timerMins = parseInt(this.minutes);
    const timerSecs = parseInt(this.seconds);
    const min = parseInt(time.split(':')[0])
    const sec = parseInt(time.split(':')[1])

    return (timerMins < min || (timerMins === min && timerSecs <= sec))
  }

  speak(text: string) {

    this.speech.volume = 0.2;
    this.speech.speak({ text: text }).catch(e => {
      console.error("An error occured when turning '" + text + "' into speech")
    });

  }

  subtract30() {

    const leftover = this.seconds - 30;

    //console.log("Leftover :  "+ leftover )
    let endmins = this.minutes;
    let endsecs = this.seconds;
    if (leftover >= 0) {
      endsecs = leftover;
      //console.log("Leftover GTZ:  endsecs :"+ endsecs )
    }
    else {
      endmins -= 1;
      endsecs = 60 + leftover

      //console.log("Leftover LTZ:  endsecs :"+ endsecs )
    }

    //console.log("Just before return :"+ endmins + ":" + endsecs )
    return (endmins + ":" + endsecs);
  }


  getSurveys(): void {
    this.surveyService.getSurveys()
        .subscribe(surveys => this.surveys = surveys['result']['elements']);
  }

  openSurveyDialog(survey: Survey): void {
    this.selectedSurvey = survey;
    const dialogRef = this.dialog.open(SurveyComponent, {
      panelClass: 'survey-dialog',
      width: '100%',
      height: '100%',
      disableClose: true,
      data: {
        id: this.selectedSurvey.id,
        name: this.selectedSurvey.name,
        unique_id: this.unique_id,
        participant_id: this.participant_id
      }
    });

  }
   
  audioSelectionChanged($event) {
    this.audioEnabled = $event.source.checked
    console.log('AudioEnabled: ' + this.audioEnabled)

    this.updateAudioState();
  }

  private updateAudioState() {
    
    console.log('CHECKING IF AUDIO NOT SENDING - updateAudioState from Interaction Pane.')
    if (!this.audioSending) {
      
      console.log('AUDIO WAS NOT SENDING - updateAudioState from Interaction Pane.')
      
      var context = this.getAudioContext();

      console.log('Check if Trial Started.')

      if (this.trialStarted && !this.startConnection) {

        console.log('Trial Started - updateAudioState from Interaction Pane.')
        
        this.audioEnabled = true;
        this.startConnection = true;
        // Start connection
        this.audioWebsocketService.startConnection(context.sampleRate).then(() => {
          if (this.audioWebsocketService.connectionActive) {
            // Start audio stream
            this.initRecording(context);
            this.audioSending = true;
            console.log("Recording Audio - Audio Sample rate: " + context.sampleRate);
          }
          else {
            this.audioEnabled = false;
            this.audioSending = false;
          }
          this.startConnection = false;        
        });
      }
    }
    else {
      console.log('AUDIO WAS SENDING - updateAudioState from Interaction Pane.')
      if (!this.trialStarted || !this.audioEnabled) {
        // Stop audio stream
        this.audioStream.getTracks().forEach(function(track) {
          if (track.readyState == 'live') {
              track.stop();
          }
        });
        this.context.close();

        // End connection
        if (this.audioWebsocketService.connectionActive) {
          this.audioWebsocketService.stopConnection();
        } 

        this.audioEnabled = false;
        this.audioSending = false;

        console.log("Stopped Recording Audio - Audio Sample rate: ");

      }
    }
  }
  private getAudioContext() {
      AudioContext = window.AudioContext;
      this.context = new AudioContext({
          // if Non-interactive, use 'playback' or 'balanced'
          // https://developer.mozilla.org/en-US/docs/Web/API/AudioContextLatencyCategory
          latencyHint : 'interactive',
      });
      return this.context;
  }

  private initRecording(context) {
    var self = this;
    var processor = context.createScriptProcessor(0, 1, 1);
      processor.connect(context.destination);
      context.resume();

      var handleSuccess = function(stream) {
          self.audioStream = stream;
          var input = context.createMediaStreamSource(stream);
          input.connect(processor);

          processor.onaudioprocess = function(e) { self.microphoneProcess(e); };
      };

      navigator.mediaDevices.getUserMedia(this.constraints).then(handleSuccess).catch((reason) => {        
      });
  }

  private microphoneProcess(e) {
      var channelData = e.inputBuffer.getChannelData(0);
      var len = channelData.length, i = 0;
      var dataAsInt16Array = new Int16Array(len);
      
      while(i < len)
        dataAsInt16Array[i] = convert(channelData[i++]);
      
      function convert(n) {
         var v = n < 0 ? n * 32768 : n * 32767;       // convert in range [-32768, 32767]
         return Math.max(-32768, Math.min(32768, v)); // clamp
      }

      if (this.audioEnabled) {
        console.log("Sending audio data");
        this.audioWebsocketService.sendAudioData(dataAsInt16Array.toString());
      }
  }
}

