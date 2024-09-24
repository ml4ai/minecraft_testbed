import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReplayRoutingModule } from './replay-routing.module';
import { ReplaysComponent } from './replays/replays.component';
import { AngularMaterialModule } from '../angular-material/angular-material-module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CreateReplayComponent } from './create-replay/create-replay.component';
import { UpdateReplayComponent } from './update-replay/update-replay.component';
import { DeleteReplayComponent } from './delete-replay/delete-replay.component';
import { OverlayModule } from '@angular/cdk/overlay';
import { JsonReplayComponent } from './json-replay/json-replay.component';

@NgModule({
  declarations: [ReplaysComponent, CreateReplayComponent, UpdateReplayComponent, DeleteReplayComponent, JsonReplayComponent],
  imports: [
    CommonModule,
    ReplayRoutingModule,
    AngularMaterialModule,
    ReactiveFormsModule,
    OverlayModule,
    FormsModule
  ]
})
export class ReplayModule { }
