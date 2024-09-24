import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard/dashboard.component';
import { ExperimentsComponent } from './experiment/experiments/experiments.component';

const routes: Routes = [
  {
    path: 'experiments',
    loadChildren: () => import('./experiment/experiment.module').then(m => m.ExperimentModule),
    data: {
      name: 'Experiments'
    }
  },
  {
    path: 'trials',
    loadChildren: () => import('./trial/trial.module').then(m => m.TrialModule),
    data: {
      name: 'Trials'
    }
  },
  {
    path: 'replays',
    loadChildren: () => import('./replay/replay.module').then(m => m.ReplayModule),
    data: {
      name: 'Replays'
    }
  },
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule),
    data: {
      name: 'Dashboard'
    }
  },
  {
    path: 'docker',
    loadChildren: () => import('./docker/docker.module').then(m => m.DockerModule),
    data: {
      name: 'Docker'
    }
  },
  {
    path: 'stats',
    loadChildren: () => import('./stats/stats.module').then(m => m.StatsModule),
    data: {
      name: 'Stats'
    }
  },
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule { }
