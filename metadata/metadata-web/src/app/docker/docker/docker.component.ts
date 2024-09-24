import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { map, startWith } from 'rxjs/operators';
import { DockerService } from '../docker.service';
import {Subscription, timer} from 'rxjs';
import { MatListOption, MatSelectionList, MatSelectionListChange } from '@angular/material/list';
import { SelectionModel } from '@angular/cdk/collections';
import { AgentService } from '../agent.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';

@Component({
  selector: 'app-docker',
  templateUrl: './docker.component.html',
  styleUrls: ['./docker.component.scss']
})
export class DockerComponent implements OnInit, OnDestroy {
  private dockerOnlineSubscription: Subscription;

  @ViewChild('containerList') matSelectionList: MatSelectionList;

  containers: any = {};
  statistics: any = {};
  selectedContainer: any = null;
  dockerOnline: boolean;
  selectedContainerLog: string[] = [];
  agents: string[] = [];
  agentLog = ''; // 'b1124ca78a7a Extracting [==================================================>]  40.41MB/40.41MB';

  private metadataAgentLogSubscription: Subscription;

  constructor(
    private dockerService: DockerService,
    // private agentService: AgentService,
    private mqttService: MqttService) {
    this.metadataAgentLogSubscription = this.mqttService.observe('metadata/agent/log').subscribe((message: IMqttMessage) => {
      const output = new TextDecoder('utf-8').decode(message.payload);
      // const logMessage = JSON.parse(output);
      // const decodedString = atob(logMessage.encoded_string);
      console.log(output);
      this.agentLog = output;
    });
  }

  ngOnInit(): void {
    this.containerStatusTimer();
    this.agentList();
    this.dockerOnlineSubscription = this.dockerService.isDockerOnline.subscribe(isOnline => this.dockerOnline = isOnline);
  }

  ngOnDestroy(): void {
    this.dockerOnlineSubscription.unsubscribe();
    this.metadataAgentLogSubscription.unsubscribe();
  }

  containerStatusTimer(): void {
    const source = timer(0, 10000);
    source.subscribe(val => {
      this.ping();
      this.containerList();
    });
  }

  ping(): void {
    this.dockerService.ping().subscribe(online => {
      this.dockerOnline = online;
    });
  }

  containerList(): void {
    this.dockerService.containerList().subscribe(containers => {
      // Remove any old containers that are not in new list
      const currentContainerIds = Object.keys(this.containers);
      currentContainerIds.forEach(id => {
        if (containers.findIndex(c => {
          return c.Id === id;
        }) === -1) {
          delete this.containers[id];
          delete this.statistics[id];
        }
      });
      // Update container list
      containers.forEach(container => {
        this.containers[container.Id] = container;
        if (this.selectedContainer && this.selectedContainer.Id === container.Id) {
          this.selectedContainer = container;
        }
        // Stats
        this.containerStats(container.Id);
      });
    });
  }

  agentList(): void {
    this.dockerService.agentList().subscribe(agents => {
      console.log('agents: ' + agents);
      this.agents = agents;
    });
  }

  containerLog(Id: string) {
    this.dockerService.containerLog(Id).subscribe(log => {
      this.selectedContainerLog = log;
    });
  }

  onSelectionChange($event) {
    this.selectedContainer = $event.option?.value;
    this.containerLog(this.selectedContainer.Id);
  }

  isSelected(Id: string) {
    if (this.selectedContainer) {
      return (this.selectedContainer.Id === Id);
    }
  }

  compare(c1: {Id: string}, c2: {Id: string}) {
    return c1 && c2 && c1.Id === c2.Id;
  }

  startContainer(id: string) {
    this.agentLog = '';
    this.dockerService.startContainer(id).subscribe(container => {
      this.selectedContainer = container;
      this.containers[id] = container;
    });
  }

  stopContainer(id: string) {
    this.agentLog = '';
    this.dockerService.stopContainer(id).subscribe(container => {
      this.selectedContainer = container;
      this.containers[id] = container;
    });
  }

  containerLogDownload(Id: string) {
    this.dockerService.containerLogDownload(Id).subscribe(response => {
      const dataType = response.type;
      const binaryData = [];
      binaryData.push(response);
      const downloadLink = document.createElement('a');
      downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {type: dataType}));
      downloadLink.setAttribute('download', `${Id}.txt`);
      document.body.appendChild(downloadLink);
      downloadLink.click();
    });
  }

  containerLogsDownload() {
    this.dockerService.containerLogsDownload().subscribe(response => {
      const dataType = response.type;
      const binaryData = [];
      binaryData.push(response);
      const downloadLink = document.createElement('a');
      downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {type: dataType}));
      downloadLink.setAttribute('download', 'dockerlogs.zip');
      document.body.appendChild(downloadLink);
      downloadLink.click();
    });
  }

  containerStats(Id: string) {
    this.dockerService.containerStats(Id).subscribe(stats => {
      this.statistics[Id] = stats[0];
    });
  }

  calcCpuPercent(Id: string) {
    // cpu_delta = cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage
    // system_cpu_delta = cpu_stats.system_cpu_usage - precpu_stats.system_cpu_usage
    // number_cpus = length(cpu_stats.cpu_usage.percpu_usage) or cpu_stats.online_cpus
    // (cpu_delta / system_cpu_delta) * number_cpus * 100.0
    const stats = this.statistics[Id];
    if (stats) {
      const cpu_delta = stats.cpu_stats.cpu_usage.total_usage - stats.precpu_stats.cpu_usage.total_usage;
      const system_cpu_delta = (stats.cpu_stats.system_cpu_usage ? stats.cpu_stats.system_cpu_usage : 0) - (stats.precpu_stats.system_cpu_usage ? stats.precpu_stats.system_cpu_usage : 0);
      const number_cpus = stats.cpu_stats.online_cpus ? stats.cpu_stats.online_cpus : (stats.cpu_stats.cpu_usage.percpu_usage ? stats.cpu_stats.cpu_usage.percpu_usage.length : 1);
      return ((cpu_delta / system_cpu_delta) * (number_cpus * 100.0)).toFixed(2);
    }
  }

  calcMemPercent(Id: string) {
    // used_memory = memory_stats.usage - memory_stats.stats.cache
    // available_memory = memory_stats.limit
    // (used_memory / available_memory) * 100.0
    const stats = this.statistics[Id];
    if (stats) {
      const used_memory = stats.memory_stats.usage ? stats.memory_stats.usage : 0 - stats.memory_stats.stats ? (stats.memory_stats.stats.cache ? stats.memory_stats.stats.cache : 0) : 0;
      const available_memory = stats.memory_stats.limit;
      return ((used_memory / available_memory) * 100.0).toFixed(2);
    }
  }

  agentUp(agent: string) {
    this.agentLog = `Calling up on agent: ${agent}`;
    this.dockerService.agentUp(agent).subscribe(output => {
      // console.log(output);
    });
  }

  agentDown(agent: string) {
    this.agentLog = `Calling down on agent: ${agent}`;
    this.dockerService.agentDown(agent).subscribe(output => {
      // console.log(output);
    });
  }

  // agentUp(agent: string) {
  //   this.agentService.agentUp(agent).subscribe(output => {
  //       console.log(output);
  //       this.agentLog = output;
  //     });
  //   // this.dockerService.agentUp(agent).subscribe(output => {
  //   //   console.log(output);
  //   //   this.agentLog = output;
  //   // });
  // }
}
