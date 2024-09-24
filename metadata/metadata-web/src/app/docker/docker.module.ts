import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DockerComponent } from './docker/docker.component';
import { DockerRoutingModule } from './docker-routing.module';
import { DashboardModule } from '../dashboard/dashboard.module';
import { ExtendedModule, FlexModule } from '@angular/flex-layout';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [DockerComponent],
  imports: [
    CommonModule,
    DockerRoutingModule,
    AngularMaterialModule,
    DashboardModule,
    ExtendedModule,
    FlexModule,
    FormsModule,
  ]
})
export class DockerModule { }
