import { Inject } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-action-dialog',
  templateUrl: './action-dialog.component.html',
  styleUrls: ['./action-dialog.component.scss']
})
export class ActionDialogComponent implements OnInit {

  // color: string ;

  message: string;

  constructor(public dialogRef: MatDialogRef<ActionDialogComponent>,@Inject(MAT_DIALOG_DATA) public data) { 
    this.message = data['message'];
   }

  ngOnInit(): void {
  }

  close(){
    //this.dialogRef.close( this.color );
    this.dialogRef.close( );
  }

}
