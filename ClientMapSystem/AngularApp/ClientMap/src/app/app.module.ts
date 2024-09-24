import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { SocketIoModule} from 'ngx-socket-io';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ActionDialogComponent } from './action-dialog/action-dialog.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { MapComponent } from './map/map.component';
import { InteractionPaneComponent } from './interaction-pane/interaction-pane.component';
import { MapParentComponent } from './map-parent/map-parent.component';
import { SurveyComponent } from './survey/survey.component';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AudioWebsocketService } from './Services/audiowebsocket.service';
import { OrderByPipe } from './shared/pipes/order-by.pipe';
import { HumanAdvisorComponent } from './human-advisor/human-advisor.component'
import { WebsocketService } from './websocket.service';
import {MatSelectModule} from '@angular/material/select';
import {MatFormFieldModule} from '@angular/material/form-field';
import { MatGridListModule } from '@angular/material/grid-list';
import { SessionService } from './Services/session.service';


@NgModule({
  declarations: [
    AppComponent,
    ActionDialogComponent,
    LoginComponent,
    MapComponent,
    InteractionPaneComponent,
    MapParentComponent,
    SurveyComponent,
    OrderByPipe,
    HumanAdvisorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    // DEBUG
    //SocketIoModule.forRoot({ url: 'ws://' + environment.wspath + ':3080', options: { transports: ['websocket'], allowUpgrades : true } }),
    // PROD
    SocketIoModule.forRoot({ url: 'wss://' + document.location.host , options: { transports: ['websocket'], allowUpgrades : true, path: '/ClientMap/socket.io' } }),
    BrowserAnimationsModule,
    MatDialogModule,
    MatCardModule,
    FormsModule,
    MatCheckboxModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatMenuModule,
    HttpClientModule,
    FlexLayoutModule,
    MatIconModule,   
    MatFormFieldModule,
    MatSelectModule,
    MatGridListModule,
  ],
  providers: [
    AudioWebsocketService,
    WebsocketService,
    SessionService
  ],
  entryComponents:[ActionDialogComponent],
  bootstrap: [AppComponent]
  
})
export class AppModule { 

  
}
