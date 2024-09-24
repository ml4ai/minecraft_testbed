import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ExportTrialComponent } from './export-trial/export-trial.component';
import { ExportReplayComponent } from './export-replay/export-replay.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { HealthStatusComponent } from './health-status/health-status.component';
import { MetadataAppStatusComponent } from './metadata-app/metadata-app-status/metadata-app-status.component';
import { ImportTrialComponent } from './import-trial/import-trial.component';
import { MaterialFileInputModule } from 'ngx-material-file-input';
import { ImportReplayComponent } from './import-replay/import-replay.component';
import { RunReplayComponent } from './run-replay/run-replay.component';
import { IMaskModule } from 'angular-imask';
import { ExportTimeWindowComponent } from './export-time-window/export-time-window.component';
import { IConfig, NgxMaskModule } from 'ngx-mask';
import { BatchRunReplayComponent } from './batch-run-replay/batch-run-replay.component';
import { JsonDialogComponent } from './json-dialog/json-dialog.component';

export const options: Partial<IConfig> | (() => Partial<IConfig>) = null;

@NgModule({
  declarations: [DashboardComponent, ExportTrialComponent, ExportReplayComponent, HealthStatusComponent, MetadataAppStatusComponent, ImportTrialComponent, ImportReplayComponent, RunReplayComponent, ExportTimeWindowComponent, BatchRunReplayComponent, JsonDialogComponent],
  exports: [
    HealthStatusComponent
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    ReactiveFormsModule,
    MatSelectModule,
    AngularMaterialModule,
    MaterialFileInputModule,
    FormsModule,
    IMaskModule,
    NgxMaskModule.forRoot(options)
  ]
})
export class DashboardModule { }
