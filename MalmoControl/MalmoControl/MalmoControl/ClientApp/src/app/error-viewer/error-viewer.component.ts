import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../Services/websocket.service';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-error-viewer',
  templateUrl: './error-viewer.component.html',
  styleUrls: ['./error-viewer.component.css']
})
export class ErrorViewerComponent implements OnInit {

  constructor(public webSocketService: WebsocketService, public dialogRef: MatDialogRef<ErrorViewerComponent>) { }

  ngOnInit() {
  }

  close() {
    this.dialogRef.close();
  }

}
