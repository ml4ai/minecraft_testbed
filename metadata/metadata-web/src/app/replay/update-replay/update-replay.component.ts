import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { v4 as uuidv4 } from 'uuid';
import {IgnoreListItem, Replay} from '../../replay/replay';
import { forkJoin} from 'rxjs';
import { Trial } from '../../trial/trial';
import { TrialService } from '../../trial/trial.service';
import { ReplayService } from '../replay.service';
import { LoggingService } from '../../logging/logging.service';

@Component({
  selector: 'app-update-replay',
  templateUrl: './update-replay.component.html',
  styleUrls: ['./update-replay.component.scss']
})
export class UpdateReplayComponent implements OnInit {
  parents: Trial[] | Replay[];
  trials: Trial[];
  replays: Replay[];
  replayParentTypes: string[] = ['TRIAL', 'REPLAY'];
  ignore_message_list: IgnoreListItem[] = [];
  ignore_source_list: string[] = [];
  ignore_topic_list: string[] = [];

  updateReplayForm = this.formBuilder.group({
    id: ['', Validators.required],
    replay_id: ['', Validators.required],
    replay_parent_id: ['', Validators.required],
    replay_parent_type: ['', Validators.required],
    date: ['', Validators.required],
    ignore_message_list_input: [''],
    ignore_source_list_input: [''],
    ignore_topic_list_input: [''],
  });

  uuidPattern: RegExp = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  ignoreListPattern: RegExp = new RegExp(/.+ : .+/);

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<UpdateReplayComponent>,
    private trialService: TrialService,
    private replayService: ReplayService,
    private loggingService: LoggingService,
    @Inject(MAT_DIALOG_DATA) public data: Replay) {}

  onUpdateClick(): void {
    const dialogResult = this.updateReplayForm.value;
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
    this.updateReplayForm.patchValue({
      replay_id: uuidv4()
    });
  }

  ngOnInit(): void {
    forkJoin(
      {
        trials: this.trialService.readTrials(),
        replays: this.replayService.readReplays()
      }).subscribe(({trials, replays}) => {
      this.trials = trials;
      this.replays = replays;
      let replayParent: Trial | Replay;
      switch (this.data.replay_parent_type) {
        case 'TRIAL':
          this.parents = this.trials;
          replayParent = this.trials.find(t => t.trial_id === this.data.replay_parent_id);
          break;
        case 'REPLAY':
          this.parents = this.replays;
          replayParent = this.replays.find(t => t.replay_id === this.data.replay_parent_id);
          break;
        default:
          this.parents = [];
          break;
      }

      this.ignore_message_list = this.data.ignore_message_list;
      this.ignore_source_list = this.data.ignore_source_list;
      this.ignore_topic_list = this.data.ignore_topic_list;

      this.updateReplayForm.patchValue({
        id: this.data.id,
        replay_id: this.data.replay_id,
        replay_parent_id: replayParent,
        replay_parent_type: this.data.replay_parent_type,
        date: this.data.date,
        ignore_message_list: this.data.ignore_message_list,
        ignore_source_list: this.data.ignore_source_list,
        ignore_topic_list: this.data.ignore_topic_list,
      });
    });
  }

  replayParentTypeChanged(event) {
    this.updateReplayForm.controls.replay_parent_id.reset('', {
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

  compareFnParents(a1: any, a2: any): boolean {
    return a1 && a2 ? a1.id === a2.id : a1 === a2;
  }

  /** Log a CreateReplayComponent message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`UpdateReplayComponent: ${message}`);
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
    if (this.updateReplayForm.controls.ignore_message_list_input.value !== '') {
      const types = this.updateReplayForm.controls.ignore_message_list_input.value.split(' : ');
      const ignoreListType = {
        message_type: types[0],
        sub_type: types[1]
      };
      this.ignore_message_list.push(ignoreListType);
      this.updateReplayForm.controls.ignore_message_list_input.setValue('');
    }
  }

  onRemoveIgnoreMessageListItem(item: any): void {
    const index: number = this.ignore_message_list.findIndex(i => i.message_type === item.message_type && i.sub_type === item.sub_type);
    if (index > -1) {
      this.ignore_message_list.splice(index, 1);
    }
  }

  onAddIgnoreSourceListItem(): void {
    if (this.updateReplayForm.controls.ignore_source_list_input.value !== '') {
      this.ignore_source_list.push(this.updateReplayForm.controls.ignore_source_list_input.value);
      this.updateReplayForm.controls.ignore_source_list_input.setValue('');
    }
  }

  onRemoveIgnoreSourceListItem(source: any): void {
    const index: number = this.ignore_source_list.findIndex(s => s === source);
    if (index > -1) {
      this.ignore_source_list.splice(index, 1);
    }
  }

  onAddIgnoreTopicListItem(): void {
    if (this.updateReplayForm.controls.ignore_topic_list_input.value !== '') {
      this.ignore_topic_list.push(this.updateReplayForm.controls.ignore_topic_list_input.value);
      this.updateReplayForm.controls.ignore_topic_list_input.setValue('');
    }
  }

  onRemoveIgnoreTopicListItem(topic: any): void {
    const index: number = this.ignore_topic_list.findIndex(t => t === topic);
    if (index > -1) {
      this.ignore_topic_list.splice(index, 1);
    }
  }
}
