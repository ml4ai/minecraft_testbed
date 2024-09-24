import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { Experiment } from '../../experiment/experiment';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ExperimentService } from '../../experiment/experiment.service';
import { v4 as uuidv4 } from 'uuid';
import { Trial } from '../trial';

@Component({
  selector: 'app-delete-trial',
  templateUrl: './delete-trial.component.html',
  styleUrls: ['./delete-trial.component.scss']
})
export class DeleteTrialComponent implements OnInit {
  experiments: Experiment[];
  deleteTrialForm = this.formBuilder.group({
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
    private dialogRef: MatDialogRef<DeleteTrialComponent>,
    private experimentService: ExperimentService,
    @Inject(MAT_DIALOG_DATA) public data: Trial) {
  }

  readExperiments(): void {
    this.experimentService.readExperiments()
      .subscribe(experiments => {
        this.experiments = experiments;
      });
  }

  onDeleteClick(): void {
    this.dialogRef.close(this.deleteTrialForm.getRawValue());
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.deleteTrialForm.patchValue({
      trial_id: uuidv4()
    });
  }

  ngOnInit(): void {
    this.readExperiments();

    this.deleteTrialForm.setValue({
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
    this.deleteTrialForm.disable();
  }

  compareFnExperiments(e1: Experiment, e2: Experiment): boolean {
    return e1 && e2 ? e1.id === e2.id : e1 === e2;
  }
}
