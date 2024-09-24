import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Trial } from '../../trial/trial';
import { TrialService } from '../../trial/trial.service';
import { map, startWith, tap } from 'rxjs/operators';
import { Observable, Subscription } from 'rxjs';
import { ElasticsearchService } from '../elasticsearch';
import { LoggingService } from '../../logging/logging.service';
import { HealthStatusService } from '../health-status/health-status.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-export-trial',
  templateUrl: './export-trial.component.html',
  styleUrls: ['./export-trial.component.scss']
})
export class ExportTrialComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;

  private isExportingTrialSubscription: Subscription;
  public isExportingTrial = false;

  private metadataAppOnlineSubscription: Subscription;
  public metadataAppOnline = false;

  private trialCreatedSubscription: Subscription;

  trials: Trial[] = [];
  filteredTrials: Observable<Trial[]>;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  trialIdControl = this.formBuilder.control( { value: '', disabled: false }, Validators.required);
  overrideTrialIdToggleControl = this.formBuilder.control(false);
  trialIdEnteredControl = this.formBuilder.control({ value: '', disabled: true }, Validators.required);

  indexNameControl = this.formBuilder.control({ value: '', disabled: false }, Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({ value: '', disabled: true }, Validators.required);

  exportTrialForm = this.formBuilder.group({
    trialId: this.trialIdControl,
    overrideTrialIdToggle: this.overrideTrialIdToggleControl,
    trialIdEntered: this.trialIdEnteredControl,
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
    this.trialService.readTrials()
      .subscribe(trials => {
        this.trials = trials;
        this.filteredTrials = this.trialIdControl.valueChanges
          .pipe(
            startWith(''),
            map(trial => trial ? this._filterTrialStates(trial) : this.trials.slice())
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

    this.trialCreatedSubscription = this.mqttService.observe('metadata/trial/created').subscribe((message: IMqttMessage) => {
      this.readTrials();
    });

    this.isExportingTrialSubscription = this.elasticsearch.isExportingTrial.subscribe(isExportingTrial => this.isExportingTrial = isExportingTrial);
    this.metadataAppOnlineSubscription = this.healthStatusService.isMetadataAppOnline.subscribe(isOnline => {
      if (this.metadataAppOnline !== isOnline) {
        this.readTrials();
      }
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

    this.overrideTrialIdToggleControl.valueChanges.subscribe((checked) => {
      if (checked) {
        this.trialIdControl.reset();
        this.trialIdControl.disable();
        this.trialIdEnteredControl.enable();
      } else {
        this.trialIdControl.enable();
        this.trialIdEnteredControl.reset();
        this.trialIdEnteredControl.disable();
      }
    });
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isExportingTrialSubscription.unsubscribe();
    this.metadataAppOnlineSubscription.unsubscribe();
    this.trialCreatedSubscription.unsubscribe();
  }

  readTrials(): void {
    this.trialService.readTrials()
      .subscribe(trials => {
        this.trials = trials;
        const selected = this.trialIdControl.value;
        this.trialIdControl.setValue(selected);
      });
  }

  displayTrialIdFn(trial: Trial): string {
    return trial && trial.name ? trial.name : '';
  }

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }

  updateTrialSelection(event): void {
    const trial = event.option.value;
    this.trialIdEnteredControl.enable();
    this.exportTrialForm.patchValue({
      trialIdEnteredControl: trial.trial_id
    });
    this.trialIdEnteredControl.disable();
  }

  private _filterTrialStates(value: any): Trial[] {
    if (value.name) {
      const filterValue = value.name.toLowerCase();
      return this.trials.filter(option => option.name.toString().toLowerCase().includes(filterValue));
    } else {
      const filterValue = value.toLowerCase();
      return this.trials.filter(option => option.name.toString().toLowerCase().includes(filterValue));
    }
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
    let selectedTrialId = '';
    let selectedIndexName = '';
    let filename = '';
    if (!this.overrideTrialIdToggleControl.value) {
      selectedTrialId = this.trialIdControl.value.trial_id;
      filename = `TrialMessages_CondBtwn-${this.trialIdControl.value.condition}_CondWin-${this.trialIdControl.value.experiment.mission}-StaticMap_Trial-${this.trialIdControl.value.trial_number}_Team-na_Member-${this.trialIdControl.value.subjects.join('-')}_Vers-${this.trialIdControl.value.testbed_version}`;

    } else {
      selectedTrialId = this.trialIdEnteredControl.value;
      filename = this.trialIdEnteredControl.value;
    }
    if (!this.overrideIndexNameToggleControl.value) {
      selectedIndexName = this.indexNameControl.value.index;
    } else {
      selectedIndexName = this.indexNameEnteredControl.value;
    }
    const trial = this.trialIdControl.value as Trial;
    this.exportTrialForm.reset();
    this.indexNameControl.enable();
    this.indexNameEnteredControl.disable();
    this.trialIdControl.enable();
    this.trialIdEnteredControl.disable();
    const exportMessage = this.trialService.generateExportMessage(trial, selectedIndexName, 'trial', 'metadata-web', environment.testbedVersion, null, null, null);
    this.elasticsearch.exportTrial(selectedIndexName, selectedTrialId, filename, exportMessage).then(() => {
      this.trialService.sendExportMessage(exportMessage);
    }).catch(error => this.log('Export error: ' + error)); // .finally(() => this.exportTrialForm.reset());
  }

  private log(message: string) {
    this.loggingService.add(`ExportTrialComponent: ${message}`);
  }
}
