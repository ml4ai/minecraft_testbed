import {Component, Inject, OnInit} from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-json-dialog',
  templateUrl: './json-dialog.component.html',
  styleUrls: ['./json-dialog.component.scss']
})
export class JsonDialogComponent implements OnInit {

  jsonDialogForm = this.formBuilder.group({
    json: ['']
  });
  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<JsonDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string
  ) { }

  ngOnInit(): void {
    this.jsonDialogForm.setValue({
      json: this.data,
    });
  }

  onParseClick(): void {
    const dialogResult = this.jsonDialogForm.value;

    this.dialogRef.close(dialogResult);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

}
