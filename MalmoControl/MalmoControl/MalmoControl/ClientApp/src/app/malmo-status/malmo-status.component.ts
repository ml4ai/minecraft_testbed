import { Component, Inject } from '@angular/core';
import { ExperimentService } from '../Services/experiment.service';
import { AgentService } from '../Services/agent.service';
import {ThemePalette} from '@angular/material/core';
import { HttpClient } from '@angular/common/http';
import { AgentControlDTO } from '../Interface/DTO';
import { MatDialog } from '@angular/material/dialog';
import { ContainerDetailsDialogComponent } from '../container-details-dialog/container-details-dialog.component';

@Component({
  selector: 'app-malmo-status',
  templateUrl: './malmo-status.component.html',
  styleUrls: ['./malmo-status.component.css']
})
export class MalmoStatusComponent {

  public baseUrl: string;

  public experimentService: ExperimentService;
  public agentService: AgentService;
  color: ThemePalette = 'primary';

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string,
    experimentService: ExperimentService, agentService: AgentService,
    public dialog: MatDialog) {

    this.baseUrl = baseUrl;

    this.experimentService = experimentService;
    this.agentService = agentService;

  }

  public isAsist( ): boolean {

      return this.experimentService.mod === 'asist';

  }

  public toggleValidator() {
    const controlDTO: AgentControlDTO = {
      'header' : {
        'timestamp' : 'NOT SET',
        'message_type' : 'NOT SET',
        'version' : '0.5'
      },
      'msg' : {
        'trial_id': this.experimentService.trial_id,
        'command': 'NOT SET',
        'experiment_name': this.experimentService.experiment_name
      }
    };

    if (this.experimentService.messageValidatorActive === 'True') {
      controlDTO.msg.command = 'stop';
      this.http.put(this.baseUrl + 'api/MQTTValidation/stopValidation', controlDTO , { responseType: 'json' }).subscribe(response => {
      },
        error => console.error(error)
      );
    } else {
      controlDTO.msg.command = 'start';
      this.http.put(this.baseUrl + 'api/MQTTValidation/startValidation', controlDTO , { responseType: 'json' }).subscribe(response => {
      },
        error => console.error(error)
      );
    }
  }

  viewContainerDetails(){
    const dialogRef = this.dialog.open(ContainerDetailsDialogComponent, {
      data: this.experimentService.agentContainers
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });

  }

}
