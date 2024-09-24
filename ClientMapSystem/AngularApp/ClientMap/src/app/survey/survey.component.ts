import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Survey, SurveyDialogData } from '../survey';
import { WebsocketService } from '../websocket.service';

@Component({
  selector: 'app-survey',
  templateUrl: './survey.component.html',
  styleUrls: ['./survey.component.scss']
})
export class SurveyComponent implements OnInit {
  safeUrl:SafeUrl;

  constructor(
    private websocketService: WebsocketService,
    public dialogRef: MatDialogRef<SurveyComponent>,
    private sanitizer: DomSanitizer,
    @Inject(MAT_DIALOG_DATA) public data: SurveyDialogData) { }

  ngOnInit(): void {
    this.getUrl(this.data)
  }

  getUrl(data: SurveyDialogData) {
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
      'https://iad1.qualtrics.com/jfe/form/' + data.id +
      '/?participantid=' + data.participant_id +
      '&surveyname=' + data.name +
      '&uniqueid=' + data.unique_id);
  }
}
