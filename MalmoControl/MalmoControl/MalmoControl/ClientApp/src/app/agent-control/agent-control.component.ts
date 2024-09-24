import { Component, Inject, OnInit, AfterContentInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ExperimentService } from '../Services/experiment.service';

@Component({
  selector: 'app-agent-control',
  templateUrl: './agent-control.component.html',
  styleUrls: ['./agent-control.component.css']
})
export class AgentControlComponent implements OnInit {

  active_agent = 'Not Set';
  last_response_time = 'Waiting';
  stopAgentInProgress = false;
  startAgentInProgress = false;

  time_div_element:HTMLDivElement = null;

  agent_response_id_map : Map<string,string> = new Map<string,string>();
  
  constructor( public experimentService:ExperimentService, public http: HttpClient, @Inject('BASE_URL') public baseUrl: string,) {

    // MAKE SURE TO ALSO MATCH THIS TO ASI ROLL CALL ID's IN EXPERIMENT SERVICE
    
    this.agent_response_id_map.set('ASI_CRA_TA1_psicoach','ASI_CRA_TA1_psicoach');
    this.agent_response_id_map.set('atomic_agent','atomic_agent');
    this.agent_response_id_map.set('ASI_CMU_TA1_ATLAS','ASI_CMU_TA1_ATLAS');
    this.agent_response_id_map.set('ASI_DOLL_TA1_RITA','ASI_DOLL_TA1_RITA');   
    this.agent_response_id_map.set('sift_asistant','sift_asistant');
    this.agent_response_id_map.set('ASI_UAZ_TA1_ToMCAT','ASI_UAZ_TA1_ToMCAT');

    experimentService.rollCallEmitter.subscribe( (name:string) => {

      if( this.agent_response_id_map.has( name )){
        //console.log(name);
        const agent = this.agent_response_id_map.get(name);
        if( agent === this.active_agent ){
          this.last_response_time = new Date().toLocaleTimeString();
          this.time_div_element.animate([      
            // keyframes
            { background: 'green' },
            { background: 'white' }
            ], {
            // timing options
            duration: 300,
            iterations: 1
          });     
        }
      }
    });
  }

  ngOnInit(): void {
  }

  ngAfterContentInit():void{

    this.time_div_element = document.getElementById('time_div') as HTMLDivElement;
    
  }

  launchAgent(){

    const agent_control_msg = {
      ['header'] :{},
      ['msg'] :{},
      ['data']:{
        ['agent_identifier']:this.experimentService.trial_intervention_agent,
        ['command']:'up'
      }
    }

    this.active_agent = this.experimentService.trial_intervention_agent;
    
    this.experimentService.agent_running = true;
    
    this.last_response_time = 'Waiting';

    this.http.put<any>(this.baseUrl + 'api/Agent/control', agent_control_msg).subscribe( (response) => {

      console.log(response);
            

    });  

  }

  stopAgent(){

    const agent_control_msg = {
      ['header'] :{},
      ['msg'] :{},
      ['data']:{
        ['agent_identifier']:this.experimentService.trial_intervention_agent,
        ['command']:'down'
      }
    }

    this.stopAgentInProgress = true;

    this.http.put<any>(this.baseUrl + 'api/Agent/control', agent_control_msg).subscribe( (response) => {

      console.log(response);
      this.stopAgentInProgress = false;
      this.experimentService.agent_running = false;

    });  

  }

  public assignInterventionAgent(event) {

    const indexFromSelect = event.target.selectedIndex;

    if (event.target.selectedIndex >= 0) {
      this.experimentService.trial_intervention_agent = this.experimentService.asi_list[indexFromSelect];
      
    }
    else {
      this.experimentService.trial_intervention_agent = null;
    }
  }

}
