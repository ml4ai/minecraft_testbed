import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ElasticsearchService } from '../elasticsearch';
import {concatMap, map, startWith} from 'rxjs/operators';
import {forkJoin, Observable, Subscription} from 'rxjs';
import { ReadableStream } from 'web-streams-polyfill/ponyfill';
import { LoggingService } from '../../logging/logging.service';
import { FirstLineReader } from '../elasticsearch/first-line-reader';
import { TrialExportMessage } from '../../trial/trial-export-message';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { TrialService } from '../../trial/trial.service';
import { ExperimentService } from '../../experiment/experiment.service';
import { FileInputComponent } from 'ngx-material-file-input';
import { Trial } from '../../trial/trial';

@Component({
  selector: 'app-import-trial',
  templateUrl: './import-trial.component.html',
  styleUrls: ['./import-trial.component.scss']
})
export class ImportTrialComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;
  private file = '';
  metadataFileDetected = false;
  // usingIndexFromMetadataFile = false;
  trialExportMessage: TrialExportMessage = null;

  private isImportingTrialSubscription: Subscription;
  public isImportingTrial = false;

  indices: any[];
  filteredIndices: Observable<any[]>;

  replays: string[];

  indexNameControl = this.formBuilder.control('', Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true}, Validators.required);

  importFileControl = this.formBuilder.control([], Validators.required);
  useIndexFromMetadataFileControl = this.formBuilder.control(false);

  indexNameCreateControl = this.formBuilder.control({value: false, disabled: true});

  importTrialForm = this.formBuilder.group({
    indexName: this.indexNameControl,
    overrideIndexNameToggle: this.overrideIndexNameToggleControl,
    indexNameEntered: this.indexNameEnteredControl,
    indexNameCreate: this.indexNameCreateControl,
    importFile: this.importFileControl,
    useIndexFromMetadataFile: this.useIndexFromMetadataFileControl
  });

  indexPattern: RegExp = new RegExp(/^(?=[a-z0-9_\-])(?!.*[\s,:"*+\/\\|?#><]+)(?!_|-)/);

  fileTrial = '';
  fileExperiment = '';
  fileIndex = '';
  @ViewChild(FileInputComponent, { }) public fileInputComponent: any;

  constructor(
    private formBuilder: FormBuilder,
    private elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private trialService: TrialService,
    private experimentService: ExperimentService
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

    this.isImportingTrialSubscription = this.elasticsearch.isImportingTrial.subscribe(isImportingTrial => this.isImportingTrial = isImportingTrial);

    this.indexNameControl.valueChanges.subscribe((newStatus) => {
      if (this.indexNameControl.disabled) {
        this.indexNameEnteredControl.enable();
        this.indexNameCreateControl.enable();
      } else {
        this.indexNameEnteredControl.disable();
        this.indexNameCreateControl.disable();
      }
    });
  }

  ngOnDestroy(): void {
    this.indexSubscription.unsubscribe();
    this.isImportingTrialSubscription.unsubscribe();
  }

  updateIndexSelection(event): void {
    const index = event.option.value;
    this.indexNameEnteredControl.enable();
    this.indexNameCreateControl.enable();
    this.importTrialForm.patchValue({
      indexNameEnteredControl: index,
      indexNameCreateControl: false
    });
    this.indexNameEnteredControl.disable();
    this.indexNameCreateControl.disable();
  }

  toggleFileIndexOverrideChange(): void {

  }

  metadataDetectedOpened(): void {
    if ('trial' in this.trialExportMessage.data.metadata)  {
      this.fileTrial = this.trialExportMessage.data.metadata.trial.name;
      this.fileExperiment = this.trialExportMessage.data.metadata.trial.experiment_name;
      this.fileIndex = this.trialExportMessage.data.index;
    } else {
      this.log('Metadata file had incorrect header information!');
      this.metadataFileDetected = false;
      this.trialExportMessage = null;
    }
  }

  metadataDetectedClosed(): void {
    this.fileTrial = '';
    this.fileExperiment = '';
    this.fileIndex = '';
  }

  toggleIndexOverrideChange(): void {
    this.indexNameControl.disabled ? this.importTrialForm.get('indexName').enable() : this.importTrialForm.get('indexName').disable();
    if (this.indexNameControl.disabled) {
      this.indexNameControl.reset('', {
        onlySelf: true
      });
    }
    if (this.indexNameEnteredControl.disabled) {
      this.indexNameEnteredControl.reset('', {
        onlySelf: true
      });
      this.indexNameCreateControl.reset('', {
        onlySelf: true
      });
    }
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

  displayIndexNameFn(index: any): string {
    return index && index.index ? index.index : '';
  }

  onFileSelected() {
    this.getFirstLine().then((result) => {
      try {
        this.trialExportMessage = JSON.parse(result[0]) as TrialExportMessage;
        // should we test his in case header is not there?????
        if ('metadata' in this.trialExportMessage.data) {
          this.metadataFileDetected = true;
        } else {
          this.metadataFileDetected = true;
          throw new Error('No metadata property in data section of message!');
        }
      } catch (e) {
        this.fileTrial = '';
        this.fileExperiment = '';
        this.fileIndex = '';
        this.trialExportMessage = null;
        this.metadataFileDetected = false;
        this.log(e);
      }
    });
  }

  private async getFirstLine() {
    const dataset = [];
    const file: File = this.importFileControl.value.files[0];
    const lineReader = new FirstLineReader(file);

    // Context is optional. It can be used to inside processLineFn
    const context = {};
    await lineReader.forEachLine(processLineFn, context)
      .then((result) => console.log('Done!', result));

    return dataset;

    // Context is same Object as passed while calling forEachLine
    function processLineFn(_line: string, _index: number, _context: any) {
      // console.log(index, _line)
      dataset.push(_line);
    }
  }

  onImportClick() {
    const selectedImportFile: File = this.importFileControl.value.files[0];
    let selectedIndexName = '';

    if (!this.overrideIndexNameToggleControl.value) {
      selectedIndexName = this.indexNameControl.value.index;
    } else {
      selectedIndexName = this.indexNameEnteredControl.value;
    }

    if (this.metadataFileDetected) {
      if (this.useIndexFromMetadataFileControl.value) {
        selectedIndexName = this.trialExportMessage.data.index;
      } else if (!this.overrideIndexNameToggleControl.value) {
        selectedIndexName = this.indexNameControl.value.index;
      } else {
        selectedIndexName = this.indexNameEnteredControl.value;
      }
      // Create db entries here!
      const experiment = {
        id: -1,
        experiment_id: this.trialExportMessage.msg.experiment_id,
        name: this.trialExportMessage.data.metadata.trial.experiment_name,
        date: this.trialExportMessage.data.metadata.trial.experiment_date,
        author: this.trialExportMessage.data.metadata.trial.experiment_author,
        mission: this.trialExportMessage.data.metadata.trial.experiment_mission
      };
      const trial = {
        id: -1,
        trial_id: this.trialExportMessage.msg.trial_id,
        name: this.trialExportMessage.data.metadata.trial.name,
        date: this.trialExportMessage.data.metadata.trial.date,
        experimenter: this.trialExportMessage.data.metadata.trial.experimenter,
        subjects: this.trialExportMessage.data.metadata.trial.subjects,
        trial_number: this.trialExportMessage.data.metadata.trial.trial_number,
        group_number: this.trialExportMessage.data.metadata.trial.group_number,
        study_number: this.trialExportMessage.data.metadata.trial.study_number,
        condition: this.trialExportMessage.data.metadata.trial.condition,
        notes: this.trialExportMessage.data.metadata.trial.notes,
        testbed_version: this.trialExportMessage.data.metadata.trial.testbed_version,
        experiment
      };
      // this.experimentService.createExperiment(experiment).subscribe(() => {
      //   // this.log(`Experiment ${this.trialExportMessage.data.metadata.trial.experiment_name} created using information in file.`);
      //   // this.showOverlay();
      // }, (err) => {
      //   this.log(`Create Experiment error [${err}].`);
      // }, () => {
      //   this.trialService.createTrial(trial).subscribe(_ => {
      //     // this.log(`Trial ${this.trialExportMessage.data.metadata.trial.name} created using information in file.`);
      //     // this.showOverlay();
      //   }, (err) => {
      //     this.log(`Create Trial error [${err}].`);
      //   });
      // });
      this.experimentService.createExperiment(experiment).pipe(
        concatMap(e => this.trialService.createTrial(trial).pipe(
          ))).subscribe(t => {
        // this.log(`Trial ${this.trialExportMessage.data.metadata.trial.name} created using information in file.`);
        // this.showOverlay();
      }, (err) => {
        this.log(`Error creating metadata for Trial import [${err}].`);
      });
    }
    if (this.indexNameCreateControl.value) {
      this.elasticsearch.createIndex(selectedIndexName)
        .subscribe(
          data => {
            const trial_id = this.trialExportMessage.msg.trial_id;
            this.importTrialForm.reset();
            this.metadataFileDetected = false;
            this.trialExportMessage = null;
            this.fileInputComponent.clear();
            this.indexNameControl.enable();
            this.indexNameEnteredControl.disable();
            this.trialService.getExistReplay(trial_id, selectedIndexName).subscribe(exist => {
              if (!exist) {
                this.elasticsearch.importTrial(selectedIndexName, selectedImportFile).then(results => {
                  this.log(`Imported ${results.success} out of ${results.total} documents with ${results.error} errors.`);
                  this.elasticsearch.catIndices();
                }).catch(error => this.log('Import error: ' + error));
              } else {
                this.log(`Can not import into index ${selectedIndexName} because trial ${trial_id} already exists here!`);
              }
            });

          },
          error => {
            this.log(`Error: ${JSON.stringify(error)}`);
          });
    } else {
      const trial_id = this.trialExportMessage.msg.trial_id;
      this.importTrialForm.reset();
      this.metadataFileDetected = false;
      this.trialExportMessage = null;
      this.fileInputComponent.clear();
      this.indexNameControl.enable();
      this.indexNameEnteredControl.disable();
      this.trialService.getExistReplay(trial_id, selectedIndexName).subscribe(exist => {
        if (!exist) {
          this.elasticsearch.importTrial(selectedIndexName, selectedImportFile).then(results => {
            this.log(`Imported ${results.success} out of ${results.total} documents with ${results.error} errors.`);
            this.elasticsearch.catIndices();
          }).catch(error => {
            this.log('Import error: ' + error);
          });
        } else {
          this.log(`Can not import into index ${selectedIndexName} because trial ${trial_id} already exists here!`);
        }
      });
    }
  }

  public usingIndexFromMetadataFileChecked($event: MatCheckboxChange) {
    // this.usingIndexFromMetadataFile = $event.checked;

    this.indexNameControl.reset('', {
      onlySelf: true
    });
    this.overrideIndexNameToggleControl.reset('', {
      onlySelf: true
    });
    this.indexNameEnteredControl.reset('', {
      onlySelf: true
    });
    this.indexNameCreateControl.reset('', {
      onlySelf: true
    });
  }

  public isFormDisabled(): boolean {
    if (!this.metadataFileDetected) {
      return true;
    } else {
      if (this.useIndexFromMetadataFileControl.value) {
        return false;
      } else {
        return !this.importTrialForm.valid;
      }
    }
  }

  private log(message: string) {
    this.loggingService.add(`ImportTrialComponent: ${message}`);
  }
}
