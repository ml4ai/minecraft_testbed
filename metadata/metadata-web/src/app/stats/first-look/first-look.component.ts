import { Component, OnDestroy, OnInit } from '@angular/core';
import { forkJoin, Observable, Subscription} from 'rxjs';
import { Replay } from '../../replay/replay';
import { Trial } from '../../trial/trial';
import { FormBuilder, Validators } from '@angular/forms';
import { ElasticsearchService } from '../../dashboard/elasticsearch';
import { LoggingService } from '../../logging/logging.service';
import { TrialService } from '../../trial/trial.service';
import { ReplayService } from '../../replay/replay.service';
import { HealthStatusService } from '../../dashboard/health-status/health-status.service';
import { MqttService } from 'ngx-mqtt';
import { map, startWith } from 'rxjs/operators';
import firstLookDataJson from './first-look-data.json';
import { FirstLook } from './first-look';
import { FirstLookReport } from './first-look-report';

@Component({
  selector: 'app-first-look',
  templateUrl: './first-look.component.html',
  styleUrls: ['./first-look.component.scss']
})
export class FirstLookComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;

  private isReplayCreatedSubscription: Subscription;
  public isFirstLookRunning = false;

  private trialCreatedSubscription: Subscription;
  private replayCreatedSubscription: Subscription;

  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  public areResultsReady = false;

  public firstLookReport: FirstLookReport = null;

  replays: Replay[] = [];
  trials: Trial[] = [];
  parents: Trial[] | Replay[] = [];
  firstLookTypes: string[] = ['TRIAL', 'REPLAY'];
  filteredFirstLooks: Observable<Trial[] | Replay[]>;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  // replayProgress = '';

  firstLookData: FirstLook[] = [];
  firstLookTests: any[] = [];

  firstLookIdControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  firstLookTypeControl = this.formBuilder.control({value: '', disabled: false}, Validators.required);
  overrideFirstLookIdToggleControl = this.formBuilder.control(false);
  firstLookIdEnteredControl = this.formBuilder.control({value: '', disabled: true}, Validators.required);

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true });

  runFirstLookForm = this.formBuilder.group({
    firstLookId: this.firstLookIdControl,
    firstLookType: this.firstLookTypeControl,
    overrideFirstLookIdToggle: this.overrideFirstLookIdToggleControl,
    firstLookIdEntered: this.firstLookIdEnteredControl,
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl,
  });

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  indexPattern: RegExp = new RegExp(/(?=[a-z0-9_\-])(?!.*[\s,:"*+\/\\|?#><]+)(?!_|-)/);
  // firstLookId: string;
  // firstLookIndexName: string;

  constructor(
    private formBuilder: FormBuilder,
    public elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private trialService: TrialService,
    private replayService: ReplayService,
    private healthStatusService: HealthStatusService,
    private mqttService: MqttService,
  ) { }

  ngOnInit(): void {
    this.firstLookData = firstLookDataJson as FirstLook[];
    // this.firstLookId = '';
    // this.firstLookIndexName = '';
    this.firstLookTests = [];
    this.isReplayCreatedSubscription = this.replayService.isReplayCreated.subscribe(isReplayCreated => {
      this.isFirstLookRunning = isReplayCreated;
    });
    this.overrideFirstLookIdToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.firstLookIdControl.reset();
        this.firstLookIdControl.disable();
        // this.replayParentTypeControl.disable();
        // this.replayParentTypeControl.reset();
        this.firstLookIdEnteredControl.enable();
      } else {
        this.firstLookIdControl.enable();
        this.firstLookIdControl.reset();
        // this.replayParentTypeControl.enable();
        // this.replayParentTypeControl.reset();
        this.firstLookIdEnteredControl.reset();
        this.firstLookIdEnteredControl.disable();
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
      this.filteredFirstLooks = this.firstLookIdControl.valueChanges
        .pipe(
          startWith(''),
          map(parent => this._filterParentStates(parent))
        );
    });
    this.trialCreatedSubscription = this.mqttService.observe('metadata/trial/created').subscribe(() => {
      this.readParents();
    });
    this.replayCreatedSubscription = this.mqttService.observe('metadata/replay/created').subscribe(() => {
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
      const selected = this.firstLookIdControl.value;
      this.firstLookIdControl.setValue(selected);
      this.filteredFirstLooks = this.firstLookIdControl.valueChanges
        .pipe(
          startWith(''),
          map(parent => this._filterParentStates(parent))
        );
    });
  }

  firstLookTypeChanged(event) {
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
    this.firstLookIdControl.setValue('');
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isReplayCreatedSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.trialCreatedSubscription.unsubscribe();
    this.replayCreatedSubscription.unsubscribe();
  }

  displayFirstLookIdFn(parent: Trial | Replay): string {
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
    this.runFirstLookForm.patchValue({
      indexNameEnteredControl: index
    });
    this.indexNameEnteredControl.disable();
  }

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }

  onClearClick() {
    this.runFirstLookForm.reset();
    this.firstLookIdControl.enable();
    this.firstLookIdEnteredControl.disable();
    this.indexNameControl.enable();
    this.indexNameEnteredControl.disable();
    this.parents = [];
    // this.firstLookId = '';
    this.firstLookData = [];
    this.firstLookTests = [];
    this.isFirstLookRunning = false;
    this.areResultsReady = false;
    this.firstLookReport = null;
  }

  onRunClick(): void {
    this.isFirstLookRunning = true;
    const parent = this.firstLookIdControl.value;
    const firstLookType = this.firstLookTypeControl.value;
    let firstLookId = '';
    let firstLookIndexName = '';
    if (!this.overrideFirstLookIdToggleControl.value) {
      firstLookId = this.firstLookIdControl.value['msg.replay_id'];
      if (firstLookType === 'TRIAL') {
        const t = parent as Trial;
        firstLookId = t.trial_id;
      } else if (firstLookType === 'REPLAY') {
        const r = parent as Replay;
        firstLookId = r.replay_id;
      }
    } else {
      firstLookId = this.firstLookIdEnteredControl.value;
    }

    if (!this.overrideIndexNameToggleControl.value) {
      firstLookIndexName = this.indexNameControl.value.index;
    } else {
      firstLookIndexName = this.indexNameEnteredControl.value;
    }

    // filename = `TrialMessages_CondBtwn-${this.trialIdControl.value.condition}_CondWin-${this.trialIdControl.value.experiment.mission}-StaticMap_Trial-${this.trialIdControl.value.trial_number}_Team-na_Member-${this.trialIdControl.value.subjects.join('-')}_Vers-${this.trialIdControl.value.testbed_version}`;
    this.firstLookReport = {id: '', index: '', is_replay: false, results: [], total_documents: 0, trial: undefined};
    if (firstLookType === 'REPLAY') {
      this.replayService.getReplayRootTrial(firstLookId).subscribe(trial => {
        this.firstLookReport.trial = trial;
        this.firstLookReport.is_replay = true;
        this.firstLookReport.id = firstLookId;
        this.firstLookReport.index = firstLookIndexName;
        this.elasticsearch.getDocumentCount(firstLookIndexName, firstLookType, firstLookId).then(documentCountResult => {
          this.firstLookReport.total_documents = documentCountResult.count;
          const tests = this.firstLookData.map((element, index) => {
            return this.elasticsearch.getMessageCount(firstLookIndexName, firstLookType, firstLookId, element.message_type, element.sub_type).then(messageCountResult => {
              this.firstLookTests[index] = {
                valid: this.isFirstLookItemValid(element, messageCountResult.count)
              };
              this.firstLookReport.results.push({
                message_type: element.message_type,
                sub_type: element.sub_type,
                comparison: element.comparison,
                result: this.firstLookTests[index].valid,
                count: messageCountResult.count
              });
            });
          });
          Promise.all(tests).then(() => {
            console.log(JSON.stringify(this.firstLookReport));
            this.isFirstLookRunning = false;
            this.areResultsReady = true;
          });
        });
      });
    } else if (firstLookType === 'TRIAL') {
      this.trialService.readTrialUUID(firstLookId).subscribe(trial => {
        this.firstLookReport.trial = trial;
        this.firstLookReport.is_replay = false;
        this.firstLookReport.id = firstLookId;
        this.firstLookReport.index = firstLookIndexName;
        this.elasticsearch.getDocumentCount(firstLookIndexName, firstLookType, firstLookId).then(documentCountResult => {
          this.firstLookReport.total_documents = documentCountResult.count;
          const tests = this.firstLookData.map((element, index) => {
            return this.elasticsearch.getMessageCount(firstLookIndexName, firstLookType, firstLookId, element.message_type, element.sub_type).then(messageCountResult => {
              this.firstLookTests[index] = {
                valid: this.isFirstLookItemValid(element, messageCountResult.count)
              };
              this.firstLookReport.results.push({
                message_type: element.message_type,
                sub_type: element.sub_type,
                comparison: element.comparison,
                result: this.firstLookTests[index].valid,
                count: messageCountResult.count
              });
            });
          });
          Promise.all(tests).then(() => {
            console.log(JSON.stringify(this.firstLookReport));
            this.isFirstLookRunning = false;
            this.areResultsReady = true;
          });
        });
      });
    }
  }

  generateReport() {
    if (this.areResultsReady) {
      const dataString = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.firstLookReport));
      const downloadLink = document.createElement('a');
      downloadLink.setAttribute('href', dataString);
      downloadLink.setAttribute('download', 'firstlook.json');
      document.body.appendChild(downloadLink);
      downloadLink.click();
      downloadLink.remove();
    }

    // var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    // var downloadAnchorNode = document.createElement('a');
    // downloadAnchorNode.setAttribute("href",     dataStr);
    // downloadAnchorNode.setAttribute("download", exportName + ".json");
    // document.body.appendChild(downloadAnchorNode); // required for firefox
    // downloadAnchorNode.click();
    // downloadAnchorNode.remove();
  }

  private isFirstLookItemValid(firstLook: FirstLook, count: number): boolean {
    switch (firstLook.comparison.operator) {
      case '>=':
        return firstLook.comparison.value >= count;
      case '==':
        return firstLook.comparison.value === count;
      default:
        return false;
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
