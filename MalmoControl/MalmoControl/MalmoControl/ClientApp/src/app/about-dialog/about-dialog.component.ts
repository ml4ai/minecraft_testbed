import { Component, OnInit, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-about-dialog',
  templateUrl: './about-dialog.component.html',
  styleUrls: ['./about-dialog.component.css']
})
export class AboutDialogComponent implements OnInit {

  baseUrl;

  aboutObject: IAboutObject;
  load = false;

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string, public dialogRef: MatDialogRef<AboutDialogComponent>) {

    this.baseUrl = baseUrl;

   }

  ngOnInit() {

    this.http.get<IAboutObject>(this.baseUrl + 'api/Help/getAbout').subscribe(response => {
      this.aboutObject = response as IAboutObject;
      this.load = true;
      },
      error => console.error(error),
      () => console.log(this.aboutObject)
    );
  }

  close() {
    this.dialogRef.close( 'canceled' );
  }
}

interface IAboutObject {

  system_name: string;
  system_description: string;
  darpa_acknolwedgement: string;
  system_version: string;
  system_build_date: string;
  aptima_legal_notice: string;
  other_notices: string[];


}
