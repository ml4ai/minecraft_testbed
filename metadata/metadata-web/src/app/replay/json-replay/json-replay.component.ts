import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-json-replay',
  templateUrl: './json-replay.component.html',
  styleUrls: ['./json-replay.component.scss']
})
export class JsonReplayComponent implements OnInit {
  jsonExperimentForm = this.formBuilder.group({
    json: ['']
  });
  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<JsonReplayComponent>,
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
