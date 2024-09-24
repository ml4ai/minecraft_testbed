import { Component, Inject, OnInit } from '@angular/core';
import { Experiment } from '../../experiment/experiment';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ExperimentService } from '../../experiment/experiment.service';
import { v4 as uuidv4 } from 'uuid';
import { Trial } from '../trial';

@Component({
  selector: 'app-update-trial',
  templateUrl: './update-trial.component.html',
  styleUrls: ['./update-trial.component.scss']
})
export class UpdateTrialComponent implements OnInit {
  experiments: Experiment[];
  updateTrialForm = this.formBuilder.group({
    id: ['', Validators.required],
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
    testbed_version: ['', Validators.required],
    experiment: ['', Validators.required]
  });
  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<UpdateTrialComponent>,
    private experimentService: ExperimentService,
    @Inject(MAT_DIALOG_DATA) public data: Trial) {
  }

  readExperiments(): void {
    this.experimentService.readExperiments()
      .subscribe(experiments => {
        this.experiments = experiments;
      });
  }

  onUpdateClick(): void {
    const dialogResult = this.updateTrialForm.value;

    const subjectsText = this.updateTrialForm.get('subjects').value;
    if (subjectsText !== '') {
      dialogResult.subjects = subjectsText.split(/[\r\n]+/);
    } else {
      dialogResult.subjects = [];
    }

    const notesText = this.updateTrialForm.get('notes').value;
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
    this.updateTrialForm.patchValue({
      trial_id: uuidv4()
    });
  }

  ngOnInit(): void {
    this.readExperiments();

    this.updateTrialForm.setValue({
      id: this.data.id,
      trial_id: this.data.trial_id,
      name: this.data.name,
      date: this.data.date,
      experimenter: this.data.experimenter,
      subjects: this.data.subjects.length > 0 ? this.data.subjects.join('\r\n') : this.data.subjects,
      trial_number: this.data.trial_number,
      group_number: this.data.group_number,
      study_number: this.data.study_number,
      condition: this.data.condition,
      notes: this.data.notes.length > 0 ? this.data.notes.join('\r\n') : this.data.notes,
      testbed_version: this.data.testbed_version,
      experiment: this.data.experiment
    });
  }

  compareFnExperiments(e1: Experiment, e2: Experiment): boolean {
    return e1 && e2 ? e1.id === e2.id : e1 === e2;
  }
}
