import { Component, Inject, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { v4 as uuidv4 } from 'uuid';
import { Experiment } from '../experiment';

@Component({
  selector: 'app-update-experiment',
  templateUrl: './update-experiment.component.html',
  styleUrls: ['./update-experiment.component.scss']
})
export class UpdateExperimentComponent implements OnInit {

  updateExperimentForm = this.formBuilder.group({
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
    private dialogRef: MatDialogRef<UpdateExperimentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Experiment) {}

  onUpdateClick(): void {
    this.dialogRef.close(this.updateExperimentForm.value);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.updateExperimentForm.patchValue({
      experiment_id: uuidv4()
    });
  }

  ngOnInit(): void {
    this.updateExperimentForm.setValue({
      id: this.data.id,
      experiment_id: this.data.experiment_id,
      name: this.data.name,
      date: this.data.date,
      author: this.data.author,
      mission: this.data.mission
    });
  }

}
