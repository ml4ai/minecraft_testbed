import {Component, OnInit, OnDestroy, ViewChild} from '@angular/core';

import { Trial } from '../trial';
import { TrialMessage } from '../trial-message';
import { TrialService } from '../trial.service';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { Subscription } from 'rxjs';
import { MediaObserver, MediaChange } from '@angular/flex-layout';
import { CreateTrialComponent } from '../create-trial/create-trial.component';
import { UpdateTrialComponent } from '../update-trial/update-trial.component';
import { DeleteTrialComponent } from '../delete-trial/delete-trial.component';
import { MatDialog } from '@angular/material/dialog';
import { LoggingService } from '../../logging/logging.service';
import { Experiment } from '../../experiment/experiment';
import { environment } from '../../../environments/environment';
import { ComponentPortal } from '@angular/cdk/portal';
import { ProgressSpinnerComponent } from '../../progress-spinner/progress-spinner.component';
import { ExperimentMessage } from '../../experiment/experiment-message';
import { Overlay, OverlayRef } from '@angular/cdk/overlay';
import { filter, map } from 'rxjs/operators';
import { IMqttMessage, MqttService } from 'ngx-mqtt';

@Component({
  selector: 'app-trials',
  templateUrl: './trials.component.html',
  styleUrls: ['./trials.component.scss']
})
export class TrialsComponent implements OnInit, OnDestroy {
  trials: Trial[];
  displayedColumns: string[];
  dataSource = new MatTableDataSource(this.trials);
  overlayRef: OverlayRef;
  private trialCreatedSubscription: Subscription;

  currentScreenWidth = '';
  flexMediaWatcher: Subscription;

  @ViewChild(MatTable) table: MatTable<Trial>;
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor(
    private trialService: TrialService,
    private mediaObserver: MediaObserver,
    public createDialog: MatDialog,
    public updateDialog: MatDialog,
    public deleteDialog: MatDialog,
    private loggingService: LoggingService,
    private overlay: Overlay,
    private mqttService: MqttService
  ) {

    this.trialCreatedSubscription = this.mqttService.observe('metadata/trial/created').subscribe((message: IMqttMessage) => {
      const json = new TextDecoder('utf-8').decode(message.payload);
      // let trial = <Trial>JSON.parse(json);
      this.log('Trial created: ' + json);
      this.read();
    });

    // this.flexMediaWatcher = mediaObserver.media$.subscribe((change: MediaChange) => {
    //   if (change.mqAlias !== this.currentScreenWidth) {
    //     this.currentScreenWidth = change.mqAlias;
    //     this.setupTable();
    //   }
    // });

    this.overlayRef = this.overlay.create({
      positionStrategy: this.overlay.position().global().centerHorizontally().centerVertically(),
      hasBackdrop: true
    });

    this.flexMediaWatcher = mediaObserver.asObservable()
      .pipe(
        filter((changes: MediaChange[]) => changes.length > 0),
        map((changes: MediaChange[]) => changes[0])
      ).subscribe((change: MediaChange) => {
        if (change.mqAlias !== this.currentScreenWidth) {
          this.currentScreenWidth = change.mqAlias;
          this.setupTable();
        }
      });
  }

  ngOnInit(): void {
    this.read();
  }

  ngOnDestroy(): void {
    this.flexMediaWatcher.unsubscribe();
    this.trialCreatedSubscription.unsubscribe();
  }

  setupTable() {
    this.displayedColumns = ['id', 'trial_id', 'name', 'date', 'experimenter', 'subjects', 'trial_number', 'group_number', 'study_number', 'condition', 'notes', 'testbed_version', 'experiment_id_experiments', 'actions'];
    if (this.currentScreenWidth === 'xs') {
      this.displayedColumns = ['name', 'experiment_id_experiments', 'actions'];
    }
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  showOverlay() {
    this.overlayRef.attach(new ComponentPortal(ProgressSpinnerComponent));
    setTimeout(() => {
      this.overlayRef.detach();
      this.read();
    }, 3000);
  }

  create(trial: Trial): void {
    if (!trial) { return; }
    this.trialService.createTrial(trial)
      .subscribe(t => {
        if (t) {
          this.log(`Trial has been created: ${t.id}`);
          this.trials.push(t);

          this.dataSource.data = this.trials;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  createMessage(trial: TrialMessage): void {
    if (!trial) { return; }
    this.trialService.createTrialMessage(trial)
      .subscribe(_ => {
        // this.log(`Trial message has been created using message bus.`);
        // this.showOverlay();
      });
    // this.table.renderRows();
  }

  read(): void {
    this.trialService.readTrials()
      .subscribe(trials => {
        this.trials = trials;
        this.dataSource = new MatTableDataSource(this.trials);
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
      });
  }

  update(index: number, trial: Trial): void {
    if (!trial) { return; }
    if (!trial.id) { return; }
    this.trialService.updateTrial(trial)
      .subscribe(t => {
        if (t) {
          this.log(`Trial has been updated: ${t.id}`);
          this.trials[index] = t;

          this.dataSource.data = this.trials;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  delete(index: number,  trial: Trial): void {
    if (!trial) { return; }
    this.trialService.deleteTrial(trial.id)
      .subscribe(success => {
        if (success) {
          this.log(`Trial has been deleted: ${trial.id}`);
          this.dataSource.data.splice(index, 1);

          this.dataSource.data = this.trials;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  openCreateTrialDialog(): void {
    // const dialogRef = this.createDialog.open(CreateTrialComponent, {
    //   // width: '250px',
    //   // data: {name: this.name, animal: this.animal}
    // });
    //
    // dialogRef.afterClosed().subscribe(result => {
    //   this.create(result);
    // });
    const dialogRef = this.createDialog.open(CreateTrialComponent, {
      // width: '250px',
      // data: {name: this.name, animal: this.animal}
      panelClass: 'full-width-1-dialog'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      if (result.useMessageBus) {
        const trialMessage = this.trialService.generateTrialMessage(result, 'create', 'metadata-web', environment.testbedVersion, null, null, null);
        this.createMessage(trialMessage);
      } else {
        const trial = {
          id: -1,
          trial_id: result.trial_id,
          name: result.name,
          date: result.date,
          experimenter: result.experimenter,
          subjects: result.subjects,
          trial_number: result.trial_number,
          group_number: result.group_number,
          study_number: result.study_number,
          condition: result.condition,
          notes: result.notes,
          testbed_version: result.testbed_version,
          experiment: result.experiment
        };
        this.create(trial);
      }
    });
  }

  openUpdateTrialDialog(index: number, id: number, trial_id: string, name: string, date: string, experimenter: string, subjects: string[], trial_number: string, group_number: string, study_number: string, condition: string, notes: string[], testbed_version: string, experiment: Experiment) {
    const dialogRef = this.updateDialog.open(UpdateTrialComponent, {
      data: {
        id,
        trial_id,
        name,
        date,
        experimenter,
        subjects,
        trial_number,
        group_number,
        study_number,
        condition,
        notes,
        testbed_version,
        experiment
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) { return; }
      this.update(index, result);
    });
  }

  openDeleteTrialDialog(index: number, id: number, trial_id: string, name: string, date: string, experimenter: string, subjects: string[], trial_number: string, group_number: string, study_number: string, condition: string, notes: string[], testbed_version: string, experiment: Experiment) {
    const dialogRef = this.deleteDialog.open(DeleteTrialComponent, {
      data: {
        id,
        trial_id,
        name,
        date,
        experimenter,
        trial_number,
        group_number,
        study_number,
        condition,
        subjects,
        notes,
        testbed_version,
        experiment }
    });

    dialogRef.afterClosed().subscribe(result => {
      this.delete(index, result);
    });
  }

  private log(message: string) {
    this.loggingService.add(`TrialComponent: ${message}`);
  }
}
