import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ReplaysComponent } from '../replay/replays/replays.component';

const routes: Routes = [
  {
    path: '',
    component: ReplaysComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReplayRoutingModule { }
