import { AfterViewInit, Component, Inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TrialDTO, ExperimentDTO } from '../Interface/DTO';
import { ExperimentService } from '../Services/experiment.service';
import { WebsocketService } from '../Services/websocket.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ExperimentDialogComponent } from '../experiment-dialog/experiment-dialog.component';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-mission-runner',
  templateUrl: './mission-runner.component.html',
  styleUrls: ['./mission-runner.component.css']
})
export class MissionRunnerComponent implements AfterViewInit {

  baseUrl;
  missionScript = 'TestScript.py';
  associatedFile = ' Not Set ';
  mapName = 'Test';
  instanceNumber = '';
  PIP = true;
  mod = 'Asist';
  showAsistMissions = true;
  killContainerInProgress = false;

  trialDTO: TrialDTO;

  experimentDTO: ExperimentDTO;

  experimentService;
  websocketService: WebsocketService;

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string, experimentService: ExperimentService,
  webSocketService: WebsocketService, public dialog: MatDialog ) {

    this.baseUrl = baseUrl;
    this.experimentService = experimentService;
    this.websocketService = webSocketService;

  }

  ngAfterViewInit(): void {
    
    const killContainerIcon: HTMLImageElement = document.getElementById('killcontainerimg') as HTMLImageElement;
    killContainerIcon.src =  environment.hostpath + 'assets/icons/stop_container.png';
  }
  
  launchExperimentDialog() {   

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;

    const dialogRef = this.dialog.open( ExperimentDialogComponent, dialogConfig);

    dialogRef.afterClosed().subscribe( dtos => {
        if (dtos !== 'canceled') {
          this.trialDTO = dtos.trialDTO;
          this.experimentDTO = dtos.experimentDTO;          
        }
      }
    );
  }



  public test() { 
    console.log('pip : ' + this.PIP);
    console.log('mod : ' + this.mod);
    if ( this.mod === 'Asist') {
      this.showAsistMissions = true;
    } else {
      this.showAsistMissions = false;
    }
  }


  public stopTrial() {

    
    this.http.get<TrialDTO>(this.baseUrl + 'api/Experiment/stopTrial').subscribe(response => {
       console.log(response);       
       this.trialDTO = response;
       this.experimentService.trial_running = 'False';       
    });
    this.killContainer();
  }

  public forceContainerKill(){
    let text = "WARNING: Are you sure you want to stop the Minecraft Server outside the context of a trial? This should only be done if you've refereshed MalmoControl and are sure the Minecraft Server needs to be forcibly stopped. Check Dozzle (...:9000/Logger/) to see if it's still running.";    
    if(confirm(text) === true){
      this.killContainer()
    } 
  }

  public killContainer(){    
    this.killContainerInProgress = true;
    this.http.get<TrialDTO>(this.baseUrl + 'api/Experiment/killContainer').subscribe(response => {
      console.log(response);
      this.killContainerInProgress = false;
      this.experimentService.minecraftContainerInitialized = 'False';
      this.experimentService.asistModIsReady = 'False';
      this.experimentService.modLoadingProgress = 0;
    });    
  }

}




