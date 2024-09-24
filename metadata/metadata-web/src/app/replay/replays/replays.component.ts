import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import {IgnoreListItem, Replay} from '../../replay/replay';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { Overlay, OverlayRef } from '@angular/cdk/overlay';
import { Subscription } from 'rxjs';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { ReplayService } from '../../replay/replay.service';
import { MediaChange, MediaObserver } from '@angular/flex-layout';
import { MatDialog } from '@angular/material/dialog';
import { LoggingService } from '../../logging/logging.service';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { filter, map } from 'rxjs/operators';
import { ComponentPortal } from '@angular/cdk/portal';
import { ProgressSpinnerComponent } from '../../progress-spinner/progress-spinner.component';
import { ReplayMessage } from '../replay-message';
import { CreateReplayComponent } from '../../replay/create-replay/create-replay.component';
import { UpdateReplayComponent } from '../../replay/update-replay/update-replay.component';
import { DeleteReplayComponent } from '../../replay/delete-replay/delete-replay.component';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-replays',
  templateUrl: './replays.component.html',
  styleUrls: ['./replays.component.scss']
})
export class ReplaysComponent implements OnInit, OnDestroy {
  replays: Replay[];
  displayedColumns: string[];
  dataSource = new MatTableDataSource(this.replays);
  overlayRef: OverlayRef;
  private replayCreatedSubscription: Subscription;

  currentScreenWidth = '';
  flexMediaWatcher: Subscription;

  @ViewChild(MatTable) table: MatTable<Replay>;
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor(
    private replayService: ReplayService,
    private mediaObserver: MediaObserver,
    public createDialog: MatDialog,
    public updateDialog: MatDialog,
    public deleteDialog: MatDialog,
    private loggingService: LoggingService,
    private overlay: Overlay,
    private mqttService: MqttService
  ) {

    this.replayCreatedSubscription = this.mqttService.observe('metadata/replay/created').subscribe((message: IMqttMessage) => {
      const json = new TextDecoder('utf-8').decode(message.payload);
      // let replay = <Replay>JSON.parse(json);
      this.log('Replay created: ' + json);
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
    this.replayCreatedSubscription.unsubscribe();
  }

  setupTable() {
    this.displayedColumns = ['id', 'replay_id', 'replay_parent_id', 'replay_parent_type', 'date', 'ignore_message_list', 'ignore_source_list', 'ignore_topic_list', 'actions'];
    if (this.currentScreenWidth === 'xs') {
      this.displayedColumns = ['replay_id', 'replay_parent_id', 'replay_parent_type'];
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

  create(replay: Replay): void {
    if (!replay) { return; }
    this.replayService.createReplay(replay)
      .subscribe(e => {
        if (e) {
          this.log(`Replay has been created: ${e.id}`);
          this.replays.push(e);

          this.dataSource.data = this.replays;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  createMessage(replay: ReplayMessage): void {
    if (!replay) { return; }
    this.replayService.createReplayMessage(replay)
      .subscribe(_ => {
        // this.log(`Replay message has been created using message bus.`);
        // this.showOverlay();
      });
    // this.table.renderRows();
  }

  read(): void {
    this.replayService.readReplays()
      .subscribe(replays => {
        this.replays = replays;
        this.dataSource = new MatTableDataSource(this.replays);
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
      });
  }

  update(index: number, replay: Replay): void {
    if (!replay) { return; }
    if (!replay.id) { return; }
    this.replayService.updateReplay(replay)
      .subscribe(e => {
        if (e) {
          this.log(`Replay has been updated: ${e.id}`);
          this.replays[index] = e;

          this.dataSource.data = this.replays;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  delete(index: number,  replay: Replay): void {
    if (!replay) { return; }
    this.replayService.deleteReplay(replay.id)
      .subscribe(success => {
        if (success) {
          this.log(`Replay has been deleted: ${replay.id}`);
          this.dataSource.data.splice(index, 1);

          this.dataSource.data = this.replays;
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
        }
      });
    this.table.renderRows();
  }

  openCreateReplayDialog(): void {
    const dialogRef = this.createDialog.open(CreateReplayComponent, {
      // width: '250px',
      // data: {name: this.name, animal: this.animal}
      panelClass: 'full-width-1-dialog'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      const parent_replay_id = result.replay_parent_type === 'TRIAL' ? result.replay_parent_id.trial_id : result.replay_parent_id.replay_id;
      if (result.useMessageBus) {
        const replay_message = this.replayService.generateReplayMessage('', '', parent_replay_id, result.replay_parent_type, result.ignore_message_list, result.ignore_source_list, result.ignore_topic_list, 'create', 'metadata-web', environment.testbedVersion);
        this.createMessage(replay_message);
      } else {
        const replay = {
          id: -1,
          replay_id: result.replay_id,
          replay_parent_id: parent_replay_id,
          replay_parent_type: result.replay_parent_type,
          date: result.date,
          ignore_message_list: result.ignore_message_list,
          ignore_source_list: result.ignore_source_list,
          ignore_topic_list: result.ignore_topic_list
        };
        this.create(replay);
      }
    });
  }

  openUpdateReplayDialog(index: number, id: number, replay_id: string, replay_parent_id: string, replay_parent_type: string, date: string, ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[]) {
    const dialogRef = this.updateDialog.open(UpdateReplayComponent, {
      data: { id, replay_id, replay_parent_id, replay_parent_type, date, ignore_message_list, ignore_source_list, ignore_topic_list }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) { return; }
      const parent_replay_id = result.replay_parent_type === 'TRIAL' ? result.replay_parent_id.trial_id : result.replay_parent_id.replay_id;
      result.replay_parent_id = parent_replay_id;
      this.update(index, result);
    });
  }

  openDeleteReplayDialog(index: number, id: number, replay_id: string, replay_parent_id: string, replay_parent_type: string, date: string, ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[]) {
    const dialogRef = this.deleteDialog.open(DeleteReplayComponent, {
      data: { id, replay_id, replay_parent_id, replay_parent_type, date, ignore_message_list, ignore_source_list, ignore_topic_list }
    });

    dialogRef.afterClosed().subscribe(result => {
      this.delete(index, result);
    });
  }

  private log(message: string) {
    this.loggingService.add(`ReplayComponent: ${message}`);
  }
}
