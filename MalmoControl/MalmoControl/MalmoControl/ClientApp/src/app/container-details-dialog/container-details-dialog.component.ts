import { Component, Inject, OnInit } from '@angular/core';
import { AgentContainer } from '../Services/experiment.service';
import { MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-container-details-dialog',
  templateUrl: './container-details-dialog.component.html',
  styleUrls: ['./container-details-dialog.component.css']
})
export class ContainerDetailsDialogComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: AgentContainer[]) { }

  ngOnInit(): void {
  }

  sortBy(prop: string) {
    return this.data.sort((a, b) => a[prop] > b[prop] ? 1 : a[prop] === b[prop] ? 0 : -1);
  }

  getStatusColor(container: AgentContainer): string{
    let currentDate = new Date();
    if (currentDate.getTime() - container.lastUpdate.getTime() < 60000) {
      return 'good-status'
    }
    else if (currentDate.getTime() - container.lastUpdate.getTime() < 300000) {
      return 'ok-status'
    }
    else {
      return 'not-ok-status'
    }

  }

}
