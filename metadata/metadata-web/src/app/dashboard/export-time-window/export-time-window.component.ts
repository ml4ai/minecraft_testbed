import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
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
import { TrialService } from '../../trial/trial.service';
// import moment from 'moment';
import moment from 'moment-timezone';

@Component({
  selector: 'app-export-time-window',
  templateUrl: './export-time-window.component.html',
  styleUrls: ['./export-time-window.component.scss']
})
export class ExportTimeWindowComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;

  private isExportingTrialSubscription: Subscription;
  public isExportingTrial = false;

  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  // trialIdControl = this.formBuilder.control( { value: '', disabled: false }, Validators.required);
  // overrideTrialIdToggleControl = this.formBuilder.control(false);
  // trialIdEnteredControl = this.formBuilder.control({ value: '', disabled: true }, Validators.required);
  beginDateTimeControl = this.formBuilder.control( { value: '', disabled: false }, Validators.required);
  endDateTimeControl = this.formBuilder.control( { value: '', disabled: false }, Validators.required);

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({ value: '', disabled: true }, Validators.required);

  exportTrialForm = this.formBuilder.group({
    // trialId: this.trialIdControl,
    // overrideTrialIdToggle: this.overrideTrialIdToggleControl,
    // trialIdEntered: this.trialIdEnteredControl,
    beginDateTime: this.beginDateTimeControl,
    endDateTime: this.endDateTimeControl,
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl
  });

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  indexPattern: RegExp = new RegExp(/^(?=[a-z0-9_\-])(?!.*[\s,:"*+\/\\|?#><]+)(?!_|-)/);

  constructor(
    private formBuilder: FormBuilder,
    private trialService: TrialService,
    public elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private healthStatusService: HealthStatusService,
    private mqttService: MqttService
  ) { }

  ngOnInit(): void {
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

    this.isExportingTrialSubscription = this.elasticsearch.isExportingTrial.subscribe(isExportingTrial => this.isExportingTrial = isExportingTrial);
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => {
      // if (this.metadataAppOnline !== isOnline) {
      //   this.readTrials();
      // }
      this.metadataAppOnline = isOnline;
    });

    this.overrideIndexNameToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.indexNameControl.reset();
        this.indexNameControl.disable();
        this.indexNameEnteredControl.enable();
      } else {
        this.indexNameControl.enable();
        this.indexNameEnteredControl.reset();
        this.indexNameEnteredControl.disable();
      }
    });
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isExportingTrialSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
  }

  displayTrialIdFn(trial: Trial): string {
    return trial && trial.name ? trial.name : '';
  }

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }

  updateIndexSelection(event): void {
    const index = event.option.value;
    this.indexNameEnteredControl.enable();
    this.exportTrialForm.patchValue({
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
    let selectedIndexName = '';
    const beginDateTime = moment(this.beginDateTimeControl.value, `MM/DD/YYYY HH/mm/ss ${moment.tz.guess()}`);
    const endDateTime = moment(this.endDateTimeControl.value, `MM/DD/YYYY HH/mm/ss ${moment.tz.guess()}`);
    // this.log(`beginDateTime: ${beginDateTime} endDateTime: ${endDateTime}`);
    // this.log(`beginDateTime: ${this.beginDateTimeControl.value} endDateTime: ${this.endDateTimeControl.value}`);
    if (!this.overrideIndexNameToggleControl.value) {
      selectedIndexName = this.indexNameControl.value.index;
    } else {
      selectedIndexName = this.indexNameEnteredControl.value;
    }
    const filename = `Begin ${beginDateTime.format('MM-DD-YYYY_HH-mm-ss')} End ${endDateTime.format('MM-DD-YYYY_HH-mm-ss')} Index ${selectedIndexName}`;
    this.exportTrialForm.reset();
    this.indexNameControl.enable();
    this.indexNameEnteredControl.disable();
    // this.trialIdControl.enable();
    // this.trialIdEnteredControl.disable();
    const exportMessage = this.elasticsearch.generateExportTimeWindowMessage(beginDateTime.toISOString(), endDateTime.toISOString(), selectedIndexName, 'time_window', 'metadata-web', environment.testbedVersion);
    // this.log(`exportMessage: ${JSON.stringify(exportMessage)}`);
    this.elasticsearch.exportTimeWindow(beginDateTime.toISOString(), endDateTime.toISOString(), selectedIndexName, filename).then(() => {
      this.elasticsearch.sendExportMessage(exportMessage);
    }).catch(error => this.log('Export error: ' + error)); // .finally(() => this.exportTrialForm.reset());
  }

  private log(message: string) {
    this.loggingService.add(`ExportTrialComponent: ${message}`);
  }
}
