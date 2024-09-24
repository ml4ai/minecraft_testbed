import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Experiment } from '../experiment';
import { v4 as uuidv4 } from 'uuid';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { JsonExperimentComponent } from '../json-experiment/json-experiment.component';
import { LoggingService } from '../../logging/logging.service';

@Component({
  selector: 'app-create-experiment',
  templateUrl: './create-experiment.component.html',
  styleUrls: ['./create-experiment.component.scss']
})
export class CreateExperimentComponent implements OnInit {

  createExperimentForm = this.formBuilder.group({
    experiment_id: ['', Validators.required],
    name: ['', Validators.required],
    date: ['', Validators.required],
    author: ['', Validators.required],
    mission: ['', Validators.required],
    useMessageBus: [false]
  });
  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<CreateExperimentComponent>,
    public jsonDialog: MatDialog,
    private loggingService: LoggingService,
    @Inject(MAT_DIALOG_DATA) public data: Experiment) {
  }

  onCreateClick(): void {
    this.dialogRef.close(this.createExperimentForm.value);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.createExperimentForm.patchValue({
      experiment_id: uuidv4()
    });
  }

  openJsonExperimentDialog(): void {
    const dialogResult = this.createExperimentForm.value;

    delete dialogResult.useMessageBus;

    const jsonDialogRef = this.jsonDialog.open(JsonExperimentComponent, {
      // width: '250px',
      data: JSON.stringify(dialogResult, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const experiment = JSON.parse(result.json) as Experiment;
          this.createExperimentForm.patchValue({
            experiment_id: experiment.experiment_id,
            name: experiment.name,
            date: experiment.date,
            author: experiment.author,
            mission: experiment.mission
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  toggleUseMessageBusChange(event: MatSlideToggleChange) {
    // if (event.checked) {
    //   this.createExperimentForm.controls['experiment_id'].reset('',{
    //     onlySelf: true
    //   });
    //   this.createExperimentForm.controls['experiment_id'].disable();
    // } else {
    //   this.createExperimentForm.controls['experiment_id'].enable();
    //   this.createExperimentForm.controls['experiment_id'].reset('',{
    //     onlySelf: true
    //   });
    // }
  }

  ngOnInit(): void {
  }

  /** Log a CreateExperimentComponent message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`CreateExperimentComponent: ${message}`);
  }
}
