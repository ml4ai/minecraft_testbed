import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { MapParentComponent } from './map-parent/map-parent.component';
import { environment } from '../environments/environment';
import {HumanAdvisorComponent} from './human-advisor/human-advisor.component';

// let loadedSettings: string;

// function readFile(file) {
//   const raw = new XMLHttpRequest(); // create a request
//   raw.open('GET', file, false); // open file
//   raw.onreadystatechange = function () { // file is ready to read
//     if (raw.readyState === 4) {
//       if (raw.status === 200 || raw.status === 0) {
//         const allText = raw.responseText;
//         loadedSettings = allText;
//       }
//     }
//   };
//   raw.send(null); // return control
// }
// if (environment.production) {
//   readFile('./assets/config.prod.json');
// } else {
//   readFile('./assets/config.develop.json');
// }

// if (loadedSettings) {
//   const parsedSettings = JSON.parse(loadedSettings);
//   environment.asistDataIngesterPath = parsedSettings.asistDataIngesterPath ? parsedSettings.asistDataIngesterPath : '';
//   console.log('AsistDataIngesterPath: ' + environment.asistDataIngesterPath);
// }

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'map', component: MapParentComponent },
  { path: 'advisor', component: HumanAdvisorComponent},
  { path: '', redirectTo: '/login', pathMatch: 'full' },
 
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
