import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { LoggingService } from '../../logging/logging.service';
import { JsonReplayComponent } from '../../replay/json-replay/json-replay.component';
import { v4 as uuidv4 } from 'uuid';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { Trial } from '../../trial/trial';
import { IgnoreListItem, Replay } from '../../replay/replay';
import { TrialService } from '../../trial/trial.service';
import { ReplayService } from '../../replay/replay.service';
import { forkJoin } from 'rxjs';
import { map, tap } from 'rxjs/operators';

@Component({
  selector: 'app-create-replay',
  templateUrl: './create-replay.component.html',
  styleUrls: ['./create-replay.component.scss']
})
export class CreateReplayComponent implements OnInit {
  parents: Trial[] | Replay[] = [];
  trials: Trial[] = [];
  replays: Replay[] = [];
  replayParentTypes: string[] = ['TRIAL', 'REPLAY'];
  ignore_message_list: IgnoreListItem[] = [];
  ignore_source_list: string[] = [];
  ignore_topic_list: string[] = [];

  createReplayForm = this.formBuilder.group({
    replay_id: ['', Validators.required],
    replay_parent_id: ['', Validators.required],
    replay_parent_type: ['', Validators.required],
    date: ['', Validators.required],
    ignore_message_list_input: [''],
    ignore_source_list_input: [''],
    ignore_topic_list_input: [''],
    useMessageBus: [false]
  });

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  ignoreListPattern: RegExp = new RegExp(/.+ : .+/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<CreateReplayComponent>,
    public jsonDialog: MatDialog,
    private loggingService: LoggingService,
    private trialService: TrialService,
    private replayService: ReplayService,
    @Inject(MAT_DIALOG_DATA) public data: Replay) {
  }

  onCreateClick(): void {
    const dialogResult = this.createReplayForm.value;
    dialogResult.ignore_message_list = this.ignore_message_list;
    dialogResult.ignore_source_list = this.ignore_source_list;
    dialogResult.ignore_topic_list = this.ignore_topic_list;
    delete dialogResult.ignore_message_list_input;
    delete dialogResult.ignore_source_list_input;
    delete dialogResult.ignore_topic_list_input;
    console.log(JSON.stringify(dialogResult));
    this.dialogRef.close(dialogResult);
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.createReplayForm.patchValue({
      replay_id: uuidv4()
    });
  }

  replayParentTypeChanged(event) {
    this.createReplayForm.controls.replay_parent_id.reset('', {
      onlySelf: true
    });
    switch (event.value) {
      case 'TRIAL':
        this.parents = this.trials;
        break;
      case 'REPLAY':
        this.parents = this.replays;
        break;
      default:
        this.parents = [];
        break;
    }
  }

  openJsonReplayDialog(): void {
    const dialogResult = this.createReplayForm.value;
    dialogResult.ignore_message_list = this.ignore_message_list;
    dialogResult.ignore_source_list = this.ignore_source_list;
    dialogResult.ignore_topic_list = this.ignore_topic_list;

    delete dialogResult.useMessageBus;

    const jsonDialogRef = this.jsonDialog.open(JsonReplayComponent, {
      // width: '250px',
      data: JSON.stringify(dialogResult, null, 2),
      panelClass: 'full-width-2-dialog'
    });

    jsonDialogRef.afterClosed().subscribe(result => {
      if (result) {
        try {
          const replay = JSON.parse(result.json) as Replay;
          this.ignore_message_list = replay.ignore_message_list;
          this.ignore_source_list = replay.ignore_source_list;
          this.ignore_topic_list = replay.ignore_topic_list;
          this.createReplayForm.patchValue({
            replay_id: replay.replay_id,
            replay_parent_id: replay.replay_parent_id,
            replay_parent_type: replay.replay_parent_type,
            date: replay.date,
            ignore_message_list: replay.ignore_message_list,
            ignore_source_list: replay.ignore_source_list,
            ignore_topic_list: replay.ignore_topic_list
          });
        } catch (e) {
          this.log(e);
        }
      }
    });
  }

  toggleUseMessageBusChange(event: MatSlideToggleChange) {
    // if (event.checked) {
    //   this.createReplayForm.controls['replay_id'].reset('',{
    //     onlySelf: true
    //   });
    //   this.createReplayForm.controls['replay_id'].disable();
    // } else {
    //   this.createReplayForm.controls['replay_id'].enable();
    //   this.createReplayForm.controls['replay_id'].reset('',{
    //     onlySelf: true
    //   });
    // }
  }

  ngOnInit(): void {
    forkJoin(
      {
        trials: this.trialService.readTrials(),
        replays: this.replayService.readReplays()
      }).subscribe(({trials, replays}) => {
        this.trials = trials;
        this.replays = replays;
    });
  }

  compareFnParents(a1: any, a2: any): boolean {
    return a1 && a2 ? a1.id === a2.id : a1 === a2;
  }

  /** Log a CreateReplayComponent message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`CreateReplayComponent: ${message}`);
  }

  getDisplayName(parent: Trial | Replay): string {
    if ((parent as Trial).name) {
      const t = parent as Trial;
      return t.name;
    } else {
      const r = parent as Replay;
      return r.replay_id;
    }
  }

  onAddIgnoreMessageListItem(): void {
    if (this.createReplayForm.controls.ignore_message_list_input.value !== '') {
      const types = this.createReplayForm.controls.ignore_message_list_input.value.split(' : ');
      const ignoreListType = {
        message_type: types[0],
        sub_type: types[1]
      };
      this.ignore_message_list.push(ignoreListType);
      this.createReplayForm.controls.ignore_message_list_input.setValue('');
    }
  }

  onRemoveIgnoreMessageListItem(item: any): void {
    const index: number = this.ignore_message_list.findIndex(i => i.message_type === item.message_type && i.sub_type === item.sub_type);
    if (index > -1) {
      this.ignore_message_list.splice(index, 1);
    }
  }

  onAddIgnoreSourceListItem(): void {
    if (this.createReplayForm.controls.ignore_source_list_input.value !== '') {
      this.ignore_source_list.push(this.createReplayForm.controls.ignore_source_list_input.value);
      this.createReplayForm.controls.ignore_source_list_input.setValue('');
    }
  }

  onRemoveIgnoreSourceListItem(source: any): void {
    const index: number = this.ignore_source_list.findIndex(s => s === source);
    if (index > -1) {
      this.ignore_source_list.splice(index, 1);
    }
  }

  onAddIgnoreTopicListItem(): void {
    if (this.createReplayForm.controls.ignore_topic_list_input.value !== '') {
      this.ignore_topic_list.push(this.createReplayForm.controls.ignore_topic_list_input.value);
      this.createReplayForm.controls.ignore_topic_list_input.setValue('');
    }
  }

  onRemoveIgnoreTopicListItem(topic: any): void {
    const index: number = this.ignore_topic_list.findIndex(t => t === topic);
    if (index > -1) {
      this.ignore_topic_list.splice(index, 1);
    }
  }

}
