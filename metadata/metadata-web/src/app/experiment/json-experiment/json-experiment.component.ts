import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-json-experiment',
  templateUrl: './json-experiment.component.html',
  styleUrls: ['./json-experiment.component.scss']
})
export class JsonExperimentComponent implements OnInit {
  jsonExperimentForm = this.formBuilder.group({
    json: ['']
  });
  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<JsonExperimentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string
  ) { }

  ngOnInit(): void {
    this.jsonExperimentForm.setValue({
      json: this.data,
    });
  }

  onParseClick(): void {
    const dialogResult = this.jsonExperimentForm.value;

    this.dialogRef.close(dialogResult);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

}
