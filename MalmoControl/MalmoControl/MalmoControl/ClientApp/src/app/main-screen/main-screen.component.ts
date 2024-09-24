import { Component } from '@angular/core';
import { ExperimentService } from '../Services/experiment.service';

@Component({
  selector: 'app-main-screen',
  templateUrl: './main-screen.component.html',
  styleUrls: ['./main-screen.component.css']
})
export class MainScreenComponent  {


  constructor(public experimentService: ExperimentService) { }

 

}
