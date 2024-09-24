import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatsComponent } from './stats/stats.component';
import { StatsRoutingModule } from '../stats/stats-routing.module';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { FirstLookComponent } from './first-look/first-look.component';
import { ReactiveFormsModule } from '@angular/forms';



@NgModule({
  declarations: [StatsComponent, FirstLookComponent],
  imports: [
    CommonModule,
    StatsRoutingModule,
    AngularMaterialModule,
    ReactiveFormsModule
  ]
})
export class StatsModule { }
