import { Component, OnInit, isDevMode } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app';

  /**
   *
   */
  constructor (private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer) {

    this.matIconRegistry
    .addSvgIcon(
      'description',
      this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/description-24px.svg'));
    // .addSvgIcon(
    //   'insert_chart_outlined',
    //   this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/insert_chart_outlined-24px.svg')
    // )

  }

  ngOnInit() {

    if (isDevMode()) {
      console.log('👋 Development!');
    } else {
      console.log('💪 Production!');
    }

    // Sets the background image

    document.body.style.backgroundImage = 'url(\"' + environment.hostpath + 'assets/images/wood.jpg\")';


  }




}
