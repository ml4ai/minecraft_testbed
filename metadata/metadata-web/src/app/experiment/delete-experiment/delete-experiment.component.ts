import { Component, Inject, OnInit } from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { v4 as uuidv4 } from 'uuid';
import { Experiment } from '../experiment';

@Component({
  selector: 'app-delete-experiment',
  templateUrl: './delete-experiment.component.html',
  styleUrls: ['./delete-experiment.component.scss']
})
export class DeleteExperimentComponent implements OnInit {

  deleteExperimentForm = this.formBuilder.group({
    id: ['', Validators.required],
    experiment_id: ['', Validators.required],
    name: ['', Validators.required],
    date: ['', Validators.required],
    author: ['', Validators.required],
    mission: ['', Validators.required]
  });
  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<DeleteExperimentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Experiment) {}

  onDeleteClick(): void {
    this.dialogRef.close(this.deleteExperimentForm.getRawValue());
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.deleteExperimentForm.patchValue({
      experiment_id: uuidv4()
    });
  }

  ngOnInit(): void {
    this.deleteExperimentForm.setValue({
      id: this.data.id,
      experiment_id: this.data.experiment_id,
      name: this.data.name,
      date: this.data.date,
      author: this.data.author,
      mission: this.data.mission
    });
    this.deleteExperimentForm.disable();
  }
}
