import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatNativeDateModule } from '@angular/material/core';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { AngularMaterialModule } from './angular-material/angular-material-module';
import { LoggingModule } from './logging/logging.module';
import { MessagePopupComponent } from './message-popup/message-popup.component';
import { MqttModule, IMqttServiceOptions } from 'ngx-mqtt';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MAT_MOMENT_DATE_ADAPTER_OPTIONS, MatMomentDateModule } from '@angular/material-moment-adapter';
import { environment } from '../environments/environment';
import { ProgressSpinnerComponent } from './progress-spinner/progress-spinner.component';

export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: environment.mqttHost,
  port: environment.mqttPort,
  protocol: 'ws',
  path: '/mqtt'
};

@NgModule({
  declarations: [
    AppComponent, MessagePopupComponent, ProgressSpinnerComponent
  ],
  entryComponents: [
    MessagePopupComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MatNativeDateModule,
    AngularMaterialModule,
    LoggingModule,
    MatDatepickerModule,
    MatMomentDateModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS)
  ],
  providers: [{ provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: { appearance: 'fill' } }, { provide: MAT_MOMENT_DATE_ADAPTER_OPTIONS, useValue: { useUtc: true } }],
  bootstrap: [AppComponent]
})
export class AppModule { }
