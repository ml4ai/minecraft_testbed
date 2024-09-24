import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { v4 as uuidv4 } from 'uuid';
import {IgnoreListItem, Replay} from '../../replay/replay';
import { TrialService } from '../../trial/trial.service';
import { Trial } from '../../trial/trial';
import { ReplayService } from '../replay.service';
import { LoggingService } from '../../logging/logging.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-delete-replay',
  templateUrl: './delete-replay.component.html',
  styleUrls: ['./delete-replay.component.scss']
})
export class DeleteReplayComponent implements OnInit {
  parents: Trial[] | Replay[];
  trials: Trial[];
  replays: Replay[];
  replayParentTypes: string[] = ['TRIAL', 'REPLAY'];
  ignore_message_list: IgnoreListItem[] = [];
  ignore_source_list: string[] = [];
  ignore_topic_list: string[] = [];

  deleteReplayForm = this.formBuilder.group({
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
    private dialogRef: MatDialogRef<DeleteReplayComponent>,
    private trialService: TrialService,
    private replayService: ReplayService,
    private loggingService: LoggingService,
    @Inject(MAT_DIALOG_DATA) public data: Replay) {}

  onDeleteClick(): void {
    this.dialogRef.close(this.deleteReplayForm.getRawValue());
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onGenerateUUIDClick(): void {
    this.deleteReplayForm.patchValue({
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

      this.deleteReplayForm.patchValue({
        id: this.data.id,
        replay_id: this.data.replay_id,
        replay_parent_id: replayParent,
        replay_parent_type: this.data.replay_parent_type,
        date: this.data.date,
        ignore_list_input: this.data.ignore_message_list,
        ignore_source_list: this.data.ignore_source_list,
        ignore_topic_list: this.data.ignore_topic_list,
      });
      this.deleteReplayForm.disable();
    });
  }

  replayParentTypeChanged(event) {
    this.deleteReplayForm.controls.replay_parent_id.reset('', {
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
    this.loggingService.add(`DeleteReplayComponent: ${message}`);
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

  // onAddIgnoreListItem(): void {
  //   if (this.updateReplayForm.controls.ignore_list_input.value !== '') {
  //     const types = this.updateReplayForm.controls.ignore_list_input.value.split(' : ');
  //     const ignoreListType = {
  //       message_type: types[0],
  //       sub_type: types[1]
  //     };
  //     this.ignore_list.push(ignoreListType);
  //     this.deleteReplayForm.controls.ignore_list_input.setValue('');
  //   }
  // }
  //
  // onRemoveIgnoreListItem(item: any): void {
  //   const index: number = this.ignore_list.findIndex(i => i.message_type === item.message_type && i.sub_type === item.sub_type);
  //   console.log(index);
  //   if (index > -1) {
  //     this.ignore_list.splice(index, 1);
  //   }
  // }
}
