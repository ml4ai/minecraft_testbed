import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TrialsComponent } from './trials/trials.component';

const routes: Routes = [
  {
    path: '',
    component: TrialsComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TrialRoutingModule {
}
