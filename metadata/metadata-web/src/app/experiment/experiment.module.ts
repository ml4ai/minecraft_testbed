import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExperimentRoutingModule } from './experiment-routing.module';
import { ExperimentsComponent } from './experiments/experiments.component';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { ReactiveFormsModule } from '@angular/forms';
import { CreateExperimentComponent } from './create-experiment/create-experiment.component';
import { UpdateExperimentComponent } from './update-experiment/update-experiment.component';
import { DeleteExperimentComponent } from './delete-experiment/delete-experiment.component';
import { OverlayModule } from '@angular/cdk/overlay';
import { JsonExperimentComponent } from './json-experiment/json-experiment.component';

@NgModule({
  declarations: [ExperimentsComponent, CreateExperimentComponent, UpdateExperimentComponent, DeleteExperimentComponent, JsonExperimentComponent],
  imports: [
    CommonModule,
    ExperimentRoutingModule,
    AngularMaterialModule,
    ReactiveFormsModule,
    OverlayModule
  ]
})
export class ExperimentModule { }
