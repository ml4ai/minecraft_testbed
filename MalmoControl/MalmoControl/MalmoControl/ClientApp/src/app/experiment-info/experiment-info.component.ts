import { Component, OnInit, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ExperimentDTO, TrialDTO } from '../Interface/DTO';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ExperimentDialogComponent } from '../experiment-dialog/experiment-dialog.component';
import { ExperimentService } from '../Services/experiment.service';

@Component({
  selector: 'app-experiment-info',
  templateUrl: './experiment-info.component.html',
  styleUrls: ['./experiment-info.component.css']
})
export class ExperimentInfoComponent implements OnInit {

  public baseUrl: string;
  
  trialDTO: TrialDTO | string = 'Trial Not Started';
  experimentDTO: ExperimentDTO;

  experimentService;

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string, public dialog: MatDialog, 
  experimentService: ExperimentService ) {

    this.baseUrl = baseUrl;
    this.experimentService = experimentService;
  }

  ngOnInit() {

  }
 
}
