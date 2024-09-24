import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoggingComponent } from './logging/logging.component';
import { BottomSheetContainerComponent, BottomSheetContainerSheet } from './bottom-sheet-container/bottom-sheet-container.component';
import { AngularMaterialModule } from '../angular-material/angular-material-module';

@NgModule({
  declarations: [LoggingComponent, BottomSheetContainerComponent, BottomSheetContainerSheet],
  exports: [
    LoggingComponent,
    BottomSheetContainerComponent
  ],
  imports: [
    CommonModule,
    AngularMaterialModule
  ],
})
export class LoggingModule { }
