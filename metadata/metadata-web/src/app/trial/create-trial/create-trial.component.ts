import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Trial } from '../trial';
import { v4 as uuidv4 } from 'uuid';
import { Experiment } from '../../experiment/Experiment';
import { ExperimentService } from '../../experiment/experiment.service';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { LoggingService } from '../../logging/logging.service';
import { JsonTrialComponent } from '../json-trial/json-trial.component';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-create-trial',
  templateUrl: './create-trial.component.html',
  styleUrls: ['./create-trial.component.scss']
})
export class CreateTrialComponent implements OnInit {
  experiments: Experiment[] = [];
  createTrialForm = this.formBuilder.group({
    trial_id: ['', Validators.required],
    name: ['', Validators.required],
    date: ['', Validators.required],
    experimenter: ['', Validators.required],
    subjects: ['', Validators.required],
    trial_number: ['', Validators.required],
    group_number: ['', Validators.required],
    study_number: ['', Validators.required],
    condition: ['', Validators.required],
    notes: [''],
    testbed_version: [environment.testbedVersion, Validators.required],
    experiment: ['', Validators.required],
    useMessageBus: [false]
  });
  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<CreateTrialComponent>,
    private experimentService: ExperimentService,
    public jsonDialog: MatDialog,
    private loggingService: LoggingService,
    @Inject(MAT_DIALOG_DATA) public data: Trial) {
  }

  readExperiments(): void {
    this.experimentService.readExperiments()
      .subscribe(experiments => {
        this.experiments = experiments;
      });
  }

  openJsonTrialDialog(): void {
    const dialogResult = this.createTrialForm.value;

    const subjectsText = this.createTrialForm.get('subjects').value;
    if (subjectsText !== '') {
      dialogResult.subjects = subjectsText.split(/[\r\n]+/);
    } else {
      dialogResult.subjects = [];
    }

    const notesText = this.createTrialForm.get('notes').value;
    if (notesText !== '') {
      dialogResult.notes = notesText.split(/[\r\n]+/);
    } else {
      dialogResult.notes = [];
    }

    delete dialogResult.useMessageBus;

    const jsonDialogRef = this.jsonDialog.open(JsonTrialComponent, {
      // width: '250px',
      data: JSON.stringify(dialogResult, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const trial = JSON.parse(result.json);
          // let experiment = {
          //   name: trial.experiment
          // }
          const experiment = this.experiments.find(e => e.name === trial.experiment);
          this.createTrialForm.patchValue({
            trial_id: trial.trial_id,
            name: trial.name,
            date: trial.date,
            experimenter: trial.experimenter,
            subjects: trial.subjects.length > 0 ? trial.subjects.join('\r\n') : trial.subjects,
            trial_number: trial.trial_number,
            group_number: trial.group_number,
            study_number: trial.study_number,
            condition: trial.condition,
            notes: trial.notes.length > 0 ? trial.notes.join('\r\n') : trial.notes,
            testbed_version: trial.testbed_version,
            experiment
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  onCreateClick(): void {
    const dialogResult = this.createTrialForm.value;

    const subjectsText = this.createTrialForm.get('subjects').value;
    if (subjectsText !== '') {
      dialogResult.subjects = subjectsText.split(/[\r\n]+/);
    } else {
      dialogResult.subjects = [];
    }

    const notesText = this.createTrialForm.get('notes').value;
    if (notesText !== '') {
      dialogResult.notes = notesText.split(/[\r\n]+/);
    } else {
      dialogResult.notes = [];
    }

    this.dialogRef.close(dialogResult);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.createTrialForm.patchValue({
      trial_id: uuidv4()
    });
  }

  toggleUseMessageBusChange(event: MatSlideToggleChange) {
    // if (event.checked) {
    //   this.createTrialForm.controls['trial_id'].reset('', {
    //     onlySelf: true
    //   });
    // } else {
    //   this.createTrialForm.controls['trial_id'].reset('', {
    //     onlySelf: true
    //   });
    // }
  }

  ngOnInit(): void {
    this.readExperiments();
  }

  compareFnExperiments(e1: Experiment, e2: Experiment): boolean {
    return e1 && e2 ? e1.name === e2.name : e1 === e2;
  }

  /** Log a TrialService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`CreateTrialComponent: ${message}`);
  }

}
