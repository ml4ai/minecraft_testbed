import { Injectable, ChangeDetectorRef, EventEmitter } from '@angular/core';

import { WebsocketService } from './websocket.service';
import { ClientInfoDTO, InterventionAgentsDTO, MissionDTO, ObserverInfoDTO, RoleTextDTO, TrialDTO } from '../Interface/DTO';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface AgentContainer {
  name: string,
  version: string,
  lastUpdate: Date
}

@Injectable({
  providedIn: 'root'
})
export class ExperimentService {

  public experiment_id = null;
  public experiment_name = null;
  public experiment_author = null;
  public experiment_mission = null;

  public trial_name = null;
  public trial_experimenter = null;
  public trial_subjects = null;
  public trial_notes = null;
  public trial_number = null;
  public trial_group_number = null;
  public trial_study_number = null;
  public trial_condition = null;
  public trial_experiment_mission = 'Test';
  public trial_intervention_agent = null;

  public trial_experiment_missionIndex = 0;

  public trial_id = null;
  public trial_id_unique = true;

  public trialDTO: TrialDTO = null;
  public trial_running = 'False';
  public mission_running = 'False';
  public mod = 'Not Set';


  public malmoIsReady = 'False';
  public asistModIsReady = 'False';
  public minecraftIsReady = 'False';
  public minecraftContainerInitialized = 'False';
  public elkContainerInitialized = 'False';
  public agentContainerInitialized = 'False';
  public experimentDataStoreInitialized = 'False';
  public messageValidatorInitialized = 'False';
  public messageValidatorActive = 'False';
  public experimentRunning = 'False';
 

  public modLoadingProgress = 5;

  public testbed_version = 'NOT SET';
  public config_received = false;

  public mission_list = [];
  public intervention_agents: InterventionAgentsDTO[] = [];
  public asi_list=['Placeholder 1','Placeholder 2', 'Placeholder 3'];
  public agent_running = false;
  
  public asi_rollcall_ids = ['ASI_CMU_TA1_ATLAS','atomic_agent','ASI_CRA_TA1_psicoach','ASI_DOLL_TA1_RITA','sift_asistant','ASI_UAZ_TA1_ToMCAT']
  

  public callsign_list = [];
  
  public missionDTO: MissionDTO =  {
    MissionName : "Not Set",
    MapName: "Not Set",
    MapBlockFilename: "Not Set",
    MapInfoFilename: "Not Set",
    ObserverInfo: [] 
  }

  agentContainers: AgentContainer[] = []
  public allAgentsStatus = 'GOOD';


  // ClientInfo
  columnDefs = [
    {
      field: "playername",
      headerName: "Playername",
      width: "200px",
      cellStyle: { "text-align": "left" },
    },
    {
      field: "callsign",
      headerName: "Call Sign",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: ['Red','Green','Blue', 'Red_Audio', 'Green_Audio', 'Blue_Audio']
      }
    },
    {
      field: "participant_id",
      headerName: "Participant Id",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true
    },
    {
      field: "staticmapversion",
      headerName: "Static Map Version",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: ['SaturnA_24', 'SaturnA_34', 'SaturnA_64', 'SaturnB_24', 'SaturnB_34', 'SaturnB_64','']
      }
    },
    {
      field: "markerblocklegend",
      headerName: "Marker Block Legend",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: ['A_Anne', 'B_Sally','']
      }
    },
    {
      field: "unique_id",
      headerName: "Unique Id",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true
    },
    {
      headerName: 'Delete',
      cellRenderer: 'buttonRenderer',
      cellRendererParams: {
        onClick: this.onDeleteButtonClick.bind(this),
        label: 'Delete'
      }
    }
  ];
  public clientInfo: ClientInfoDTO[] = [];

  public gridOptions = {
    rowData: this.clientInfo,
    columnDefs: this.columnDefs,
    stopEditingWhenGridLosesFocus: true,
    singleClickEdit: true,

    api: null,
  };

  // ObserverInfo
  obsColumnDefs = [
    {
      field: "playername",
      headerName: "Playername",
      width: "200px",
      cellStyle: { "text-align": "left" },
      editable: true
    }
  ];
  public observerInfo: ObserverInfoDTO[] = [];

  public obsGridOptions = {
    rowData: this.observerInfo,
    columnDefs: this.obsColumnDefs,
    stopEditingWhenGridLosesFocus: true,
    singleClickEdit: true,
    
    api: null,
  };

  webSocketService;

  rollCallEmitter:EventEmitter<string>=new EventEmitter<string>();
  
  constructor(websocketservice: WebsocketService, private _snackBar:MatSnackBar ) {

    this.webSocketService = websocketservice;
    this.addWSMessageListeners();
    this.mod = this.webSocketService.mod;

   }

  public addWSMessageListeners() {   

    this.webSocketService.hubConnection.on('minecraftContainerUp', (message) => {

      console.log('Received MinecraftContainerUp Message from: AsistMod');      

      this.minecraftContainerInitialized = message.data; 
      
      if (message.data == 'Restart'){        

        this._snackBar.open(
          "MapBlock Loading Error: Restarting Minecraft up to 5 times.",
          null,
          { duration: 5000 }
        ).afterDismissed().subscribe( () => {
          this.minecraftContainerInitialized = 'True';
        });      

      }

      if (message.data == 'Fail'){        

        this._snackBar.open(
          "5 Restarts have failed. Something must be critically wrong with the Minecraft container. ",
          null,
          { duration: 5000 }
        )     

      }

    });

    this.webSocketService.hubConnection.on('minecraftIsReady', (message) => {

      console.log('Received minecraftIsReady Message from: AsistMod');      

      this.asistModIsReady = message.data;      

    });

    this.webSocketService.hubConnection.on('minecraftLoadingProgress', (message) => {

      console.log('Received minecraftLoadingProgress : ');
      console.log(message);


      this.modLoadingProgress = message.loaded; 
      
      if(message.loaded == 100){
        this.asistModIsReady = 'True';
      }

    });

    this.webSocketService.hubConnection.on('restartTrialDTO', (message) => {
      console.log('Received restartTrialDto : ');
      console.log(message);

      this.trialDTO = message;
    });

    this.webSocketService.hubConnection.on('agentHeartbeats', (message) => {
      console.log('m', message)
      let obj = JSON.parse(message.data);
      let entry = {
        component: obj['msg']['source'],
        state: obj['msg']['state']
      }

      for(let agent of this.agentContainers){
        if (agent.name === entry['component']) {
          agent['lastUpdate'] = new Date();
          // console.log(agent.name, 'updated')
        }
      }
      if(entry.state !== 'ok') {
        this.allAgentsStatus = 'NOT OK'
      } else {
        this.allAgentsStatus = 'GOOD'

      }
      let currentTime = new Date();
      for(let a of this.agentContainers){
        if(currentTime.getTime() - a.lastUpdate.getTime() > 300000){
          this.allAgentsStatus = 'NOT OK'
          break
        }

        if(currentTime.getTime() - a.lastUpdate.getTime() > 60000){
          this.allAgentsStatus = 'OK'
        }
      }

    });

    this.webSocketService.hubConnection.on('allContainers', (message) => {
      let obj = JSON.parse(message.data);
      let entry = {
        name: obj['data']['agent_name'],
        version: obj['data']['version'],
        lastUpdate: new Date(obj['header']['timestamp'])
      }

      let newAgent = true;
      for(let [i, agent] of this.agentContainers.entries()){
        if (agent.name === obj['data']['agent_name']) {
          this.agentContainers.splice(i, 1, entry)
          newAgent = false
        }
      }
      if(newAgent) {
        this.agentContainers.push(entry)
      }

      let currentTime = new Date();
      for(let a of this.agentContainers){
        if(currentTime.getTime() - a.lastUpdate.getTime() > 300000){
          this.allAgentsStatus = 'NOT OK'
          break
        }

        if(currentTime.getTime() - a.lastUpdate.getTime() > 60000){
          this.allAgentsStatus = 'OK'
          break
        }
      }
    });


    this.webSocketService.hubConnection.on('messageValidatorInitialized', (message) => {
      this.messageValidatorInitialized = message.data;
    });

    this.webSocketService.hubConnection.on('messageValidatorActive', (message) => {
      this.messageValidatorActive = message.data;
    });

    this.webSocketService.hubConnection.on('agentContainerInitialized', (message) => { 
      this.agentContainerInitialized = message.data; });

    this.webSocketService.hubConnection.on('experimentDataStoreInitialized', (message) => {
      this.experimentDataStoreInitialized = message.data; });

    this.webSocketService.hubConnection.on('experimentRunning', (message) => { this.experimentRunning = message.data; });   

    this.webSocketService.hubConnection.on('rollcallResponse', (message) => {



      if (message != null && message.msg != null && message.msg.source != null && message.msg.source != '') {
        
        const newInterventionAgent = message.msg.source;

        if( this.asi_rollcall_ids.includes(newInterventionAgent) ){
          this.rollCallEmitter.emit(newInterventionAgent);
        }

        this.intervention_agents.push({
          AgentName: newInterventionAgent
        });

        console.log('Received rollcallResponse: ' + newInterventionAgent);    

      }

    });
  }

  public isTrialRunning(): boolean {

    return  this.trial_running === 'True';

  }

  onDeleteButtonClick(params) {
    this.gridOptions.api.applyTransaction({remove: [params.data]});
  }

  
  onAddRow()
   {
     this.obsGridOptions.api.updateRowData({
        add: [{ playername: 'ChangeMe' }]
     });
  
   }
}
