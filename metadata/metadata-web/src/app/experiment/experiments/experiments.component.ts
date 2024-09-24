import {Component, OnInit, OnDestroy, ViewChild} from '@angular/core';

import { Experiment } from '../experiment';
import { ExperimentMessage } from '../experiment-message';
import { ExperimentService } from '../experiment.service';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { Subscription } from 'rxjs';
import { MediaObserver, MediaChange } from '@angular/flex-layout';
import { CreateExperimentComponent } from '../create-experiment/create-experiment.component';
import { UpdateExperimentComponent } from '../update-experiment/update-experiment.component';
import { DeleteExperimentComponent } from '../delete-experiment/delete-experiment.component';
import { MatDialog } from '@angular/material/dialog';
import { LoggingService } from '../../logging/logging.service';
import { Overlay, OverlayRef } from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';
import { filter, map } from 'rxjs/operators';
import { ProgressSpinnerComponent } from '../../progress-spinner/progress-spinner.component';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-experiments',
  templateUrl: './experiments.component.html',
  styleUrls: ['./experiments.component.scss']
})
export class ExperimentsComponent implements OnInit, OnDestroy {
  experiments: Experiment[];
  displayedColumns: string[];
  dataSource = new MatTableDataSource(this.experiments);
  overlayRef: OverlayRef;
  private experimentCreatedSubscription: Subscription;

  currentScreenWidth = '';
  flexMediaWatcher: Subscription;

  @ViewChild(MatTable) table: MatTable<Experiment>;
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor(
    private experimentService: ExperimentService,
    private mediaObserver: MediaObserver,
    public createDialog: MatDialog,
    public updateDialog: MatDialog,
    public deleteDialog: MatDialog,
    private loggingService: LoggingService,
    private overlay: Overlay,
    private mqttService: MqttService
  ) {

    this.experimentCreatedSubscription = this.mqttService.observe('metadata/experiment/created').subscribe((message: IMqttMessage) => {
      const json = new TextDecoder('utf-8').decode(message.payload);
      // let experiment = <Experiment>JSON.parse(json);
      this.log('Experiment created: ' + json);
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
    this.experimentCreatedSubscription.unsubscribe();
  }

  setupTable() {
    this.displayedColumns = ['id', 'experiment_id', 'name', 'date', 'author', 'mission', 'actions'];
    if (this.currentScreenWidth === 'xs') {
      this.displayedColumns = ['name', 'mission', 'actions'];
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

  create(experiment: Experiment): void {
    if (!experiment) { return; }
    this.experimentService.createExperiment(experiment)
      .subscribe(e => {
        if (e) {
          this.log(`Experiment has been created: ${e.id}`);
          this.experiments.push(e);

          this.dataSource.data = this.experiments;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  createMessage(experiment: ExperimentMessage): void {
    if (!experiment) { return; }
    this.experimentService.createExperimentMessage(experiment)
      .subscribe(_ => {
        // this.log(`Experiment message has been created using message bus.`);
        // this.showOverlay();
      });
    // this.table.renderRows();
  }

  read(): void {
    this.experimentService.readExperiments()
      .subscribe(experiments => {
        this.experiments = experiments;
        this.dataSource = new MatTableDataSource(this.experiments);
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
      });
  }

  update(index: number, experiment: Experiment): void {
    if (!experiment) { return; }
    if (!experiment.id) { return; }
    this.experimentService.updateExperiment(experiment)
      .subscribe(e => {
        if (e) {
          this.log(`Experiment has been updated: ${e.id}`);
          this.experiments[index] = e;

          this.dataSource.data = this.experiments;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  delete(index: number,  experiment: Experiment): void {
    if (!experiment) { return; }
    this.experimentService.deleteExperiment(experiment.id)
      .subscribe(success => {
        if (success) {
          this.log(`Experiment has been deleted: ${experiment.id}`);
          this.dataSource.data.splice(index, 1);

          this.dataSource.data = this.experiments;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  openCreateExperimentDialog(): void {
    const dialogRef = this.createDialog.open(CreateExperimentComponent, {
      // width: '250px',
      // data: {name: this.name, animal: this.animal}
      panelClass: 'full-width-1-dialog'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      if (result.useMessageBus) {
        const experimentMessage = this.experimentService.generateExperimentMessage(result, 'experiment', 'create', 'metadata-web', environment.testbedVersion);
        this.createMessage(experimentMessage);
      } else {
        const experiment = {
          id: -1,
          experiment_id: result.experiment_id,
          name: result.name,
          date: result.date,
          author: result.author,
          mission: result.mission
        };
        this.create(experiment);
      }
    });
  }

  openUpdateExperimentDialog(index: number, id: number, experiment_id: string, name: string, date: string, author: string, mission: string) {
    const dialogRef = this.updateDialog.open(UpdateExperimentComponent, {
      data: { id, experiment_id, name, date, author, mission }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) { return; }
      this.update(index, result);
    });
  }

  openDeleteExperimentDialog(index: number, id: number, experiment_id: string, name: string, date: string, author: string, mission: string) {
    const dialogRef = this.deleteDialog.open(DeleteExperimentComponent, {
      data: { id, experiment_id, name, date, author, mission }
    });

    dialogRef.afterClosed().subscribe(result => {
      this.delete(index, result);
    });
  }

  private log(message: string) {
    this.loggingService.add(`ExperimentComponent: ${message}`);
  }
}
