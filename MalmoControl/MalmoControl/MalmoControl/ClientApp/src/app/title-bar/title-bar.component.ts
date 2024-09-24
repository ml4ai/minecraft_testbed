import { Component, OnInit, Inject } from '@angular/core';
import { environment } from 'src/environments/environment';
import { MatDialogConfig, MatDialog } from '@angular/material/dialog';
import { AboutDialogComponent } from '../about-dialog/about-dialog.component';
import { HelpDialogComponent } from '../help-dialog/help-dialog.component';
import { HttpClient } from '@angular/common/http';
import { ExperimentService } from '../Services/experiment.service';
import { ErrorViewerComponent } from '../error-viewer/error-viewer.component';

@Component({
  selector: 'app-title-bar',
  templateUrl: './title-bar.component.html',
  styleUrls: ['./title-bar.component.css']
})
export class TitleBarComponent implements OnInit {

  baseUrl;
  experimentService: ExperimentService;

  constructor( public dialog: MatDialog, private http: HttpClient, @Inject('BASE_URL') baseUrl: string,
  experimentService: ExperimentService ) {
    this.baseUrl = baseUrl;
    this.experimentService = experimentService;
  }

  ngOnInit() {

    const blockImage: HTMLImageElement = document.getElementById('block-image') as HTMLImageElement;
    blockImage.src =  environment.hostpath + 'assets/images/minecraft-block.png';
    const block2Image: HTMLImageElement = document.getElementById('block-image2') as HTMLImageElement;
    block2Image.src = environment.hostpath + 'assets/images/minecraft-block.png';

    const aboutImage: HTMLImageElement = document.getElementById('about-image') as HTMLImageElement;
    aboutImage.src =  environment.hostpath + 'assets/images/about.png';

    const helpImage: HTMLImageElement = document.getElementById('help-image') as HTMLImageElement;
    helpImage.src =  environment.hostpath + 'assets/images/help.png';

    const errorImage: HTMLImageElement = document.getElementById('error-image') as HTMLImageElement;
    errorImage.src =  environment.hostpath + 'assets/images/error.png';

    // gets config and instantiates the websocket by hitting a controller that uses it as a service
    this.http.get<any>(this.baseUrl + 'api/Help/getConfig').subscribe( (config) => {

      console.log(config);
      this.experimentService.mod = config.mod;
      this.experimentService.testbed_version = config.testbed_version;
      this.experimentService.mission_list = config.mission_list;
      this.experimentService.missionDTO.MissionName = this.experimentService.mission_list[0]
      this.experimentService.callsign_list = config.callsign_list; 
      this.experimentService.asi_list = ["No Agent"].concat( config.asi_list as Array<string> ) ;

      this.experimentService.trial_intervention_agent =  this.experimentService.asi_list[0]; 
      this.experimentService.config_received = true;   
      this.experimentService.intervention_agents = [
        {AgentName: "None"}
      ]
    });
  }

  alert() { alert( 'Under Construction!'); }

  launchAboutDialog() {

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    const dialogRef = this.dialog.open( AboutDialogComponent, dialogConfig);

  }

  launchHelpDialog() {

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    const dialogRef = this.dialog.open(HelpDialogComponent, dialogConfig);
  }

  launchErrorDialog() {

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    const dialogRef = this.dialog.open(ErrorViewerComponent, dialogConfig);
  }

}
