import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainScreenComponent } from './main-screen/main-screen.component';
import { ErrorViewerComponent } from './error-viewer/error-viewer.component';

const routes: Routes = [
  { path: '', component: MainScreenComponent },
  { path: 'ErrorViewer', component: ErrorViewerComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
