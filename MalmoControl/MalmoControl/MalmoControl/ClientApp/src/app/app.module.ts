import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import {CommonModule} from '@angular/common';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppComponent } from './app.component';
import { NavMenuComponent } from './nav-menu/nav-menu.component';



import { FetchPortsComponent } from './fetch-ports/fetch-ports.component';
import { MissionRunnerComponent } from './mission-runner/mission-runner.component';
import { MalmoStatusComponent } from './malmo-status/malmo-status.component';
import { PortOutComponent } from './port-out/port-out.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner'
import { MatProgressBarModule } from '@angular/material/progress-bar'
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule, MatIcon } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatSelectModule } from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTabsModule } from '@angular/material/tabs';
import {MatTableModule} from '@angular/material/table';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { AgGridModule } from 'ag-grid-angular';
import { AboutDialogComponent } from './about-dialog/about-dialog.component';
import {MatTooltipModule} from '@angular/material/tooltip';
import { TitleBarComponent } from './title-bar/title-bar.component';
import { ReferenceAgentComponent } from './reference-agent/reference-agent.component';
import { ExperimentInfoComponent } from './experiment-info/experiment-info.component';
import { ExperimentDialogComponent } from './experiment-dialog/experiment-dialog.component';
import { HelpDialogComponent } from './help-dialog/help-dialog.component';
import { MainScreenComponent } from './main-screen/main-screen.component';
import { AppRoutingModule } from './app-routing.module';
import { ErrorViewerComponent } from './error-viewer/error-viewer.component';
import { TestbedLauncherComponent } from './testbed-launcher/testbed-launcher.component';
import { ClientInfoComponent } from './client-info/client-info.component';
import { ObserverInfoComponent } from './observer-info/observer-info.component';
import { ContainerDetailsDialogComponent } from './container-details-dialog/container-details-dialog.component';
import { AgentControlComponent } from './agent-control/agent-control.component';

@NgModule({
  declarations: [
    AppComponent,
    NavMenuComponent,
    FetchPortsComponent,
    MissionRunnerComponent,
    MalmoStatusComponent,
    PortOutComponent,
    AboutDialogComponent,
    TitleBarComponent,
    ReferenceAgentComponent,
    ExperimentInfoComponent,
    ExperimentDialogComponent,
    HelpDialogComponent,
    MainScreenComponent,
    ErrorViewerComponent,
    TestbedLauncherComponent,
    ClientInfoComponent,
    ObserverInfoComponent,
    ContainerDetailsDialogComponent,
    AgentControlComponent
  ],
  imports: [
    CommonModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatSelectModule,
    MatIconModule,
    MatButtonModule,
    MatCheckboxModule,
    MatDialogModule,
    MatRadioModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatTableModule,
    AgGridModule.withComponents([]),
    ScrollingModule,
    MatTabsModule,
    MatListModule,
    BrowserAnimationsModule,
    BrowserModule.withServerTransition({ appId: 'ng-cli-universal' }),
    HttpClientModule,
    FormsModule,
    FlexLayoutModule,
    AppRoutingModule,
    MatTooltipModule
  ],
  providers: [],
  entryComponents: [ExperimentDialogComponent, AboutDialogComponent, HelpDialogComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
