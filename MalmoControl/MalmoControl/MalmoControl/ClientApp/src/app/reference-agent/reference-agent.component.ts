import { Component, OnInit, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AgentService } from '../Services/agent.service';
import { AgentControlDTO } from '../Interface/DTO';
import { ExperimentService } from '../Services/experiment.service';

@Component({
  selector: 'app-reference-agent',
  templateUrl: './reference-agent.component.html',
  styleUrls: ['./reference-agent.component.css']
})
export class ReferenceAgentComponent implements OnInit {

  public baseUrl: string;
  public status: any = 'Agent Not Started';
  public agentActionString = 'Init';
  public experimentService;

  public agentService;

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string, agentService: AgentService,
  experimentService: ExperimentService) {

    this.baseUrl = baseUrl;
    this.agentService = agentService;
    this.experimentService = experimentService;

  }

  ngOnInit() {

  }

  public agentAction() {

    // create message dto object
    const agentControlDTO: AgentControlDTO = {
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

    // if message is init
    if (this.agentActionString === 'Init') {
      if ( this.experimentService.trial_running === 'True') {
        agentControlDTO.msg.command = 'init';

        this.http.put(this.baseUrl + 'api/Agent/initAgent', agentControlDTO , { responseType: 'json' }).subscribe(response => {
          this.status = response;
          this.agentActionString = 'Start';

        },
        error => console.error(error)
      );
      } else {
        alert(' Please Create a Trial and Run a Mission first!');
      }
    } else if (this.agentActionString === 'Start') {
      if ( this.experimentService.trial_running === 'True') {agentControlDTO.msg.command = 'start';

        this.http.put(this.baseUrl + 'api/Agent/startAgent', agentControlDTO , { responseType: 'json' }).subscribe(response => {
          this.status = response;
          this.agentService.agent_running = 'True';
          this.agentActionString = 'Stop';
        },
          error => console.error(error)
        );
      } else {
        alert(' Please Create a Trial and Run a Mission first!');
      }
    } else if (this.agentActionString === 'Stop') {

      agentControlDTO.msg.command = 'stop';

      this.http.put(this.baseUrl + 'api/Agent/stopAgent', agentControlDTO , { responseType: 'json' }).subscribe(response => {
        this.status = response;
        this.agentService.agent_running = 'False';
        this.agentActionString = 'Init';
      },
        error => console.error(error)
      );
    }
   }
}
