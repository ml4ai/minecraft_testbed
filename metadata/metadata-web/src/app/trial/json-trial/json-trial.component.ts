import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-json-trial',
  templateUrl: './json-trial.component.html',
  styleUrls: ['./json-trial.component.scss']
})
export class JsonTrialComponent implements OnInit {
  jsonTrialForm = this.formBuilder.group({
    json: ['']
  });
  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<JsonTrialComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string
  ) { }

  ngOnInit(): void {
    this.jsonTrialForm.setValue({
      json: this.data,
    });
  }

  onParseClick(): void {
    const dialogResult = this.jsonTrialForm.value;

    this.dialogRef.close(dialogResult);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

}
