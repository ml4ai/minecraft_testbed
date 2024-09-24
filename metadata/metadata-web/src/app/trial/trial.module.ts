import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TrialRoutingModule } from './trial-routing.module';
import { TrialsComponent } from './trials/trials.component';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { ReactiveFormsModule } from '@angular/forms';
import { CreateTrialComponent } from './create-trial/create-trial.component';
import { UpdateTrialComponent } from './update-trial/update-trial.component';
import { DeleteTrialComponent } from './delete-trial/delete-trial.component';
import { JsonTrialComponent } from './json-trial/json-trial.component';



@NgModule({
  declarations: [TrialsComponent, CreateTrialComponent, UpdateTrialComponent, DeleteTrialComponent, JsonTrialComponent],
  imports: [
    CommonModule,
    TrialRoutingModule,
    AngularMaterialModule,
    ReactiveFormsModule
  ]
})
export class TrialModule { }
