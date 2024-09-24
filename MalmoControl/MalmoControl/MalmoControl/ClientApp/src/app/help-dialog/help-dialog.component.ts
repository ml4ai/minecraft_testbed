import { Component, OnInit, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-help-dialog',
  templateUrl: './help-dialog.component.html',
  styleUrls: ['./help-dialog.component.css']
})
export class HelpDialogComponent implements OnInit {

  baseUrl

  constructor( private http: HttpClient, @Inject('BASE_URL') baseUrl: string, public dialogRef: MatDialogRef<HelpDialogComponent>) { 
    this.baseUrl = baseUrl;
   }

  ngOnInit() {
  }

  close() {
    this.dialogRef.close( 'canceled' );
  }

}
