import { Component, OnDestroy, OnInit } from '@angular/core';
import {forkJoin, Observable, Subscription, timer} from 'rxjs';
import {FormBuilder, FormControl, PatternValidator, Validators} from '@angular/forms';
import { ElasticsearchService } from '../elasticsearch';
import { LoggingService } from '../../logging/logging.service';
import { map, startWith } from 'rxjs/operators';
import { Trial } from '../../trial/trial';
import { Replay } from '../../replay/replay';
import { TrialService } from '../../trial/trial.service';
import { ReplayService } from '../../replay/replay.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { HealthStatusService } from '../health-status/health-status.service';
import { environment } from '../../../environments/environment';
import { ReplayMessageCountMessage } from './replay-message-count-message';
import { ReplayCompletedMessage } from './replay-completed-message';
import { IgnoreListItem } from '../../replay/ignore-list-item';
import { JsonDialogComponent } from '../json-dialog/json-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-run-replay',
  templateUrl: './run-replay.component.html',
  styleUrls: ['./run-replay.component.scss']
})
export class RunReplayComponent implements OnInit, OnDestroy {
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
  filteredParents: Observable<Trial[] | Replay[]>;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  ignore_message_list: IgnoreListItem[] = [];
  ignore_source_list: string[] = [];
  ignore_topic_list: string[] = [];

  replayProgress = '';

  replayParentIdControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  replayParentTypeControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  overrideReplayParentIdToggleControl = this.formBuilder.control(false);
  replayParentIdEnteredControl = this.formBuilder.control({value: '', disabled: true}, Validators.required);
  ignoreListControl = this.formBuilder.control('');

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true });

  isAbortClicked = false;
  isReplayAborted = false;

  ignoreMessageInputControl = this.formBuilder.control({ value: '', disabled: false });
  ignoreSourceInputControl = this.formBuilder.control({ value: '', disabled: false });
  ignoreTopicInputControl = this.formBuilder.control({ value: '', disabled: false });

  runReplayForm = this.formBuilder.group({
    replayParentId: this.replayParentIdControl,
    replayParentType: this.replayParentTypeControl,
    overrideReplayIdToggle: this.overrideReplayParentIdToggleControl,
    replayParentIdEntered: this.replayParentIdEnteredControl,
    ignoreList: this.ignoreListControl,
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl,
    ignoreMessageInput: this.ignoreMessageInputControl,
    ignoreSourceInput: this.ignoreSourceInputControl,
    ignoreTopicInput: this.ignoreTopicInputControl
  });

  quickToggle = new FormControl(false);

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
        this.log(`Replay ${replayCompletedMessage.replay_id} completed: [${replayCompletedMessage.reason}] with ${replayCompletedMessage.total_messages_sent} out of ${replayCompletedMessage.total_message_count} processed.`);
      });
    });
  }

  ngOnInit(): void {
    this.isReplayCreatedSubscription = this.replayService.isReplayCreated.subscribe(isReplayCreated => {
      this.isReplayCreated = isReplayCreated;
    });
    this.overrideReplayParentIdToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.replayParentIdControl.reset();
        this.replayParentIdControl.disable();
        // this.replayParentTypeControl.disable();
        // this.replayParentTypeControl.reset();
        this.replayParentIdEnteredControl.enable();
      } else {
        this.replayParentIdControl.enable();
        this.replayParentIdControl.reset();
        // this.replayParentTypeControl.enable();
        // this.replayParentTypeControl.reset();
        this.replayParentIdEnteredControl.reset();
        this.replayParentIdEnteredControl.disable();
      }
    });
    this.overrideIndexNameToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.indexNameControl.reset();
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
      this.filteredParents = this.replayParentIdControl.valueChanges
        .pipe(
          startWith(''),
          map(parent => this._filterParentStates(parent))
        );
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
  }

  readParents(): void {
    forkJoin(
      {
        trials: this.trialService.readTrials(),
        replays: this.replayService.readReplays()
      }).subscribe(({trials, replays}) => {
      this.trials = trials;
      this.replays = replays;
      const selected = this.replayParentIdControl.value;
      this.replayParentIdControl.setValue(selected);
      this.filteredParents = this.replayParentIdControl.valueChanges
        .pipe(
          startWith(''),
          map(parent => this._filterParentStates(parent))
        );
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
    this.replayParentIdControl.setValue('');
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

  public onAbortClick() {
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
    const parent = this.replayParentIdControl.value;
    let replay_parent_id = '';
    const replay_parent_type = this.replayParentTypeControl.value;
    const ignore_message_list = this.ignore_message_list;
    const ignore_source_list = this.ignore_source_list;
    const ignore_topic_list = this.ignore_topic_list;

    if (!this.overrideReplayParentIdToggleControl.value) {
      replay_parent_id = this.replayParentIdControl.value['msg.replay_id'];
      if (replay_parent_type === 'TRIAL') {
        const t = parent as Trial;
        replay_parent_id = t.trial_id;
      } else if (replay_parent_type === 'REPLAY') {
        const r = parent as Replay;
        replay_parent_id = r.replay_id;
      }
    } else {
      replay_parent_id = this.replayParentIdEnteredControl.value;
    }

    let index = '';
    if (!this.overrideIndexNameToggleControl.value) {
      index = this.indexNameControl.value.index;
    } else {
      index = this.indexNameEnteredControl.value;
    }

    if (replay_parent_type === 'REPLAY') {
      if (this.quickToggle.value) {
        this.runReplayForm.reset();
        this.replayParentIdControl.enable();
        this.replayParentIdEnteredControl.disable();
        this.indexNameControl.enable();
        this.indexNameEnteredControl.disable();
        this.parents = [];
        this.quickToggle.reset();
        this.replayService.runQuickReplay(replay_parent_id, ignore_message_list, ignore_source_list, ignore_topic_list, index).subscribe(messageApiResult => {
          this.replayService.sendRunMessage(messageApiResult);
        });
      } else {
        this.replayService.getReplayRootTrial(replay_parent_id).subscribe(trial => {
          const replayRunMessage = this.replayService.generateReplayMessage(trial.trial_id, trial.experiment.experiment_id, replay_parent_id, replay_parent_type, ignore_message_list, ignore_source_list, ignore_topic_list, 'run', 'metadata-gui', environment.testbedVersion);
          this.runReplayForm.reset();
          this.replayParentIdControl.enable();
          this.replayParentIdEnteredControl.disable();
          this.indexNameControl.enable();
          this.indexNameEnteredControl.disable();
          this.parents = [];
          this.replayService.runReplay(replayRunMessage, index).subscribe(replay => {
            this.replayService.sendRunMessage(replay);
          });
        });
      }
    } else if (replay_parent_type === 'TRIAL') {
      if (this.quickToggle.value) {
        this.runReplayForm.reset();
        this.replayParentIdControl.enable();
        this.replayParentIdEnteredControl.disable();
        this.indexNameControl.enable();
        this.indexNameEnteredControl.disable();
        this.parents = [];
        this.quickToggle.reset();
        this.replayService.runQuickTrial(replay_parent_id, ignore_message_list, ignore_source_list, ignore_topic_list, index).subscribe(messageApiResult => {
          this.replayService.sendRunMessage(messageApiResult);
        });
      } else {
        this.trialService.readTrialUUID(replay_parent_id).subscribe(trial => {
          const replayRunMessage = this.replayService.generateReplayMessage(trial.trial_id, trial.experiment.experiment_id, replay_parent_id, replay_parent_type, ignore_message_list, ignore_source_list, ignore_topic_list, 'run', 'metadata-gui', environment.testbedVersion);
          this.runReplayForm.reset();
          this.replayParentIdControl.enable();
          this.replayParentIdEnteredControl.disable();
          this.indexNameControl.enable();
          this.indexNameEnteredControl.disable();
          this.parents = [];
          this.replayService.runReplay(replayRunMessage, index).subscribe(replay => {
            this.replayService.sendRunMessage(replay);
          });
        });
      }
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

  private _filterParentStates(value: any): any[] {
    const filteredList: any[] = [];
    if (value === null) {
      return filteredList;
    }
    let filterValue = '';
    if (value.name) {
      filterValue = value.name.toLowerCase();
    } else if (value.replay_id) {
      filterValue = value.replay_id.toLowerCase();
    } else {
      filterValue = value.toLowerCase();
    }
    this.parents.forEach(parent => {
      if ((parent as Trial).name) {
        const t = parent as Trial;
        if (t.name.toString().toLowerCase().includes(filterValue)) {
          filteredList.push(t);
        }
      } else {
        const r = parent as Replay;
        if (r.replay_id.toString().toLowerCase().includes(filterValue)) {
          filteredList.push(r);
        }
      }
    });
    return filteredList;
    // return this.parents.filter(parent => replay['msg.replay_id'].toLowerCase().indexOf(filterValue) === 0);
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
