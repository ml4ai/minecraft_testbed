import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { Observable, Subscription } from 'rxjs';
import { ElasticsearchService } from '../elasticsearch';
import { LoggingService } from '../../logging/logging.service';
import { ReplayService } from '../../replay/replay.service';
import { Replay } from '../../replay/replay';
import { HealthStatusService } from '../health-status/health-status.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { Trial } from '../../trial/trial';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-export-replay',
  templateUrl: './export-replay.component.html',
  styleUrls: ['./export-replay.component.scss']
})
export class ExportReplayComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;

  private isExportingReplaySubscription: Subscription;
  public isExportingReplay = false;

  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  private replayCreatedSubscription: Subscription;

  replays: Replay[] = [];
  filteredReplays: Observable<Replay[]>;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  replayIdControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideReplayIdToggleControl = this.formBuilder.control(false);
  replayIdEnteredControl = this.formBuilder.control({ value: '', disabled: true }, Validators.required);

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true });

  exportReplayForm = this.formBuilder.group({
    replayId: this.replayIdControl,
    overrideReplayIdToggle: this.overrideReplayIdToggleControl,
    replayIdEntered: this.replayIdEnteredControl,
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl
  });

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  indexPattern: RegExp = new RegExp(/^(?=[a-z0-9_\-])(?!.*[\s,:"*+\/\\|?#><]+)(?!_|-)/);

  constructor(
    private formBuilder: FormBuilder,
    public elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private replayService: ReplayService,
    private healthStatusService: HealthStatusService,
    private mqttService: MqttService
  ) { }

  ngOnInit(): void {
    this.replayService.readReplays()
      .subscribe(replays => {
        this.replays = replays;
        this.filteredReplays = this.replayIdControl.valueChanges
          .pipe(
            startWith(''),
            map(replay => replay ? this._filterReplayStates(replay) : this.replays.slice())
          );
      });
    this.filteredIndices = this.indexNameControl.valueChanges
      .pipe(
        startWith(''),
        map(index => index ? this._filterIndexStates(index) : this.indices.slice())
      );
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

    this.replayCreatedSubscription = this.mqttService.observe('metadata/replay/created').subscribe((message: IMqttMessage) => {
      this.readReplays();
    });

    this.isExportingReplaySubscription = this.elasticsearch.isExportingReplay.subscribe(isExportingReplay => this.isExportingReplay = isExportingReplay);
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => {
      if (this.metadataAppOnline !== isOnline) {
        this.readReplays();
      }
      this.metadataAppOnline = isOnline;
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

    this.overrideReplayIdToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.replayIdControl.reset();
        this.replayIdControl.disable();
        this.replayIdEnteredControl.enable();
      } else {
        this.replayIdControl.enable();
        this.replayIdEnteredControl.reset();
        this.replayIdEnteredControl.disable();
      }
    });
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isExportingReplaySubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.replayCreatedSubscription.unsubscribe();
  }

  readReplays(): void {
    this.replayService.readReplays()
      .subscribe(replays => {
        this.replays = replays;
        const selected = this.replayIdControl.value;
        this.replayIdControl.setValue(selected);
      });
  }

  searchReplays(event): void {
    const index = this.overrideIndexNameToggleControl.value ? this.indexNameEnteredControl.value : this.indexNameControl.value.index;
    if (!index) {
      return;
    }
    this.elasticsearch.getReplays(index).then(results => { this.replays = results; this.log('Replays: ' + results.length + ' found.'); }).catch(error => this.log('GetReplays error: ' + error));
    event.stopPropagation();
  }

  displayReplayIdFn(replay: Replay): string {
    return replay && replay.replay_id ? replay.replay_id : '';
  }

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }
  updateReplaySelection(event): void {
    const replay = event.option.value;
    this.replayIdEnteredControl.enable();
    this.exportReplayForm.patchValue({
      replayIdEnteredControl: replay.replay_id
    });
    this.replayIdEnteredControl.disable();
  }

  // clearReplayControls(): void {
  //   this.replayIdControl.reset('', {
  //     onlySelf: true
  //   });
  //
  //   this.replayIdEnteredControl.reset('', {
  //     onlySelf: true
  //   });
  //
  //   this.replays = [];
  // }

  private _filterReplayStates(value: any): Replay[] {
      if (value.replay_id) {
        const filterValue = value.replay_id.toLowerCase();
        return this.replays.filter(option => option.replay_id.toString().toLowerCase().includes(filterValue));
      } else {
        const filterValue = value.toLowerCase();
        return this.replays.filter(option => option.replay_id.toString().toLowerCase().includes(filterValue));
      }
    }

  updateIndexSelection(event): void {
    // this.clearReplayControls();
    const index = event.option.value;
    this.indexNameEnteredControl.enable();
    this.exportReplayForm.patchValue({
      indexNameEnteredControl: index
    });
    this.indexNameEnteredControl.disable();
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

  onExportClick(): void {
    let selectedReplayId = '';
    let selectedIndexName = '';
    let filename = '';
    if (!this.overrideReplayIdToggleControl.value) {
      selectedReplayId = this.replayIdControl.value.replay_id;
      filename = this.replayIdControl.value.replay_id;
    } else {
      selectedReplayId = this.replayIdEnteredControl.value;
      filename = this.replayIdEnteredControl.value;
    }
    if (!this.overrideIndexNameToggleControl.value) {
      selectedIndexName = this.indexNameControl.value.index;
    } else {
      selectedIndexName = this.indexNameEnteredControl.value;
    }
    const replay = this.replayIdControl.value as Replay;
    this.exportReplayForm.reset();
    this.indexNameControl.enable();
    this.indexNameEnteredControl.disable();
    this.replayIdControl.enable();
    this.replayIdEnteredControl.disable();
    this.replayService.getReplayParents(selectedReplayId).subscribe(parents => {
      const exportMessage = this.replayService.generateExportMessage(replay, parents, selectedIndexName, 'replay', 'metadata-web', environment.testbedVersion);
      this.elasticsearch.exportReplay(selectedIndexName, selectedReplayId, filename, exportMessage).then(() => {
        this.replayService.sendExportMessage(exportMessage);
      }).catch(error => this.log('Export error: ' + error)); // .finally(() => this.exportTrialForm.reset());
    });
    // this.elasticsearch.exportReplay(selectedIndexName, selectedReplayId, filename).catch(error => this.log('Export error: ' + error)); // .finally(() => this.exportReplayForm.reset());
  }

  private log(message: string) {
    this.loggingService.add(`ExportReplayComponent: ${message}`);
  }
}
