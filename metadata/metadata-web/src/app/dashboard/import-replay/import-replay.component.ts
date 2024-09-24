import {Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {ElasticsearchService} from '../elasticsearch';
import {concatMap, map, mergeMap, startWith} from 'rxjs/operators';
import {Observable, Subscription, forkJoin, of} from 'rxjs';
import {ReadableStream} from 'web-streams-polyfill/ponyfill';
import {LoggingService} from '../../logging/logging.service';
import {ReplayExportMessage} from '../../replay/replay-export-message';
import {FirstLineReader} from '../elasticsearch/first-line-reader';
import {TrialService} from '../../trial/trial.service';
import {ExperimentService} from '../../experiment/experiment.service';
import {ReplayService} from '../../replay/replay.service';
import {Trial} from '../../trial/trial';
import {Replay} from '../../replay/replay';
import {MatCheckboxChange} from '@angular/material/checkbox';
import {Experiment} from '../../experiment/experiment';
import {FileInputComponent} from 'ngx-material-file-input';

@Component({
  selector: 'app-import-replay',
  templateUrl: './import-replay.component.html',
  styleUrls: ['./import-replay.component.scss']
})
export class ImportReplayComponent implements OnInit, OnDestroy {
  private indexSubscription: Subscription;
  file = '';
  metadataFileDetected = false;
  replayExportMessage: ReplayExportMessage = null;

  private isImportingReplaySubscription: Subscription;
  public isImportingReplay = false;

  indices: any[] = [];
  filteredIndices: Observable<any[]>;

  replays: string[] = [];

  indexNameControl = this.formBuilder.control('', Validators.required);
  overrideIndexNameToggleControl = this.formBuilder.control(false);
  indexNameEnteredControl = this.formBuilder.control({value: '', disabled: true}, Validators.required);

  importFileControl = this.formBuilder.control([], Validators.required);
  useIndexFromMetadataFileControl = this.formBuilder.control(false);

  indexNameCreateControl = this.formBuilder.control({value: false, disabled: true});

  importReplayForm = this.formBuilder.group({
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
  fileReplays: (Trial | Replay)[] = [];
  @ViewChild(FileInputComponent, {}) public fileInputComponent: any;

  constructor(
    private formBuilder: FormBuilder,
    private elasticsearch: ElasticsearchService,
    private loggingService: LoggingService,
    private trialService: TrialService,
    private experimentService: ExperimentService,
    private replayService: ReplayService,
  ) {
  }

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

    this.isImportingReplaySubscription = this.elasticsearch.isImportingReplay.subscribe(isImportingReplay => this.isImportingReplay = isImportingReplay);

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
    this.isImportingReplaySubscription.unsubscribe();
  }

  updateIndexSelection(event): void {
    const index = event.option.value;
    this.indexNameEnteredControl.enable();
    this.indexNameCreateControl.enable();
    this.importReplayForm.patchValue({
      indexNameEnteredControl: index,
      indexNameCreateControl: false
    });
    this.indexNameEnteredControl.disable();
    this.indexNameCreateControl.disable();
  }

  toggleFileIndexOverrideChange(): void {

  }

  metadataDetectedOpened(): void {
    if (this.replayExportMessage != null) {
      const root = this.replayExportMessage.data.metadata.parents[this.replayExportMessage.data.metadata.parents.length - 1] as Trial;
      if (root.trial_id) {
        const replay = {
          id: -1,
          replay_id: this.replayExportMessage.data.metadata.replay.replay_id,
          replay_parent_id: this.replayExportMessage.data.metadata.replay.replay_parent_id,
          replay_parent_type: this.replayExportMessage.data.metadata.replay.replay_parent_type,
          date: this.replayExportMessage.data.metadata.replay.date,
          ignore_message_list: this.replayExportMessage.data.metadata.replay.ignore_message_list,
          ignore_source_list: this.replayExportMessage.data.metadata.replay.ignore_source_list,
          ignore_topic_list: this.replayExportMessage.data.metadata.replay.ignore_topic_list
        } as Replay;
        this.fileTrial = root.name;
        this.fileExperiment = root.experiment.name;
        this.fileIndex = this.replayExportMessage.data.index;
        this.fileReplays = this.replayExportMessage.data.metadata.parents.concat([replay]);
      } else {
        this.log('Metadata file had incorrect header information!');
        this.metadataFileDetected = false;
        this.replayExportMessage = null;
        this.fileReplays = [];
      }
    }
  }

  metadataDetectedClosed(): void {
    this.fileTrial = '';
    this.fileExperiment = '';
    this.fileIndex = '';
    this.fileReplays = [];
  }

  toggleIndexOverrideChange(): void {
    this.indexNameControl.disabled ? this.importReplayForm.get('indexName').enable() : this.importReplayForm.get('indexName').disable();
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
        this.replayExportMessage = JSON.parse(result[0]) as ReplayExportMessage;
        // should we test his in case header is not there?????
        if ('metadata' in this.replayExportMessage.data) {
          this.metadataFileDetected = true;
        } else {
          this.metadataFileDetected = true;
          throw new Error('No metadata property in data section of message!');
        }
      } catch (e) {
        this.fileTrial = '';
        this.fileExperiment = '';
        this.fileIndex = '';
        this.fileReplays = [];
        this.replayExportMessage = null;
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

  // onImportClick() {
  //   const selectedImportFile: File = this.importFileControl.value.files[0];
  //   let selectedIndexName = '';
  //   if (!this.overrideIndexNameToggleControl.value) {
  //     selectedIndexName = this.indexNameControl.value.index;
  //   } else {
  //     selectedIndexName = this.indexNameEnteredControl.value;
  //   }
  //   if (this.indexNameCreateControl.value) {
  //     this.log(`Creating index: ${selectedIndexName}`);
  //     this.elasticsearch.createIndex(selectedIndexName)
  //       .subscribe(
  //         data => {
  //           this.importReplayForm.reset();
  //           this.elasticsearch.catIndices();
  //           this.elasticsearch.importReplay(selectedIndexName, selectedImportFile).then(results => this.log('Imported ' + results + ' documents successfully.')).catch(error => this.log('Import error: ' + error)); // .finally(() => this.importReplayForm.reset());
  //         },
  //         error => {
  //           this.log(`Error: ${JSON.stringify(error)}`);
  //         });
  //   } else {
  //     this.importReplayForm.reset();
  //     this.elasticsearch.importReplay(selectedIndexName, selectedImportFile).then(results => { this.log('Imported ' + results + ' documents successfully.'); }).catch(error => this.log('Import error: ' + error)); // .finally(() => this.importReplayForm.reset());
  //   }
  // }
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
        selectedIndexName = this.replayExportMessage.data.index;
      } else if (!this.overrideIndexNameToggleControl.value) {
        selectedIndexName = this.indexNameControl.value.index;
      } else {
        selectedIndexName = this.indexNameEnteredControl.value;
      }
      const root = this.replayExportMessage.data.metadata.parents[this.replayExportMessage.data.metadata.parents.length - 1] as Trial;
      if (root === null) {
        this.log('Root item in replay parent tree was not a Trial!');
        return null;
      }
      // Create db entries here!
      const experiment = {
        id: -1,
        experiment_id: root.experiment.experiment_id,
        name: root.experiment.name,
        date: root.experiment.date,
        author: root.experiment.author,
        mission: root.experiment.mission
      } as Experiment;
      const trial = {
        id: -1,
        trial_id: root.trial_id,
        name: root.name,
        date: root.date,
        experimenter: root.experimenter,
        subjects: root.subjects,
        trial_number: root.trial_number,
        group_number: root.group_number,
        study_number: root.study_number,
        condition: root.condition,
        notes: root.notes,
        testbed_version: root.testbed_version,
        experiment
      } as Trial;
      const replay = {
        id: -1,
        replay_id: this.replayExportMessage.data.metadata.replay.replay_id,
        replay_parent_id: this.replayExportMessage.data.metadata.replay.replay_parent_id,
        replay_parent_type: this.replayExportMessage.data.metadata.replay.replay_parent_type,
        date: this.replayExportMessage.data.metadata.replay.date,
        ignore_message_list: this.replayExportMessage.data.metadata.replay.ignore_message_list,
        ignore_source_list: this.replayExportMessage.data.metadata.replay.ignore_source_list,
        ignore_topic_list: this.replayExportMessage.data.metadata.replay.ignore_topic_list
      } as Replay;
      // Remove the root trial.
      const replays = this.replayExportMessage.data.metadata.parents.concat([replay]).slice(1) as Replay[];
      this.experimentService.createExperiment(experiment).pipe(
        concatMap(e => this.trialService.createTrial(trial).pipe(
          concatMap(t => forkJoin(
            replays.map(r => this.replayService.createReplay(r)
            )))))).subscribe(i => {
      }, (err) => {
        this.log(`Error creating metadata for Replay import [${err}].`);
      });
    }
    if (this.indexNameCreateControl.value) {
      this.elasticsearch.createIndex(selectedIndexName)
        .subscribe(
          data => {
            const replay_id = this.replayExportMessage.data.metadata.replay.replay_id;
            this.importReplayForm.reset();
            this.metadataFileDetected = false;
            this.replayExportMessage = null;
            this.fileInputComponent.clear();
            this.indexNameControl.enable();
            this.indexNameEnteredControl.disable();
            this.replayService.getExistReplay(replay_id, selectedIndexName).subscribe(exist => {
              if (!exist) {
                this.elasticsearch.importReplay(selectedIndexName, selectedImportFile).then(results => {
                  this.log(`Imported ${results.success} out of ${results.total} documents with ${results.error} errors.`);
                  this.elasticsearch.catIndices();
                }).catch(error => this.log('Import error: ' + error));
              } else {
                this.log(`Can not import into index ${selectedIndexName} because replay ${replay_id} already exists here!`);
              }
            });
          },
          error => {
            this.log(`Error: ${JSON.stringify(error)}`);
          });
    } else {
      const replay_id = this.replayExportMessage.data.metadata.replay.replay_id;
      this.importReplayForm.reset();
      this.metadataFileDetected = false;
      this.replayExportMessage = null;
      this.fileInputComponent.clear();
      this.indexNameControl.enable();
      this.indexNameEnteredControl.disable();
      this.replayService.getExistReplay(replay_id, selectedIndexName).subscribe(exist => {
        if (!exist) {
          this.elasticsearch.importReplay(selectedIndexName, selectedImportFile).then(results => {
            this.log(`Imported ${results.success} out of ${results.total} documents with ${results.error} errors.`);
            this.elasticsearch.catIndices();
          }).catch(error => {
            this.log('Import error: ' + error);
          });
        } else {
          this.log(`Can not import into index ${selectedIndexName} because replay ${replay_id} already exists here!`);
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
        return !this.importReplayForm.valid;
      }
    }
  }

  private log(message: string) {
    this.loggingService.add(`ImportReplayComponent: ${message}`);
  }
}

