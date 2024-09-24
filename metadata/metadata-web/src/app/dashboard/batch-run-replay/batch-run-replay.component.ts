import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { forkJoin, Observable, Subscription, timer } from 'rxjs';
import { Replay } from '../../replay/replay';
import { Trial } from '../../trial/trial';
import { IgnoreListItem } from '../../replay/ignore-list-item';
import {FormBuilder, FormControl, FormGroupDirective, Validators} from '@angular/forms';
import { ElasticsearchService } from '../elasticsearch';
import { LoggingService } from '../../logging/logging.service';
import { TrialService } from '../../trial/trial.service';
import { ReplayService } from '../../replay/replay.service';
import { HealthStatusService } from '../health-status/health-status.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { ReplayMessageCountMessage } from '../run-replay/replay-message-count-message';
import { ReplayCompletedMessage } from '../run-replay/replay-completed-message';
import { map, startWith } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { MatSelectChange } from '@angular/material/select';
import { MatOptionSelectionChange } from '@angular/material/core';
import { JsonDialogComponent } from '../json-dialog/json-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { DockerService } from '../../docker/docker.service';
import {ReplayObject} from './replayObject';

@Component({
  selector: 'app-batch-run-replay',
  templateUrl: './batch-run-replay.component.html',
  styleUrls: ['./batch-run-replay.component.scss']
})
export class BatchRunReplayComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;

  private isReplayCreatedSubscription: Subscription;
  public isReplayCreated = false;

  public isReplayRunning = false;

  private trialCreatedSubscription: Subscription;
  private replayCreatedSubscription: Subscription;

  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  private replayMessageCountSubscription: Subscription;
  private replayCompletedSubscription: Subscription;

  replays: Replay[] = [];
  trials: Trial[] = [];
  parents: Trial[] | Replay[] = [];
  replayParentTypes: string[] = ['TRIAL', 'REPLAY'];
  // filteredParents: Observable<Trial[] | Replay[]>;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  ignore_message_list: IgnoreListItem[] = [];
  ignore_source_list: string[] = [];
  ignore_topic_list: string[] = [];

  asiAgents: any = [];

  replayProgress = '';

  // replayParentIdControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  replayParentIdsControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  replayParentTypeControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  // overrideReplayParentIdToggleControl = this.formBuilder.control(false);
  // replayParentIdEnteredControl = this.formBuilder.control({value: '', disabled: true}, Validators.required);

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true });

  asiAgentNamesControl = this.formBuilder.control({value: '', disabled: false});

  isAbortClicked = false;
  isReplayAborted = false;

  ignoreMessageInputControl = this.formBuilder.control({ value: '', disabled: false });
  ignoreSourceInputControl = this.formBuilder.control({ value: '', disabled: false });
  ignoreTopicInputControl = this.formBuilder.control({ value: '', disabled: false });

  orderedParents: ReplayObject[] = [];

  restartAcAgentsControl = this.formBuilder.control({value: true, disabled: false}, Validators.required);

  runReplayForm = this.formBuilder.group({
    replayParentIds: this.replayParentIdsControl,
    replayParentType: this.replayParentTypeControl,
    // overrideReplayIdToggle: this.overrideReplayParentIdToggleControl,
    // replayParentIdEntered: this.replayParentIdEnteredControl,
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl,
    ignoreMessageInput: this.ignoreMessageInputControl,
    ignoreSourceInput: this.ignoreSourceInputControl,
    ignoreTopicInput: this.ignoreTopicInputControl,
    asiAgentNames: this.asiAgentNamesControl,
    restartAcAgents: this.restartAcAgentsControl
  });

  // quickToggle = new FormControl(false);

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  indexPattern: RegExp = new RegExp(/(?=[a-z0-9_\-])(?!.*[\s,:"*+\/\\|?#><]+)(?!_|-)/);
  ignoreMessagePattern: RegExp = new RegExp(/.+ : .+/);

  constructor(
    private formBuilder: FormBuilder,
    public elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private trialService: TrialService,
    private replayService: ReplayService,
    private healthStatusService: HealthStatusService,
    private mqttService: MqttService,
    private dockerService: DockerService,
    public jsonDialog: MatDialog,
  ) {
    this.replayMessageCountSubscription = this.mqttService.observe('metadata/replay/message/count').subscribe((message: IMqttMessage) => {
      if (!this.isReplayRunning) {
        this.isReplayRunning = true;
      }
      const json = new TextDecoder('utf-8').decode(message.payload);
      const replayMessageCountMessage = JSON.parse(json) as ReplayMessageCountMessage;
      // console.log(json);
      this.replayProgress = `${replayMessageCountMessage.current_message_count} sent out of ${replayMessageCountMessage.total_message_count} messages replayed`;
    });
    this.replayCompletedSubscription = this.mqttService.observe('metadata/replay/completed').subscribe((message: IMqttMessage) => {
      const json = new TextDecoder('utf-8').decode(message.payload);
      const replayCompletedMessage = JSON.parse(json) as ReplayCompletedMessage;
      // console.log(json);
      const delay = timer(1000);
      const subscribe = delay.subscribe(() => {
        this.isReplayRunning = false;
        this.replayProgress = '';
        this.log(`Batch Replay ${replayCompletedMessage.replay_id} completed: [${replayCompletedMessage.reason}] with ${replayCompletedMessage.total_messages_sent} out of ${replayCompletedMessage.total_message_count} processed.`);
      });
    });
  }

  ngOnInit(): void {
    this.isReplayCreatedSubscription = this.replayService.isReplayCreated.subscribe(isReplayCreated => {
      this.isReplayCreated = isReplayCreated;
    });
    this.overrideIndexNameToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.indexNameControl.reset();
        this.restartAcAgentsControl.reset(true);
        this.indexNameControl.disable();
        this.indexNameEnteredControl.enable();
        // this.clearReplayControls();
      } else {
        this.indexNameControl.enable();
        this.indexNameEnteredControl.reset();
        this.indexNameEnteredControl.disable();
        // this.clearReplayControls();
      }
    });
    forkJoin(
      {
        trials: this.trialService.readTrials(),
        replays: this.replayService.readReplays()
      }).subscribe(({trials, replays}) => {
      this.trials = trials;
      this.replays = replays;
      // this.filteredParents = this.replayParentIdsControl.valueChanges
      //   .pipe(
      //     startWith(''),
      //     map(parent => this._filterParentStates(parent))
      //   );
    });
    this.trialCreatedSubscription = this.mqttService.observe('metadata/trial/created').subscribe((message: IMqttMessage) => {
      this.readParents();
    });
    this.replayCreatedSubscription = this.mqttService.observe('metadata/replay/created').subscribe((message: IMqttMessage) => {
      this.readParents();
    });
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => {
      if (this.metadataAppOnline !== isOnline) {
        this.readParents();
      }
      this.metadataAppOnline = isOnline;
    });
    this.indexSubscription = this.elasticsearch.indices.subscribe(indices => {
      const selected = this.indexNameControl.value;
      this.indices = indices;
      this.filteredIndices = this.indexNameControl.valueChanges
        .pipe(
          startWith(''),
          map(index => index ? this._filterIndexStates(index) : this.indices.slice())
        );
      this.indexNameControl.setValue(selected);
    });
    this.dockerService.agentList().subscribe(acAgents => {
      this.asiAgents = acAgents;
    });
  }

  readParents(): void {
    forkJoin(
      {
        trials: this.trialService.readTrials(),
        replays: this.replayService.readReplays()
      }).subscribe(({trials, replays}) => {
      this.trials = trials;
      this.replays = replays;
      const selected = this.replayParentIdsControl.value;
      this.replayParentIdsControl.setValue(selected);
      // this.filteredParents = this.replayParentIdsControl.valueChanges
      //   .pipe(
      //     startWith(''),
      //     map(parent => this._filterParentStates(parent))
      //   );
    });
  }

  replayParentTypeChanged(event) {
    switch (event.value) {
      case 'TRIAL':
        this.parents = this.trials;
        break;
      case 'REPLAY':
        this.parents = this.replays;
        break;
      default:
        this.parents = [];
        break;
    }
    // const selected = this.replayParentIdControl.value;
    this.replayParentIdsControl.setValue('');
    this.asiAgentNamesControl.setValue('');
    // this.filteredParents = this.parents;
    this.orderedParents = [];
  }

  openJsonIgnoreMessageDialog(): void {
    const jsonDialogRef = this.jsonDialog.open(JsonDialogComponent, {
      // width: '250px',
      data: JSON.stringify(this.ignore_message_list, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const ignore_list = JSON.parse(result.json) as IgnoreListItem[];
          this.ignore_message_list = [];
          ignore_list.forEach(ignoreListItem  => {
            this.ignore_message_list.push(ignoreListItem);
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  openJsonIgnoreSourceDialog(): void {
    const jsonDialogRef = this.jsonDialog.open(JsonDialogComponent, {
      // width: '250px',
      data: JSON.stringify(this.ignore_source_list, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const ignore_list = JSON.parse(result.json) as string[];
          this.ignore_source_list = [];
          ignore_list.forEach(ignoreListItem  => {
            this.ignore_source_list.push(ignoreListItem);
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  openJsonIgnoreTopicDialog(): void {
    const jsonDialogRef = this.jsonDialog.open(JsonDialogComponent, {
      // width: '250px',
      data: JSON.stringify(this.ignore_topic_list, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const ignore_list = JSON.parse(result.json) as string[];
          this.ignore_topic_list = [];
          ignore_list.forEach(ignoreListItem  => {
            this.ignore_topic_list.push(ignoreListItem);
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isReplayCreatedSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.trialCreatedSubscription.unsubscribe();
    this.replayCreatedSubscription.unsubscribe();
    this.replayMessageCountSubscription.unsubscribe();
    this.replayCompletedSubscription.unsubscribe();
  }

  displayParentIdFn(parent: Trial | Replay): string {
    if (!parent) {
      return '';
    }
    if ((parent as Trial).name) {
      const t = parent as Trial;
      return t.name;
    } else {
      const r = parent as Replay;
      return r.replay_id;
    }
  }

  getDisplayName(parent: Trial | Replay): string {
    if ((parent as Trial).name) {
      const t = parent as Trial;
      return t.name;
    } else {
      const r = parent as Replay;
      return r.replay_id;
    }
  }

  updateIndexSelection(event): void {
    // this.clearReplayControls();
    const index = event.option.value;
    this.indexNameEnteredControl.enable();
    this.runReplayForm.patchValue({
      indexNameEnteredControl: index
    });
    this.indexNameEnteredControl.disable();
  }

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }

  onAbortClick() {
    this.replayService.abortReplay()
      .subscribe(result => {
        if (result === true) {
          this.isReplayAborted = true;
          this.isAbortClicked = true;
          this.log(`Currently running replay has been aborted.`);
        } else {
          this.isReplayAborted = false;
          this.isAbortClicked = true;
          this.log(`No running replays to abort.`);
        }
      });
    setTimeout (() => {
      this.isAbortClicked = false;
    }, 3000);
  }

  onRunClick(): void {
    this.isReplayRunning = true;
    const parent = this.replayParentIdsControl.value;
    // let parentUuids = [];
    const restart = this.restartAcAgentsControl.value;
    const replay_parent_type = this.replayParentTypeControl.value;
    const ignore_message_list = this.ignore_message_list;
    const ignore_source_list = this.ignore_source_list;
    const ignore_topic_list = this.ignore_topic_list;
    // No quick support yet for batch.
    // const quick = this.quickToggle.value;F
    const quick = false;
    const ordered_parents = this.orderedParents;
    let restart_agent_names = [];
    if (this.asiAgentNamesControl.value !== '') {
      restart_agent_names = this.asiAgentNamesControl.value;
    }
    // if (!this.overrideReplayParentIdToggleControl.value) {
    // replay_parent_id = this.replayParentIdsControl.value['msg.replay_id'];
    // if (replay_parent_type === 'TRIAL') {
    //   // const t = parent as Trial;
    //   parentUuids = this.orderedParents.map( (t) => t.trial_id );
    // } else if (replay_parent_type === 'REPLAY') {
    //   // const r = parent as Replay;
    //   parentUuids = this.orderedParents.map( (t) => t.replay_id );
    // }
    // } else {
    //   replay_parent_id = this.replayParentIdEnteredControl.value;
    // }

    let index = '';
    if (!this.overrideIndexNameToggleControl.value) {
      index = this.indexNameControl.value.index;
    } else {
      index = this.indexNameEnteredControl.value;
    }

    if (replay_parent_type === 'REPLAY') {
      this.replayService.runBatchReplay(ordered_parents, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index).subscribe(messageApiResult => {
        this.runReplayForm.reset();
        this.restartAcAgentsControl.reset(true);
        this.replayParentIdsControl.enable();
        // this.replayParentIdEnteredControl.disable();
        this.indexNameControl.enable();
        this.indexNameEnteredControl.disable();
        this.parents = [];
        this.ignore_message_list = [];
        this.ignore_source_list = [];
        this.ignore_topic_list = [];
        this.orderedParents = [];
        // this.quickToggle.reset();
        this.replayService.sendRunMessage(messageApiResult);
      });
    } else if (replay_parent_type === 'TRIAL') {
      this.replayService.runBatchTrial(ordered_parents, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index).subscribe(messageApiResult => {
        this.runReplayForm.reset();
        this.restartAcAgentsControl.reset(true);
        this.replayParentIdsControl.enable();
        // this.replayParentIdEnteredControl.disable();
        this.indexNameControl.enable();
        this.indexNameEnteredControl.disable();
        this.parents = [];
        this.ignore_message_list = [];
        this.ignore_source_list = [];
        this.ignore_topic_list = [];
        this.orderedParents = [];
        // this.quickToggle.reset();
        this.replayService.sendRunMessage(messageApiResult);
      });
    }
  }

  onAddIgnoreMessageItem(): void {
    if (this.ignoreMessageInputControl.value !== '') {
      const types = this.ignoreMessageInputControl.value.split(' : ');
      const ignoreListItem = {
        message_type: types[0],
        sub_type: types[1]
      };
      this.ignore_message_list.push(ignoreListItem);
      this.ignoreMessageInputControl.setValue('');
    }
  }

  onRemoveIgnoreMessageItem(item: any): void {
    const index: number = this.ignore_message_list.findIndex(i => i.message_type === item.message_type && i.sub_type === item.sub_type);
    if (index > -1) {
      this.ignore_message_list.splice(index, 1);
    }
  }

  onAddIgnoreSourceItem(): void {
    if (this.ignoreSourceInputControl.value !== '') {
      this.ignore_source_list.push(this.ignoreSourceInputControl.value);
      this.ignoreSourceInputControl.setValue('');
    }
  }

  onRemoveIgnoreSourceItem(item: any): void {
    const index: number = this.ignore_source_list.findIndex(i => i === item);
    if (index > -1) {
      this.ignore_source_list.splice(index, 1);
    }
  }

  onAddIgnoreTopicItem(): void {
    if (this.ignoreTopicInputControl.value !== '') {
      this.ignore_topic_list.push(this.ignoreTopicInputControl.value);
      this.ignoreTopicInputControl.setValue('');
    }
  }

  onRemoveIgnoreTopicItem(item: any): void {
    const index: number = this.ignore_topic_list.findIndex(i => i === item);
    if (index > -1) {
      this.ignore_topic_list.splice(index, 1);
    }
  }

  onBatchParentChange($event: MatOptionSelectionChange) {
    // console.log(`${$event.source.selected} ${$event.source.value.name}`);

    if (this.replayParentTypeControl.value === 'TRIAL') {
      if ($event.source.selected) {
        const index = this.orderedParents.findIndex(trial => {
          return trial.id === $event.source.value.trial_id;
        });
        if (index === -1) {
          this.orderedParents.push({
            id: $event.source.value.trial_id,
            type: this.replayParentTypeControl.value
          });
        }
      } else {
        const index = this.orderedParents.findIndex(trial => {
          return trial.id === $event.source.value.trial_id;
        });
        if (index !== -1) {
          this.orderedParents.splice(index, 1);
        }
      }
    } else if (this.replayParentTypeControl.value === 'REPLAY') {
      if ($event.source.selected) {
        const index = this.orderedParents.findIndex(replay => {
          return replay.id === $event.source.value.replay_id;
        });
        if (index === -1) {
          this.orderedParents.push({
            id: $event.source.value.replay_id,
            type: this.replayParentTypeControl.value
          });
        }
      } else {
        const index = this.orderedParents.findIndex(replay => {
          return replay.id === $event.source.value.replay_id;
        });
        if (index !== -1) {
          this.orderedParents.splice(index, 1);
        }
      }
    }
  }

  parentDrop(event: CdkDragDrop<any[]>) {
    moveItemInArray(this.orderedParents, event.previousIndex, event.currentIndex);
    // this.orderedTrials.forEach(trial => console.log(trial.trial_id));
    // console.log(JSON.stringify(this.orderedParents));
  }

  onAsiAgents($event: MatOptionSelectionChange) {
    if ($event.source.selected) {
      const index = this.orderedParents.findIndex(agent => {
        return agent.id === $event.source.value;
      });
      if (index === -1) {
        // console.log($event.source.value);
        this.orderedParents.push({
          id: $event.source.value,
          type: 'ASI'
        });
      }
    } else {
      const index = this.orderedParents.findIndex(agent => {
        return agent.id === $event.source.value;
      });
      if (index !== -1) {
        this.orderedParents.splice(index, 1);
      }
    }
  }

  isBatchOrderValid(): boolean {
    return this.orderedParents.every((element, index, array) => {
      if (element.type === 'ASI') {
        if (index + 1 < array.length) {
          if (array[index + 1].type === 'TRIAL' || array[index + 1].type === 'REPLAY') {
            return true;
          } else {
            return false;
          }
        } else {
          return false;
        }
      } else {
        return true;
      }
    });
  }

  private _filterIndexStates(value: any): any[] {
    if (value.index) {
      const filterValue = value.index.toLowerCase();
      return this.indices.filter(option => option.index.toString().toLowerCase().includes(filterValue));
    } else {
      const filterValue = value.toLowerCase();
      return this.indices.filter(option => option.index.toString().toLowerCase().includes(filterValue));
    }
  }

  private log(message: string) {
    this.loggingService.add(`RunReplayComponent: ${message}`);
  }
}

